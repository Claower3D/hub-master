package main

import (
	"database/sql"
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"os"
	"sync"
	"time"

	_ "github.com/lib/pq"
	"golang.org/x/crypto/bcrypt"
)

// User represents a registered account
type User struct {
	ID           int       `json:"id"`
	Name         string    `json:"name"`
	Email        string    `json:"email"`
	Phone        string    `json:"phone"`
	City         string    `json:"city"`
	Bonuses      int       `json:"bonuses"`
	PasswordHash string    `json:"password_hash,omitempty"`
	Role         string    `json:"role"` // "admin" or "customer"
	CreatedAt    time.Time `json:"created_at"`
}

// Session represents a logged-in user session
type Session struct {
	Token     string    `json:"token"`
	UserID    int       `json:"user_id"`
	ExpiresAt time.Time `json:"expires_at"`
}

// CallbackRecord extends CallbackRequest with DB fields
type CallbackRecord struct {
	ID        int       `json:"id"`
	UserID    *int      `json:"user_id"` // Pointer for nullable field
	Name      string    `json:"name"`
	Phone     string    `json:"phone"`
	Service   string    `json:"service"`
	City      string    `json:"city"`
	Address   string    `json:"address"`
	Comment   string    `json:"comment"`
	Status    string    `json:"status"` // "pending", "in_progress", "completed"
	CreatedAt time.Time `json:"created_at"`
}

// ReviewRecord represents a user review in the DB
type ReviewRecord struct {
	ID        int       `json:"id"`
	UserID    *int      `json:"user_id"`
	Author    string    `json:"author"`
	Text      string    `json:"text"`
	Rating    int       `json:"rating"`
	CreatedAt time.Time `json:"created_at"`
}

type CategoryReviewRecord struct {
	ID         int       `json:"id"`
	CategoryID string    `json:"category_id"`
	UserID     *int      `json:"user_id"`
	Author     string    `json:"author"`
	Text       string    `json:"text"`
	Rating     int       `json:"rating"`
	CreatedAt  time.Time `json:"created_at"`
}

type CustomPage struct {
	ID          int    `json:"id"`
	Name        string `json:"name"`
	Type        string `json:"type"` // "section", "category", "subcategory"
	ParentSlug  string `json:"parent_slug"`
	SectionSlug string `json:"section_slug"`
	Slug        string `json:"slug"`
	Description string `json:"description"`
	Image       string `json:"image"`
	FilePath    string `json:"file_path"`
}

// DB defines all database operations
type DB interface {
	CreateUser(name, email, phone, city, password string) (*User, error)
	GetUserByEmail(email string) (*User, error)
	GetUserByPhone(phone string) (*User, error)
	GetUserByID(id int) (*User, error)
	CreateSession(userID int) (*Session, error)
	GetSession(token string) (*Session, error)
	DeleteSession(token string) error
	CreateCallback(req CallbackRequest, userID *int) (*CallbackRecord, error)
	GetCallbacks(userID int, phone string) ([]CallbackRecord, error)
	GetAllCallbacks() ([]CallbackRecord, error)
	UpdateCallbackStatus(id int, status string) error
	DeleteCallback(id int) error
	UpdateUser(id int, name, phone, city, password string) (*User, error)
	AddTelegramSubscriber(chatID int64, name string) error
	RemoveTelegramSubscriber(chatID int64) error
	GetTelegramSubscribers() ([]int64, error)
	CreateReview(author, text string, rating int, userID *int) (*ReviewRecord, error)
	GetReviews() ([]ReviewRecord, error)
	CreateCategoryReview(categoryID string, author string, text string, rating int, userID *int) (*CategoryReviewRecord, error)
	GetCategoryReviews(categoryID string) ([]CategoryReviewRecord, error)
	GetCatalog() (string, error)
	SaveCatalog(catalogJSON string) error
	Close() error

	// Custom Pages methods
	CreateCustomPage(page CustomPage) (*CustomPage, error)
	GetCustomPages() ([]CustomPage, error)
	GetCustomPageByID(id int) (*CustomPage, error)
	GetCustomPageBySlug(slug string, pageType string) (*CustomPage, error)
	UpdateCustomPage(page CustomPage) error
	DeleteCustomPage(id int) error
	AddUserBonuses(id int, amount int) (*User, error)
}


// PostgresDB implements DB interface using PostgreSQL
type PostgresDB struct {
	db *sql.DB
}

func NewPostgresDB(connStr string) (*PostgresDB, error) {
	db, err := sql.Open("postgres", connStr)
	if err != nil {
		return nil, err
	}

	// Test connection
	if err := db.Ping(); err != nil {
		db.Close()
		return nil, err
	}

	// Run migrations
	_, err = db.Exec(`
		CREATE TABLE IF NOT EXISTS users (
			id SERIAL PRIMARY KEY,
			name VARCHAR(255) NOT NULL,
			email VARCHAR(255) UNIQUE NOT NULL,
			phone VARCHAR(255) NOT NULL,
			city VARCHAR(255) NOT NULL,
			password_hash VARCHAR(255) NOT NULL,
			role VARCHAR(50) NOT NULL DEFAULT 'customer',
			bonuses INTEGER NOT NULL DEFAULT 0,
			created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
		);

		ALTER TABLE users ADD COLUMN IF NOT EXISTS bonuses INTEGER NOT NULL DEFAULT 0;
		ALTER TABLE callbacks ADD COLUMN IF NOT EXISTS comment TEXT NOT NULL DEFAULT '';
		ALTER TABLE callbacks ADD COLUMN IF NOT EXISTS address VARCHAR(255) NOT NULL DEFAULT '';

		CREATE TABLE IF NOT EXISTS sessions (
			token VARCHAR(255) PRIMARY KEY,
			user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
			expires_at TIMESTAMP WITH TIME ZONE NOT NULL
		);

		CREATE TABLE IF NOT EXISTS callbacks (
			id SERIAL PRIMARY KEY,
			user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
			name VARCHAR(255) NOT NULL,
			phone VARCHAR(255) NOT NULL,
			service VARCHAR(255) NOT NULL,
			city VARCHAR(255) NOT NULL,
			address VARCHAR(255) NOT NULL DEFAULT '',
			comment TEXT NOT NULL DEFAULT '',
			status VARCHAR(50) NOT NULL DEFAULT 'pending',
			created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
		);

		CREATE TABLE IF NOT EXISTS tg_subscribers (
			chat_id BIGINT PRIMARY KEY,
			name VARCHAR(255) NOT NULL
		);

		CREATE TABLE IF NOT EXISTS reviews (
			id SERIAL PRIMARY KEY,
			user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
			author VARCHAR(255) NOT NULL,
			text TEXT NOT NULL,
			rating INTEGER NOT NULL DEFAULT 5,
			created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
		);

		CREATE TABLE IF NOT EXISTS category_reviews (
			id SERIAL PRIMARY KEY,
			category_id VARCHAR(255) NOT NULL,
			user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
			author VARCHAR(255) NOT NULL,
			text TEXT NOT NULL,
			rating INTEGER NOT NULL DEFAULT 5,
			created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
		);

		CREATE TABLE IF NOT EXISTS catalog (
			id INTEGER PRIMARY KEY,
			data TEXT NOT NULL,
			updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
		);

		CREATE TABLE IF NOT EXISTS custom_pages (
			id SERIAL PRIMARY KEY,
			name VARCHAR(255) NOT NULL,
			type VARCHAR(50) NOT NULL,
			parent_slug VARCHAR(255) NOT NULL DEFAULT '',
			section_slug VARCHAR(255) NOT NULL DEFAULT '',
			slug VARCHAR(255) NOT NULL,
			description TEXT NOT NULL DEFAULT '',
			image VARCHAR(255) NOT NULL DEFAULT '',
			file_path VARCHAR(255) NOT NULL DEFAULT ''
		);
	`)
	if err != nil {
		db.Close()
		return nil, fmt.Errorf("migration failed: %w", err)
	}

	return &PostgresDB{db: db}, nil
}

func (p *PostgresDB) CreateUser(name, email, phone, city, password string) (*User, error) {
	hash, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return nil, err
	}

	role := "customer"
	// Make first user or specific emails admin
	if email == "admin@masterhub.kz" || os.Getenv("INITIAL_ADMIN_EMAIL") == email {
		role = "admin"
	}

	var user User
	err = p.db.QueryRow(`
		INSERT INTO users (name, email, phone, city, password_hash, role, bonuses)
		VALUES ($1, $2, $3, $4, $5, $6, 0)
		RETURNING id, name, email, phone, city, role, bonuses, created_at
	`, name, email, phone, city, string(hash), role).Scan(
		&user.ID, &user.Name, &user.Email, &user.Phone, &user.City, &user.Role, &user.Bonuses, &user.CreatedAt,
	)
	if err != nil {
		return nil, err
	}

	// Link past callbacks with matching phone number
	_, _ = p.db.Exec(`
		UPDATE callbacks SET user_id = $1 WHERE phone = $2 AND user_id IS NULL
	`, user.ID, phone)

	return &user, nil
}

func (p *PostgresDB) GetUserByEmail(email string) (*User, error) {
	var user User
	err := p.db.QueryRow(`
		SELECT id, name, email, phone, city, password_hash, role, bonuses, created_at
		FROM users WHERE email = $1
	`, email).Scan(
		&user.ID, &user.Name, &user.Email, &user.Phone, &user.City, &user.PasswordHash, &user.Role, &user.Bonuses, &user.CreatedAt,
	)
	if err == sql.ErrNoRows {
		return nil, errors.New("user not found")
	}
	if err != nil {
		return nil, err
	}
	return &user, nil
}

func (p *PostgresDB) GetUserByPhone(phone string) (*User, error) {
	var user User
	err := p.db.QueryRow(`
		SELECT id, name, email, phone, city, password_hash, role, bonuses, created_at
		FROM users WHERE phone = $1
	`, phone).Scan(
		&user.ID, &user.Name, &user.Email, &user.Phone, &user.City, &user.PasswordHash, &user.Role, &user.Bonuses, &user.CreatedAt,
	)
	if err == sql.ErrNoRows {
		return nil, errors.New("user not found")
	}
	if err != nil {
		return nil, err
	}
	return &user, nil
}

func (p *PostgresDB) GetUserByID(id int) (*User, error) {
	var user User
	err := p.db.QueryRow(`
		SELECT id, name, email, phone, city, password_hash, role, bonuses, created_at
		FROM users WHERE id = $1
	`, id).Scan(
		&user.ID, &user.Name, &user.Email, &user.Phone, &user.City, &user.PasswordHash, &user.Role, &user.Bonuses, &user.CreatedAt,
	)
	if err == sql.ErrNoRows {
		return nil, errors.New("user not found")
	}
	if err != nil {
		return nil, err
	}
	return &user, nil
}

func (p *PostgresDB) UpdateUser(id int, name, phone, city, password string) (*User, error) {
	var err error
	var hash []byte
	if password != "" {
		hash, err = bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
		if err != nil {
			return nil, err
		}
	}

	var user User
	if password != "" {
		err = p.db.QueryRow(`
			UPDATE users 
			SET name = $1, phone = $2, city = $3, password_hash = $4
			WHERE id = $5
			RETURNING id, name, email, phone, city, role, bonuses, created_at
		`, name, phone, city, string(hash), id).Scan(
			&user.ID, &user.Name, &user.Email, &user.Phone, &user.City, &user.Role, &user.Bonuses, &user.CreatedAt,
		)
	} else {
		err = p.db.QueryRow(`
			UPDATE users 
			SET name = $1, phone = $2, city = $3
			WHERE id = $4
			RETURNING id, name, email, phone, city, role, bonuses, created_at
		`, name, phone, city, id).Scan(
			&user.ID, &user.Name, &user.Email, &user.Phone, &user.City, &user.Role, &user.Bonuses, &user.CreatedAt,
		)
	}

	if err != nil {
		return nil, err
	}
	return &user, nil
}

func (p *PostgresDB) AddUserBonuses(id int, amount int) (*User, error) {
	var user User
	err := p.db.QueryRow(`
		UPDATE users 
		SET bonuses = bonuses + $1
		WHERE id = $2
		RETURNING id, name, email, phone, city, role, bonuses, created_at
	`, amount, id).Scan(
		&user.ID, &user.Name, &user.Email, &user.Phone, &user.City, &user.Role, &user.Bonuses, &user.CreatedAt,
	)
	if err != nil {
		return nil, err
	}
	return &user, nil
}

func (p *PostgresDB) CreateSession(userID int) (*Session, error) {
	// Generate random token
	token := fmt.Sprintf("%x", time.Now().UnixNano()) + fmt.Sprintf("%x", userID)
	expiresAt := time.Now().Add(24 * 7 * time.Hour) // 7 days

	_, err := p.db.Exec(`
		INSERT INTO sessions (token, user_id, expires_at)
		VALUES ($1, $2, $3)
	`, token, userID, expiresAt)
	if err != nil {
		return nil, err
	}

	return &Session{Token: token, UserID: userID, ExpiresAt: expiresAt}, nil
}

func (p *PostgresDB) GetSession(token string) (*Session, error) {
	var sess Session
	err := p.db.QueryRow(`
		SELECT token, user_id, expires_at FROM sessions WHERE token = $1
	`, token).Scan(&sess.Token, &sess.UserID, &sess.ExpiresAt)
	if err == sql.ErrNoRows {
		return nil, errors.New("session not found")
	}
	if err != nil {
		return nil, err
	}

	if time.Now().After(sess.ExpiresAt) {
		p.DeleteSession(token)
		return nil, errors.New("session expired")
	}

	return &sess, nil
}

func (p *PostgresDB) DeleteSession(token string) error {
	_, err := p.db.Exec("DELETE FROM sessions WHERE token = $1", token)
	return err
}

func (p *PostgresDB) CreateCallback(req CallbackRequest, userID *int) (*CallbackRecord, error) {
	var record CallbackRecord
	status := "pending"

	err := p.db.QueryRow(`
		INSERT INTO callbacks (user_id, name, phone, service, city, address, comment, status)
		VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
		RETURNING id, user_id, name, phone, service, city, address, comment, status, created_at
	`, userID, req.Name, req.Phone, req.Service, req.City, req.Address, req.Comment, status).Scan(
		&record.ID, &record.UserID, &record.Name, &record.Phone, &record.Service, &record.City, &record.Address, &record.Comment, &record.Status, &record.CreatedAt,
	)
	if err != nil {
		return nil, err
	}
	return &record, nil
}

func (p *PostgresDB) GetCallbacks(userID int, phone string) ([]CallbackRecord, error) {
	rows, err := p.db.Query(`
		SELECT id, user_id, name, phone, service, city, address, comment, status, created_at
		FROM callbacks
		WHERE user_id = $1 OR phone = $2
		ORDER BY created_at DESC
	`, userID, phone)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var list []CallbackRecord
	for rows.Next() {
		var r CallbackRecord
		if err := rows.Scan(&r.ID, &r.UserID, &r.Name, &r.Phone, &r.Service, &r.City, &r.Address, &r.Comment, &r.Status, &r.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, r)
	}
	return list, nil
}

func (p *PostgresDB) GetAllCallbacks() ([]CallbackRecord, error) {
	rows, err := p.db.Query(`
		SELECT id, user_id, name, phone, service, city, address, comment, status, created_at
		FROM callbacks
		ORDER BY created_at DESC
	`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var list []CallbackRecord
	for rows.Next() {
		var r CallbackRecord
		if err := rows.Scan(&r.ID, &r.UserID, &r.Name, &r.Phone, &r.Service, &r.City, &r.Address, &r.Comment, &r.Status, &r.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, r)
	}
	return list, nil
}

func (p *PostgresDB) UpdateCallbackStatus(id int, status string) error {
	tx, err := p.db.Begin()
	if err != nil {
		return err
	}
	defer tx.Rollback()

	var oldStatus string
	var userID *int
	err = tx.QueryRow("SELECT status, user_id FROM callbacks WHERE id = $1", id).Scan(&oldStatus, &userID)
	if err != nil {
		return err
	}

	_, err = tx.Exec("UPDATE callbacks SET status = $1 WHERE id = $2", status, id)
	if err != nil {
		return err
	}

	if status == "completed" && oldStatus != "completed" && userID != nil {
		_, err = tx.Exec("UPDATE users SET bonuses = bonuses + 1000 WHERE id = $1", *userID)
		if err != nil {
			return err
		}
	}

	return tx.Commit()
}

func (p *PostgresDB) DeleteCallback(id int) error {
	_, err := p.db.Exec("DELETE FROM callbacks WHERE id = $1", id)
	return err
}

func (p *PostgresDB) Close() error {
	return p.db.Close()
}

func (p *PostgresDB) AddTelegramSubscriber(chatID int64, name string) error {
	_, err := p.db.Exec(`
		INSERT INTO tg_subscribers (chat_id, name)
		VALUES ($1, $2)
		ON CONFLICT (chat_id) DO NOTHING
	`, chatID, name)
	return err
}

func (p *PostgresDB) RemoveTelegramSubscriber(chatID int64) error {
	_, err := p.db.Exec("DELETE FROM tg_subscribers WHERE chat_id = $1", chatID)
	return err
}

func (p *PostgresDB) GetTelegramSubscribers() ([]int64, error) {
	rows, err := p.db.Query("SELECT chat_id FROM tg_subscribers")
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var list []int64
	for rows.Next() {
		var cid int64
		if err := rows.Scan(&cid); err != nil {
			return nil, err
		}
		list = append(list, cid)
	}
	return list, nil
}

func (p *PostgresDB) CreateReview(author, text string, rating int, userID *int) (*ReviewRecord, error) {
	var r ReviewRecord
	err := p.db.QueryRow(`
		INSERT INTO reviews (author, text, rating, user_id)
		VALUES ($1, $2, $3, $4)
		RETURNING id, user_id, author, text, rating, created_at
	`, author, text, rating, userID).Scan(&r.ID, &r.UserID, &r.Author, &r.Text, &r.Rating, &r.CreatedAt)
	if err != nil {
		return nil, err
	}
	return &r, nil
}

func (p *PostgresDB) GetReviews() ([]ReviewRecord, error) {
	rows, err := p.db.Query(`
		SELECT id, user_id, author, text, rating, created_at
		FROM reviews
		ORDER BY created_at DESC
	`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var list []ReviewRecord
	for rows.Next() {
		var r ReviewRecord
		if err := rows.Scan(&r.ID, &r.UserID, &r.Author, &r.Text, &r.Rating, &r.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, r)
	}
	return list, nil
}

func (p *PostgresDB) CreateCategoryReview(categoryID string, author string, text string, rating int, userID *int) (*CategoryReviewRecord, error) {
	var r CategoryReviewRecord
	err := p.db.QueryRow(`
		INSERT INTO category_reviews (category_id, author, text, rating, user_id)
		VALUES ($1, $2, $3, $4, $5)
		RETURNING id, category_id, user_id, author, text, rating, created_at
	`, categoryID, author, text, rating, userID).Scan(&r.ID, &r.CategoryID, &r.UserID, &r.Author, &r.Text, &r.Rating, &r.CreatedAt)
	if err != nil {
		return nil, err
	}
	return &r, nil
}

func (p *PostgresDB) GetCategoryReviews(categoryID string) ([]CategoryReviewRecord, error) {
	rows, err := p.db.Query(`
		SELECT id, category_id, user_id, author, text, rating, created_at
		FROM category_reviews
		WHERE category_id = $1
		ORDER BY created_at DESC
	`, categoryID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var list []CategoryReviewRecord
	for rows.Next() {
		var r CategoryReviewRecord
		if err := rows.Scan(&r.ID, &r.CategoryID, &r.UserID, &r.Author, &r.Text, &r.Rating, &r.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, r)
	}
	return list, nil
}

func (p *PostgresDB) GetCatalog() (string, error) {
	var data string
	err := p.db.QueryRow("SELECT data FROM catalog WHERE id = 1").Scan(&data)
	if err == sql.ErrNoRows {
		return "", nil
	}
	return data, err
}

func (p *PostgresDB) SaveCatalog(catalogJSON string) error {
	_, err := p.db.Exec(`
		INSERT INTO catalog (id, data, updated_at)
		VALUES (1, $1, CURRENT_TIMESTAMP)
		ON CONFLICT (id)
		DO UPDATE SET data = EXCLUDED.data, updated_at = CURRENT_TIMESTAMP
	`, catalogJSON)
	return err
}

func (p *PostgresDB) CreateCustomPage(page CustomPage) (*CustomPage, error) {
	err := p.db.QueryRow(`
		INSERT INTO custom_pages (name, type, parent_slug, section_slug, slug, description, image, file_path)
		VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
		RETURNING id
	`, page.Name, page.Type, page.ParentSlug, page.SectionSlug, page.Slug, page.Description, page.Image, page.FilePath).Scan(&page.ID)
	if err != nil {
		return nil, err
	}
	return &page, nil
}

func (p *PostgresDB) GetCustomPages() ([]CustomPage, error) {
	rows, err := p.db.Query("SELECT id, name, type, parent_slug, section_slug, slug, description, image, file_path FROM custom_pages")
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var pages []CustomPage
	for rows.Next() {
		var page CustomPage
		err := rows.Scan(&page.ID, &page.Name, &page.Type, &page.ParentSlug, &page.SectionSlug, &page.Slug, &page.Description, &page.Image, &page.FilePath)
		if err != nil {
			return nil, err
		}
		pages = append(pages, page)
	}
	return pages, nil
}

func (p *PostgresDB) GetCustomPageByID(id int) (*CustomPage, error) {
	var page CustomPage
	err := p.db.QueryRow(`
		SELECT id, name, type, parent_slug, section_slug, slug, description, image, file_path 
		FROM custom_pages WHERE id = $1
	`, id).Scan(&page.ID, &page.Name, &page.Type, &page.ParentSlug, &page.SectionSlug, &page.Slug, &page.Description, &page.Image, &page.FilePath)
	if err == sql.ErrNoRows {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}
	return &page, nil
}

func (p *PostgresDB) GetCustomPageBySlug(slug string, pageType string) (*CustomPage, error) {
	var page CustomPage
	err := p.db.QueryRow(`
		SELECT id, name, type, parent_slug, section_slug, slug, description, image, file_path 
		FROM custom_pages WHERE slug = $1 AND type = $2
	`, slug, pageType).Scan(&page.ID, &page.Name, &page.Type, &page.ParentSlug, &page.SectionSlug, &page.Slug, &page.Description, &page.Image, &page.FilePath)
	if err == sql.ErrNoRows {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}
	return &page, nil
}

func (p *PostgresDB) UpdateCustomPage(page CustomPage) error {
	_, err := p.db.Exec(`
		UPDATE custom_pages 
		SET name = $1, type = $2, parent_slug = $3, section_slug = $4, slug = $5, description = $6, image = $7, file_path = $8
		WHERE id = $9
	`, page.Name, page.Type, page.ParentSlug, page.SectionSlug, page.Slug, page.Description, page.Image, page.FilePath, page.ID)
	return err
}

func (p *PostgresDB) DeleteCustomPage(id int) error {
	_, err := p.db.Exec("DELETE FROM custom_pages WHERE id = $1", id)
	return err
}

type TgSubscriber struct {
	ChatID int64  `json:"chat_id"`
	Name   string `json:"name"`
}

// JsonDB implements DB interface using a single JSON file
type JsonDB struct {
	filePath string
	mu       sync.Mutex
	Data     struct {
		Users           []User                 `json:"users"`
		Sessions        []Session              `json:"sessions"`
		Callbacks       []CallbackRecord       `json:"callbacks"`
		TgSubscribers   []TgSubscriber         `json:"tg_subscribers"`
		Reviews         []ReviewRecord         `json:"reviews"`
		CategoryReviews []CategoryReviewRecord `json:"category_reviews"`
		Catalog         string                 `json:"catalog,omitempty"`
		Pages           []CustomPage           `json:"pages"`
	}
}

func NewJsonDB(filePath string) (*JsonDB, error) {
	db := &JsonDB{filePath: filePath}
	err := db.load()
	if err != nil && !os.IsNotExist(err) {
		return nil, err
	}
	if os.IsNotExist(err) {
		db.Data.Users = []User{}
		db.Data.Sessions = []Session{}
		db.Data.Callbacks = []CallbackRecord{}
		db.Data.TgSubscribers = []TgSubscriber{}
		db.Data.Reviews = []ReviewRecord{}
		db.Data.CategoryReviews = []CategoryReviewRecord{}
		db.Data.Pages = []CustomPage{}
		err = db.save()
		if err != nil {
			return nil, err
		}
	}
	return db, nil
}

func (j *JsonDB) load() error {
	j.mu.Lock()
	defer j.mu.Unlock()
	file, err := os.ReadFile(j.filePath)
	if err != nil {
		return err
	}
	err = json.Unmarshal(file, &j.Data)
	if err != nil {
		return err
	}
	if j.Data.Users == nil {
		j.Data.Users = []User{}
	}
	if j.Data.Sessions == nil {
		j.Data.Sessions = []Session{}
	}
	if j.Data.Callbacks == nil {
		j.Data.Callbacks = []CallbackRecord{}
	}
	if j.Data.TgSubscribers == nil {
		j.Data.TgSubscribers = []TgSubscriber{}
	}
	if j.Data.Reviews == nil {
		j.Data.Reviews = []ReviewRecord{}
	}
	if j.Data.CategoryReviews == nil {
		j.Data.CategoryReviews = []CategoryReviewRecord{}
	}
	return nil
}

func (j *JsonDB) save() error {
	j.mu.Lock()
	defer j.mu.Unlock()
	bytes, err := json.MarshalIndent(j.Data, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(j.filePath, bytes, 0644)
}

func (j *JsonDB) CreateUser(name, email, phone, city, password string) (*User, error) {
	j.load() // Load latest data

	// Check email uniqueness
	for _, u := range j.Data.Users {
		if u.Email == email {
			return nil, errors.New("user with this email already exists")
		}
	}

	hash, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return nil, err
	}

	role := "customer"
	if email == "admin@masterhub.kz" || len(j.Data.Users) == 0 {
		role = "admin" // make first registered user or admin@masterhub.kz an admin
	}

	userID := len(j.Data.Users) + 1
	user := User{
		ID:           userID,
		Name:         name,
		Email:        email,
		Phone:        phone,
		City:         city,
		PasswordHash: string(hash),
		Role:         role,
		CreatedAt:    time.Now(),
	}

	j.Data.Users = append(j.Data.Users, user)

	// Link past callbacks with matching phone number
	for idx, cb := range j.Data.Callbacks {
		if cb.Phone == phone && cb.UserID == nil {
			idVal := userID
			j.Data.Callbacks[idx].UserID = &idVal
		}
	}

	if err := j.save(); err != nil {
		return nil, err
	}

	return &user, nil
}

func (j *JsonDB) GetUserByEmail(email string) (*User, error) {
	j.load()
	for _, u := range j.Data.Users {
		if u.Email == email {
			return &u, nil
		}
	}
	return nil, errors.New("user not found")
}

func (j *JsonDB) GetUserByPhone(phone string) (*User, error) {
	j.load()
	for _, u := range j.Data.Users {
		if u.Phone == phone {
			return &u, nil
		}
	}
	return nil, errors.New("user not found")
}

func (j *JsonDB) GetUserByID(id int) (*User, error) {
	j.load()
	for _, u := range j.Data.Users {
		if u.ID == id {
			return &u, nil
		}
	}
	return nil, errors.New("user not found")
}

func (j *JsonDB) UpdateUser(id int, name, phone, city, password string) (*User, error) {
	j.load()
	for idx, u := range j.Data.Users {
		if u.ID == id {
			j.Data.Users[idx].Name = name
			j.Data.Users[idx].Phone = phone
			j.Data.Users[idx].City = city
			if password != "" {
				hash, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
				if err != nil {
					return nil, err
				}
				j.Data.Users[idx].PasswordHash = string(hash)
			}
			if err := j.save(); err != nil {
				return nil, err
			}
			updated := j.Data.Users[idx]
			return &updated, nil
		}
	}
	return nil, errors.New("user not found")
}

func (j *JsonDB) AddUserBonuses(id int, amount int) (*User, error) {
	j.load()
	for idx, u := range j.Data.Users {
		if u.ID == id {
			j.Data.Users[idx].Bonuses += amount
			if err := j.save(); err != nil {
				return nil, err
			}
			updated := j.Data.Users[idx]
			return &updated, nil
		}
	}
	return nil, errors.New("user not found")
}

func (j *JsonDB) CreateSession(userID int) (*Session, error) {
	j.load()
	token := fmt.Sprintf("%x", time.Now().UnixNano()) + fmt.Sprintf("%x", userID)
	expiresAt := time.Now().Add(24 * 7 * time.Hour)

	sess := Session{
		Token:     token,
		UserID:    userID,
		ExpiresAt: expiresAt,
	}

	j.Data.Sessions = append(j.Data.Sessions, sess)
	if err := j.save(); err != nil {
		return nil, err
	}
	return &sess, nil
}

func (j *JsonDB) GetSession(token string) (*Session, error) {
	j.load()
	for idx, s := range j.Data.Sessions {
		if s.Token == token {
			if time.Now().After(s.ExpiresAt) {
				// Remove expired session
				j.Data.Sessions = append(j.Data.Sessions[:idx], j.Data.Sessions[idx+1:]...)
				j.save()
				return nil, errors.New("session expired")
			}
			return &s, nil
		}
	}
	return nil, errors.New("session not found")
}

func (j *JsonDB) DeleteSession(token string) error {
	j.load()
	for idx, s := range j.Data.Sessions {
		if s.Token == token {
			j.Data.Sessions = append(j.Data.Sessions[:idx], j.Data.Sessions[idx+1:]...)
			return j.save()
		}
	}
	return nil
}

func (j *JsonDB) CreateCallback(req CallbackRequest, userID *int) (*CallbackRecord, error) {
	j.load()
	id := len(j.Data.Callbacks) + 1
	record := CallbackRecord{
		ID:        id,
		UserID:    userID,
		Name:      req.Name,
		Phone:     req.Phone,
		Service:   req.Service,
		City:      req.City,
		Address:   req.Address,
		Comment:   req.Comment,
		Status:    "pending",
		CreatedAt: time.Now(),
	}

	j.Data.Callbacks = append(j.Data.Callbacks, record)
	if err := j.save(); err != nil {
		return nil, err
	}
	return &record, nil
}

func (j *JsonDB) GetCallbacks(userID int, phone string) ([]CallbackRecord, error) {
	j.load()
	var list []CallbackRecord
	// Return in reverse chronological order
	for i := len(j.Data.Callbacks) - 1; i >= 0; i-- {
		cb := j.Data.Callbacks[i]
		if (cb.UserID != nil && *cb.UserID == userID) || cb.Phone == phone {
			list = append(list, cb)
		}
	}
	return list, nil
}

func (j *JsonDB) GetAllCallbacks() ([]CallbackRecord, error) {
	j.load()
	var list []CallbackRecord
	for i := len(j.Data.Callbacks) - 1; i >= 0; i-- {
		list = append(list, j.Data.Callbacks[i])
	}
	return list, nil
}

func (j *JsonDB) UpdateCallbackStatus(id int, status string) error {
	j.load()
	for idx, cb := range j.Data.Callbacks {
		if cb.ID == id {
			oldStatus := cb.Status
			j.Data.Callbacks[idx].Status = status

			if status == "completed" && oldStatus != "completed" && cb.UserID != nil {
				for uIdx, u := range j.Data.Users {
					if u.ID == *cb.UserID {
						j.Data.Users[uIdx].Bonuses += 1000
						break
					}
				}
			}
			return j.save()
		}
	}
	return errors.New("callback not found")
}

func (j *JsonDB) DeleteCallback(id int) error {
	j.load()
	found := false
	var updated []CallbackRecord
	for _, cb := range j.Data.Callbacks {
		if cb.ID == id {
			found = true
			continue
		}
		updated = append(updated, cb)
	}
	if !found {
		return errors.New("callback not found")
	}
	j.Data.Callbacks = updated
	return j.save()
}

func (j *JsonDB) AddTelegramSubscriber(chatID int64, name string) error {
	j.load()
	for _, s := range j.Data.TgSubscribers {
		if s.ChatID == chatID {
			return nil // already exists
		}
	}
	j.Data.TgSubscribers = append(j.Data.TgSubscribers, TgSubscriber{ChatID: chatID, Name: name})
	return j.save()
}

func (j *JsonDB) RemoveTelegramSubscriber(chatID int64) error {
	j.load()
	for idx, s := range j.Data.TgSubscribers {
		if s.ChatID == chatID {
			j.Data.TgSubscribers = append(j.Data.TgSubscribers[:idx], j.Data.TgSubscribers[idx+1:]...)
			return j.save()
		}
	}
	return nil
}

func (j *JsonDB) GetTelegramSubscribers() ([]int64, error) {
	j.load()
	var list []int64
	for _, s := range j.Data.TgSubscribers {
		list = append(list, s.ChatID)
	}
	return list, nil
}

func (j *JsonDB) Close() error {
	return nil
}

func (j *JsonDB) CreateReview(author, text string, rating int, userID *int) (*ReviewRecord, error) {
	j.load()
	id := 1
	if len(j.Data.Reviews) > 0 {
		id = j.Data.Reviews[len(j.Data.Reviews)-1].ID + 1
	}

	r := ReviewRecord{
		ID:        id,
		UserID:    userID,
		Author:    author,
		Text:      text,
		Rating:    rating,
		CreatedAt: time.Now(),
	}
	j.Data.Reviews = append(j.Data.Reviews, r)
	if err := j.save(); err != nil {
		return nil, err
	}
	return &r, nil
}

func (j *JsonDB) GetReviews() ([]ReviewRecord, error) {
	j.load()
	var list []ReviewRecord
	for i := len(j.Data.Reviews) - 1; i >= 0; i-- {
		list = append(list, j.Data.Reviews[i])
	}
	return list, nil
}

func (j *JsonDB) CreateCategoryReview(categoryID string, author string, text string, rating int, userID *int) (*CategoryReviewRecord, error) {
	j.load()
	id := 1
	if len(j.Data.CategoryReviews) > 0 {
		id = j.Data.CategoryReviews[len(j.Data.CategoryReviews)-1].ID + 1
	}

	r := CategoryReviewRecord{
		ID:         id,
		CategoryID: categoryID,
		UserID:     userID,
		Author:     author,
		Text:       text,
		Rating:     rating,
		CreatedAt:  time.Now(),
	}
	j.Data.CategoryReviews = append(j.Data.CategoryReviews, r)
	if err := j.save(); err != nil {
		return nil, err
	}
	return &r, nil
}

func (j *JsonDB) GetCategoryReviews(categoryID string) ([]CategoryReviewRecord, error) {
	j.load()
	var list []CategoryReviewRecord
	for i := len(j.Data.CategoryReviews) - 1; i >= 0; i-- {
		cb := j.Data.CategoryReviews[i]
		if cb.CategoryID == categoryID {
			list = append(list, cb)
		}
	}
	return list, nil
}

func (j *JsonDB) GetCatalog() (string, error) {
	j.load()
	return j.Data.Catalog, nil
}

func (j *JsonDB) SaveCatalog(catalogJSON string) error {
	j.load()
	j.Data.Catalog = catalogJSON
	return j.save()
}

func (j *JsonDB) CreateCustomPage(page CustomPage) (*CustomPage, error) {
	j.load()
	maxID := 0
	for _, p := range j.Data.Pages {
		if p.ID > maxID {
			maxID = p.ID
		}
	}
	page.ID = maxID + 1
	j.Data.Pages = append(j.Data.Pages, page)
	if err := j.save(); err != nil {
		return nil, err
	}
	return &page, nil
}

func (j *JsonDB) GetCustomPages() ([]CustomPage, error) {
	j.load()
	pages := make([]CustomPage, len(j.Data.Pages))
	copy(pages, j.Data.Pages)
	return pages, nil
}

func (j *JsonDB) GetCustomPageByID(id int) (*CustomPage, error) {
	j.load()
	for _, p := range j.Data.Pages {
		if p.ID == id {
			return &p, nil
		}
	}
	return nil, nil
}

func (j *JsonDB) GetCustomPageBySlug(slug string, pageType string) (*CustomPage, error) {
	j.load()
	for _, p := range j.Data.Pages {
		if p.Slug == slug && p.Type == pageType {
			return &p, nil
		}
	}
	return nil, nil
}

func (j *JsonDB) UpdateCustomPage(page CustomPage) error {
	j.load()
	for i, p := range j.Data.Pages {
		if p.ID == page.ID {
			j.Data.Pages[i] = page
			return j.save()
		}
	}
	return fmt.Errorf("page not found")
}

func (j *JsonDB) DeleteCustomPage(id int) error {
	j.load()
	for i, p := range j.Data.Pages {
		if p.ID == id {
			j.Data.Pages = append(j.Data.Pages[:i], j.Data.Pages[i+1:]...)
			return j.save()
		}
	}
	return fmt.Errorf("page not found")
}


// Helper function to initialize database connection
func InitDB() (DB, error) {
	dbURL := os.Getenv("DATABASE_URL")
	if dbURL == "" {
		if os.Getenv("PGPASSWORD") != "" {
			dbURL = fmt.Sprintf("postgres://postgres:%s@localhost:5432/masterhub?sslmode=disable", os.Getenv("PGPASSWORD"))
		}
	}

	var db DB
	var err error

	jsonDBPath := resolvePath("data/masterhub_db.json")
	oldJsonDBPath := resolvePath("data/masterhub_data.json")

	// Migration: if masterhub_db.json doesn't exist but masterhub_data.json does, copy it
	if _, errStat := os.Stat(jsonDBPath); os.IsNotExist(errStat) {
		if _, errStat := os.Stat(oldJsonDBPath); errStat == nil {
			log.Println("🔄 Migrating old JSON DB to new un-tracked JSON DB (masterhub_db.json)...")
			input, readErr := os.ReadFile(oldJsonDBPath)
			if readErr == nil {
				_ = os.WriteFile(jsonDBPath, input, 0644)
			}
		}
	}

	if dbURL != "" {
		log.Println("🔌 Connecting to PostgreSQL database...")
		db, err = NewPostgresDB(dbURL)
		if err == nil {
			log.Println("✅ Connected to PostgreSQL successfully!")
		} else {
			log.Printf("⚠️ PostgreSQL connection failed: %v. Falling back to JSON storage.\n", err)
			db, err = NewJsonDB(jsonDBPath)
		}
	} else {
		log.Println("📁 Using JSON local file storage (masterhub_db.json)...")
		db, err = NewJsonDB(jsonDBPath)
	}

	if err != nil {
		return nil, err
	}

	// Seed default test admin account
	_, err = db.GetUserByEmail("admin@masterhub.kz")
	if err != nil {
		log.Println("👤 Seeding default admin account (admin@masterhub.kz)...")
		_, err = db.CreateUser("Administrator", "admin@masterhub.kz", "+77777777777", "almaty", "admin123")
		if err != nil {
			log.Printf("⚠️ Failed to seed admin account: %v\n", err)
		}
	}

	return db, nil
}
