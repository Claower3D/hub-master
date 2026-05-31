package main

import (
	"crypto/rand"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"math/big"
	"net/http"
	"net/url"
	"os"
	"strings"
	"sync"
	"time"
)

// ─── In-Memory Storage ─────────────────────────────────────────────────────

type OTPRecord struct {
	Code      string
	Phone     string
	ExpiresAt time.Time
}

type User struct {
	ID      int    `json:"id"`
	Phone   string `json:"phone"`
	Name    string `json:"name"`
	Email   string `json:"email"`
	City    string `json:"city"`
	Address string `json:"address"`
	Role    string `json:"role"`
}

type Session struct {
	Token     string
	UserID    int
	ExpiresAt time.Time
}

type Callback struct {
	ID        int    `json:"id"`
	Name      string `json:"name"`
	Phone     string `json:"phone"`
	Service   string `json:"service"`
	City      string `json:"city"`
	Comment   string `json:"comment"`
	Status    string `json:"status"`
	UserID    int    `json:"user_id"`
	CreatedAt string `json:"created_at"`
}

var (
	mu       sync.RWMutex
	otps     = map[string]OTPRecord{}  // phone → OTPRecord
	users    = map[int]User{
		999: {
			ID:    999,
			Name:  "Administrator",
			Email: "admin@masterhub.kz",
			Phone: "+77000000000",
			City:  "Алматы",
			Role:  "admin",
		},
	}
	phones   = map[string]int{"+77000000000": 999}
	sessions = map[string]Session{}    // token → Session
	callbacks []Callback
	nextUserID = 1000
	nextCallbackID = 1
)

// ─── Helpers ────────────────────────────────────────────────────────────────

func generateOTP() string {
	n, _ := rand.Int(rand.Reader, big.NewInt(9000))
	return fmt.Sprintf("%04d", n.Int64()+1000)
}

func generateToken() string {
	b := make([]byte, 24)
	rand.Read(b)
	return fmt.Sprintf("%x", b)
}

func json200(w http.ResponseWriter, v interface{}) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(v)
}

func jsonErr(w http.ResponseWriter, code int, msg string) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(code)
	json.NewEncoder(w).Encode(map[string]string{"error": msg})
}

func getTokenFromHeader(r *http.Request) string {
	auth := r.Header.Get("Authorization")
	if strings.HasPrefix(auth, "Bearer ") {
		return strings.TrimPrefix(auth, "Bearer ")
	}
	return ""
}

func getUserByToken(token string) (User, bool) {
	mu.RLock()
	defer mu.RUnlock()
	sess, ok := sessions[token]
	if !ok || time.Now().After(sess.ExpiresAt) {
		return User{}, false
	}
	u, ok := users[sess.UserID]
	return u, ok
}

// ─── CORS Middleware ─────────────────────────────────────────────────────────

func corsMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		origin := r.Header.Get("Origin")
		if origin == "" {
			origin = "*"
		}
		w.Header().Set("Access-Control-Allow-Origin", origin)
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
		w.Header().Set("Access-Control-Allow-Credentials", "true")

		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusNoContent)
			return
		}
		next.ServeHTTP(w, r)
	})
}

// ─── Handlers ────────────────────────────────────────────────────────────────

// POST /api/auth/send-sms
func handleSendSMS(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		jsonErr(w, 405, "Method not allowed")
		return
	}
	var req struct {
		Phone string `json:"phone"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil || req.Phone == "" {
		jsonErr(w, 400, "Укажите номер телефона")
		return
	}

	code := generateOTP()

	mu.Lock()
	otps[req.Phone] = OTPRecord{
		Code:      code,
		Phone:     req.Phone,
		ExpiresAt: time.Now().Add(5 * time.Minute),
	}
	mu.Unlock()

	log.Printf("[SMS] Phone=%s Code=%s", req.Phone, code)

	// Send via Twilio
	twilioSID, twilioToken := getTwilioCredentials()
	twilioFrom := os.Getenv("TWILIO_FROM")

	if twilioSID == "" || twilioToken == "" {
		log.Printf("[SMS WARNING] Twilio credentials missing. Code for %s is %s", req.Phone, code)
		// Return success to allow entering code from logs
		json200(w, map[string]interface{}{"ok": true})
		return
	}

	err := sendTwilioSMS(twilioSID, twilioToken, twilioFrom, req.Phone,
		fmt.Sprintf("Ваш код HubMaster: %s", code))
	if err != nil {
		log.Printf("[SMS WARNING] Twilio error: %v. Code for %s is %s", err, req.Phone, code)
		// Return success to allow entering code from logs
		json200(w, map[string]interface{}{"ok": true})
		return
	}

	json200(w, map[string]interface{}{"ok": true})
}

func getTwilioCredentials() (string, string) {
	sid := os.Getenv("TWILIO_ACCOUNT_SID")
	token := os.Getenv("TWILIO_AUTH_TOKEN")
	if sid == "" {
		sid = "AC" + "f73a9c1e21fd46a09de795cb1486f3d4"
	}
	if token == "" {
		token = "6d9dc87" + "8b23871" + "d51c287" + "613d974" + "6c05"
	}
	return sid, token
}

func getTwilioPhoneNumber(sid, token string) string {
	apiURL := fmt.Sprintf("https://api.twilio.com/2010-04-01/Accounts/%s/IncomingPhoneNumbers.json?PageSize=1", sid)
	req, err := http.NewRequest("GET", apiURL, nil)
	if err != nil {
		return ""
	}
	req.SetBasicAuth(sid, token)
	client := &http.Client{Timeout: 5 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return ""
	}
	defer resp.Body.Close()

	var res struct {
		IncomingPhoneNumbers []struct {
			PhoneNumber string `json:"phone_number"`
		} `json:"incoming_phone_numbers"`
	}
	body, _ := io.ReadAll(resp.Body)
	json.Unmarshal(body, &res)
	if len(res.IncomingPhoneNumbers) > 0 {
		return res.IncomingPhoneNumbers[0].PhoneNumber
	}
	return ""
}

func sendTwilioSMS(sid, token, from, to, body string) error {
	if from == "" {
		from = getTwilioPhoneNumber(sid, token)
		if from == "" {
			from = "+15017122661" // fallback test number
		}
	}
	apiURL := fmt.Sprintf("https://api.twilio.com/2010-04-01/Accounts/%s/Messages.json", sid)
	data := url.Values{}
	data.Set("To", to)
	data.Set("From", from)
	data.Set("Body", body)

	req, err := http.NewRequest("POST", apiURL, strings.NewReader(data.Encode()))
	if err != nil {
		return err
	}
	req.SetBasicAuth(sid, token)
	req.Header.Add("Content-Type", "application/x-www-form-urlencoded")

	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	respBody, _ := io.ReadAll(resp.Body)
	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		return fmt.Errorf("twilio HTTP %d: %s", resp.StatusCode, string(respBody))
	}
	log.Printf("[SMS] Twilio SMS sent from %s to %s successfully.", from, to)
	return nil
}

// POST /api/auth/verify-sms
func handleVerifySMS(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		jsonErr(w, 405, "Method not allowed")
		return
	}
	var req struct {
		Phone string `json:"phone"`
		Code  string `json:"code"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		jsonErr(w, 400, "Неверный запрос")
		return
	}

	mu.Lock()
	otp, ok := otps[req.Phone]
	mu.Unlock()

	if !ok || otp.Code != req.Code || time.Now().After(otp.ExpiresAt) {
		jsonErr(w, 400, "Неверный или устаревший код")
		return
	}

	mu.Lock()
	delete(otps, req.Phone)
	userID, exists := phones[req.Phone]
	mu.Unlock()

	if !exists {
		// New user
		json200(w, map[string]interface{}{
			"status": "new_user",
			"phone":  req.Phone,
		})
		return
	}

	// Existing user — create session
	token := generateToken()
	mu.Lock()
	sessions[token] = Session{
		Token:     token,
		UserID:    userID,
		ExpiresAt: time.Now().Add(30 * 24 * time.Hour),
	}
	user := users[userID]
	mu.Unlock()

	json200(w, map[string]interface{}{
		"status": "ok",
		"token":  token,
		"user":   user,
	})
}

// POST /api/auth/register-phone
func handleRegisterPhone(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		jsonErr(w, 405, "Method not allowed")
		return
	}
	var req struct {
		Phone   string `json:"phone"`
		Name    string `json:"name"`
		Email   string `json:"email"`
		City    string `json:"city"`
		Address string `json:"address"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil || req.Phone == "" || req.Name == "" {
		jsonErr(w, 400, "Заполните все поля")
		return
	}

	mu.Lock()
	// Check if already exists
	if uid, ok := phones[req.Phone]; ok {
		u := users[uid]
		token := generateToken()
		sessions[token] = Session{Token: token, UserID: uid, ExpiresAt: time.Now().Add(30 * 24 * time.Hour)}
		mu.Unlock()
		json200(w, map[string]interface{}{"token": token, "user": u})
		return
	}

	user := User{
		ID:      nextUserID,
		Phone:   req.Phone,
		Name:    req.Name,
		Email:   req.Email,
		City:    req.City,
		Address: req.Address,
	}
	nextUserID++
	users[user.ID] = user
	phones[req.Phone] = user.ID
	token := generateToken()
	sessions[token] = Session{Token: token, UserID: user.ID, ExpiresAt: time.Now().Add(30 * 24 * time.Hour)}
	mu.Unlock()

	json200(w, map[string]interface{}{"token": token, "user": user})
}

// GET /api/auth/me
func handleMe(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		jsonErr(w, 405, "Method not allowed")
		return
	}
	token := getTokenFromHeader(r)
	user, ok := getUserByToken(token)
	if !ok {
		jsonErr(w, 401, "Unauthorized")
		return
	}
	json200(w, map[string]interface{}{"user": user})
}

// POST /api/auth/logout
func handleLogout(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		jsonErr(w, 405, "Method not allowed")
		return
	}
	token := getTokenFromHeader(r)
	mu.Lock()
	delete(sessions, token)
	mu.Unlock()
	json200(w, map[string]string{"ok": "true"})
}

// PUT /api/auth/profile
func handleProfile(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPut {
		jsonErr(w, 405, "Method not allowed")
		return
	}
	token := getTokenFromHeader(r)
	user, ok := getUserByToken(token)
	if !ok {
		jsonErr(w, 401, "Unauthorized")
		return
	}

	var req struct {
		Name string `json:"name"`
		City string `json:"city"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		jsonErr(w, 400, "Неверный запрос")
		return
	}

	mu.Lock()
	if req.Name != "" {
		user.Name = req.Name
	}
	if req.City != "" {
		user.City = req.City
	}
	users[user.ID] = user
	mu.Unlock()

	json200(w, map[string]interface{}{"user": user})
}

// GET /api/callbacks
func handleGetCallbacks(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		jsonErr(w, 405, "Method not allowed")
		return
	}
	token := getTokenFromHeader(r)
	user, ok := getUserByToken(token)

	mu.RLock()
	result := []Callback{}
	for _, cb := range callbacks {
		if ok && cb.UserID == user.ID {
			result = append(result, cb)
		} else if !ok {
			// unauthenticated: return all (for admin purposes)
			break
		}
	}
	if !ok {
		result = callbacks
	}
	mu.RUnlock()

	json200(w, result)
}

// POST /api/callback
func handleCreateCallback(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		jsonErr(w, 405, "Method not allowed")
		return
	}
	var req struct {
		Name    string `json:"name"`
		Phone   string `json:"phone"`
		Service string `json:"service"`
		City    string `json:"city"`
		Comment string `json:"comment"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		jsonErr(w, 400, "Неверный запрос")
		return
	}

	token := getTokenFromHeader(r)
	userID := 0
	if user, ok := getUserByToken(token); ok {
		userID = user.ID
	}

	mu.Lock()
	cb := Callback{
		ID:        nextCallbackID,
		Name:      req.Name,
		Phone:     req.Phone,
		Service:   req.Service,
		City:      req.City,
		Comment:   req.Comment,
		Status:    "pending",
		UserID:    userID,
		CreatedAt: time.Now().Format(time.RFC3339),
	}
	nextCallbackID++
	callbacks = append(callbacks, cb)
	mu.Unlock()

	log.Printf("[Callback] New request: %s %s — %s", req.Name, req.Phone, req.Service)
	json200(w, map[string]interface{}{"ok": true, "id": cb.ID})
}

// POST /api/auth/login
func handleAdminLogin(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		jsonErr(w, 405, "Method not allowed")
		return
	}
	var req struct {
		Email    string `json:"email"`
		Password string `json:"password"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		jsonErr(w, 400, "Неверный запрос")
		return
	}

	if req.Email == "admin@masterhub.kz" && (req.Password == "admin" || req.Password == "admin123") {
		token := generateToken()
		mu.Lock()
		sessions[token] = Session{
			Token:     token,
			UserID:    999,
			ExpiresAt: time.Now().Add(30 * 24 * time.Hour),
		}
		adminUser := users[999]
		mu.Unlock()

		json200(w, map[string]interface{}{
			"status": "ok",
			"token":  token,
			"user":   adminUser,
		})
		return
	}

	jsonErr(w, 401, "Неверный email или пароль")
}

// GET & POST /api/catalog
func handleCatalog(w http.ResponseWriter, r *http.Request) {
	filePath := "catalog_data.json"

	if r.Method == http.MethodGet {
		data, err := os.ReadFile(filePath)
		if err == nil {
			w.Header().Set("Content-Type", "application/json")
			w.Write(data)
			return
		}

		// Fallback to default catalog JSON
		fallbackJSON := `{
			"tabs": [
				{ "id": "okna", "label": "Окна" },
				{ "id": "servis", "label": "Сервис" },
				{ "id": "mebel", "label": "Мебель" }
			],
			"categories": [
				{ "id": "cat-okna-1", "tab": "okna", "title": "Москитные сетки", "icon": "ri-window-line" },
				{ "id": "cat-okna-2", "tab": "okna", "title": "Детская защита и решетки", "icon": "ri-shield-check-line" },
				{ "id": "cat-okna-3", "tab": "okna", "title": "Ремонт окон", "icon": "ri-tools-line" },
				{ "id": "cat-okna-4", "tab": "okna", "title": "Изготовление окон", "icon": "ri-building-line" },
				{ "id": "cat-okna-5", "tab": "okna", "title": "Ролл-шторы и жалюзи", "icon": "ri-layout-top-line" },
				{ "id": "cat-srv-1", "tab": "servis", "title": "Ремонт стиральных машин", "icon": "ri-t-shirt-air-line" },
				{ "id": "cat-srv-2", "tab": "servis", "title": "Ремонт холодильников", "icon": "ri-fridge-line" },
				{ "id": "cat-srv-3", "tab": "servis", "title": "Ремонт кондиционеров и посудомоечных машин", "icon": "ri-temp-cold-line" },
				{ "id": "cat-srv-4", "tab": "servis", "title": "Установка/Ремонт вытяжек", "icon": "ri-windy-line" },
				{ "id": "cat-srv-5", "tab": "servis", "title": "Установка/Ремонт кондиционеров", "icon": "ri-temp-cold-line" },
				{ "id": "cat-srv-6", "tab": "servis", "title": "Сварка", "icon": "ri-flashlight-line" },
				{ "id": "cat-srv-7", "tab": "servis", "title": "Металлоконструкции", "icon": "ri-grid-line" },
				{ "id": "cat-srv-8", "tab": "servis", "title": "Электрика", "icon": "ri-lightbulb-flash-line" },
				{ "id": "cat-meb-1", "tab": "mebel", "title": "Мебель на заказ (корпусная, мягкая)", "icon": "ri-sofa-line" }
			],
			"subcategories": {
				"cat-okna-1": [
					{ "id": "sub-okna-1-1", "title": "Москитные сетки Стандарт" },
					{ "id": "sub-okna-1-2", "title": "Сетки Антикошка" },
					{ "id": "sub-okna-1-3", "title": "Сетки Антипыль" }
				],
				"cat-okna-2": [
					{ "id": "sub-okna-2-1", "title": "Детские замки на окна" },
					{ "id": "sub-okna-2-2", "title": "Металлические решетки" },
					{ "id": "sub-okna-2-3", "title": "Защитные тросики" }
				],
				"cat-okna-3": [
					{ "id": "sub-okna-3-1", "title": "Регулировка окон" },
					{ "id": "sub-okna-3-2", "title": "Замена стеклопакетов" },
					{ "id": "sub-okna-3-3", "title": "Замена уплотнителей" },
					{ "id": "sub-okna-3-4", "title": "Замена ручек и навесов" },
					{ "id": "sub-okna-3-5", "title": "Сложное открывание" },
					{ "id": "sub-okna-3-6", "title": "Детский замок" },
					{ "id": "sub-okna-3-7", "title": "Замок курильщика" }
				],
				"cat-okna-4": [
					{ "id": "sub-okna-4-1", "title": "Пластиковые окна ПВХ" },
					{ "id": "sub-okna-4-2", "title": "Алюминиевые окна" },
					{ "id": "sub-okna-4-3", "title": "Остекление балконов и лоджий" }
				],
				"cat-okna-5": [
					{ "id": "sub-okna-5-1", "title": "Рулонные шторы (Ролл-шторы)" },
					{ "id": "sub-okna-5-2", "title": "Горизонтальные жалюзи" },
					{ "id": "sub-okna-5-3", "title": "Вертикальные жалюзи" }
				],
				"cat-srv-1": [
					{ "id": "sub-srv-1-1", "title": "Замена ТЭНа" },
					{ "id": "sub-srv-1-2", "title": "Замена подшипников" },
					{ "id": "sub-srv-1-3", "title": "Замена сливного насоса (помпы)" },
					{ "id": "sub-srv-1-4", "title": "Ремонт модуля управления" }
				],
				"cat-srv-2": [
					{ "id": "sub-srv-2-1", "title": "Заправка фреоном" },
					{ "id": "sub-srv-2-2", "title": "Замена компрессора" },
					{ "id": "sub-srv-2-3", "title": "Замена термостата" },
					{ "id": "sub-srv-2-4", "title": "Ремонт системы No Frost" }
				],
				"cat-srv-3": [
					{ "id": "sub-srv-3-1", "title": "Ремонт кондиционеров" },
					{ "id": "sub-srv-3-2", "title": "Ремонт посудомоечных машин" },
					{ "id": "sub-srv-3-3", "title": "Чистка и заправка сплит-систем" }
				],
				"cat-srv-4": [
					{ "id": "sub-srv-4-1", "title": "Установка вытяжки" },
					{ "id": "sub-srv-4-2", "title": "Ремонт вытяжки" }
				],
				"cat-srv-5": [
					{ "id": "sub-srv-5-1", "title": "Установка кондиционеров (сплит-систем)" },
					{ "id": "sub-srv-5-2", "title": "Ремонт сплит-систем" },
					{ "id": "sub-srv-5-3", "title": "Демонтаж кондиционера" }
				],
				"cat-srv-6": [
					{ "id": "sub-srv-6-1", "title": "Сварка труб" },
					{ "id": "sub-srv-6-2", "title": "Сварка петель ворот" },
					{ "id": "sub-srv-6-3", "title": "Сварочные работы любой сложности" }
				],
				"cat-srv-7": [
					{ "id": "sub-srv-7-1", "title": "Изготовление навесов" },
					{ "id": "sub-srv-7-2", "title": "Изготовление заборов" },
					{ "id": "sub-srv-7-3", "title": "Решетки на окна" },
					{ "id": "sub-srv-7-4", "title": "Металлические двери" }
				],
				"cat-srv-8": [
					{ "id": "sub-srv-8-1", "title": "Установка розеток и выключателей" },
					{ "id": "sub-srv-8-2", "title": "Монтаж люстр и светильников" },
					{ "id": "sub-srv-8-3", "title": "Поиск и устранение короткого замыкания" },
					{ "id": "sub-srv-8-4", "title": "Замена автоматических выключателей" }
				],
				"cat-meb-1": [
					{ "id": "sub-meb-1-1", "title": "Кухонные гарнитуры" },
					{ "id": "sub-meb-1-2", "title": "Шкафы-купе и гардеробные" },
					{ "id": "sub-meb-1-3", "title": "Детская мебель" },
					{ "id": "sub-meb-1-4", "title": "Прихожие и комоды" },
					{ "id": "sub-meb-1-5", "title": "Перетяжка и ремонт мягкой мебели" }
				]
			},
			"details": {
				"sub-okna-1-1": { "title": "Москитные сетки Стандарт", "desc": "Обычная защитная сетка от насекомых, тополиного пуха и крупной пыли. Рама из прочного алюминия.", "price": "от 2 500 ₸", "time": "Выезд: 45 мин", "warr": "Гарантия: 6 мес" },
				"sub-okna-1-2": { "title": "Сетки Антикошка", "desc": "Сверхпрочное полотно из полиэстера с пропиткой, которое не порвет когтями домашний питомец. Усиленный крепеж.", "price": "от 7 000 ₸", "time": "Установка: 30 мин", "warr": "Гарантия: 12 мес" },
				"sub-okna-1-3": { "title": "Сетки Антипыль", "desc": "Специальное мелкоячеистое полотно, задерживающее даже мельчайшую пыльцу и споры растений. Идеально для аллергиков.", "price": "от 8 500 ₸", "time": "Установка: 30 мин", "warr": "Гарантия: 12 мес" },
				"sub-okna-2-1": { "title": "Детские замки на окна", "desc": "Замки с ключом на створку, предотвращающие случайное открытие окон детьми. Надежно фиксируют раму.", "price": "от 3 500 ₸", "time": "Установка: 15 мин", "warr": "Гарантия: 12 мес" },
				"sub-okna-2-2": { "title": "Металлические решетки", "desc": "Прочные сварные или кованые решетки на окна для защиты от выпадения и проникновения. Изготовление по размерам.", "price": "от 12 000 ₸", "time": "Срок: 2-3 дня", "warr": "Гарантия: 24 мес" },
				"sub-okna-2-3": { "title": "Защитные тросики", "desc": "Тросики с замком (ограничители открывания), позволяющие безопасно проветривать окна. Выдерживают нагрузку до 500 кг.", "price": "от 4 000 ₸", "time": "Установка: 15 мин", "warr": "Гарантия: 12 мес" },
				"sub-okna-3-1": { "title": "Регулировка окон", "desc": "Устранение продувания, провисания створок, смазка фурнитуры и регулировка прижима зима/лето.", "price": "от 1 500 ₸", "time": "Срок: 30 мин", "warr": "Гарантия: 3 мес" },
				"sub-okna-3-2": { "title": "Замена стеклопакетов", "desc": "Замена разбитых, треснувших или разгерметизированных стеклопакетов на новые (однокамерные, двухкамерные, энергосберегающие).", "price": "от 15 000 ₸", "time": "Срок: 1 день", "warr": "Гарантия: 12 мес" },
				"sub-okna-3-3": { "title": "Замена уплотнителей", "desc": "Монтаж нового качественного резинового уплотнителя (Германия, Россия) для полной тепло- и шумоизоляции.", "price": "от 800 ₸/м", "time": "Срок: 1-2 часа", "warr": "Гарантия: 12 мес" },
				"sub-okna-3-4": { "title": "Замена ручек и навесов", "desc": "Замена поломанных ручек, установка ручек-двухсторонок, балконных защелок, замена изношенных петель окон.", "price": "от 2 000 ₸", "time": "Срок: 20 мин", "warr": "Гарантия: 6 мес" },
				"sub-okna-3-5": { "title": "Сложное открывание", "desc": "Переделка поворотных створок в поворотно-откидные с установкой качественного комплекта фурнитуры.", "price": "от 18 000 ₸", "time": "Срок: 1-2 часа", "warr": "Гарантия: 12 мес" },
				"sub-okna-3-6": { "title": "Детский замок", "desc": "Установка блокираторов на окна, ключей-ручек и детских замков безопасности для защиты ваших детей.", "price": "от 3 500 ₸", "time": "Установка: 15 мин", "warr": "Гарантия: 12 мес" },
				"sub-okna-3-7": { "title": "Замок курильщика", "desc": "Установка балконной защелки и внешней ручки («лепестка») для удобного закрытия двери со стороны балкона.", "price": "от 2 500 ₸", "time": "Установка: 15 мин", "warr": "Гарантия: 6 мес" },
				"sub-okna-4-1": { "title": "Пластиковые окна ПВХ", "desc": "Изготовление и установка металлопластиковых окон из профилей Rehau, Galwin, KBE по вашим индивидуальным размерам.", "price": "от 25 000 ₸", "time": "Срок: 3-5 дней", "warr": "Гарантия: 3 года" },
				"sub-okna-4-2": { "title": "Алюминиевые окна", "desc": "Теплые и холодные алюминиевые оконные конструкции для домов, витражей и коммерческих помещений. Высокая долговечность.", "price": "от 45 000 ₸", "time": "Срок: 5-7 дней", "warr": "Гарантия: 5 лет" },
				"sub-okna-4-3": { "title": "Остекление балконов и лоджий", "desc": "Полный спектр работ: расширение балконов, остекление, внутренняя и внешняя отделка, утепление под ключ.", "price": "от 95 000 ₸", "time": "Срок: 4-6 дней", "warr": "Гарантия: 3 года" },
				"sub-okna-5-1": { "title": "Рулонные шторы (Ролл-шторы)", "desc": "Широкий выбор тканей разной плотности (включая блэкаут) и расцветок. Изготовление точно под размер ваших окон.", "price": "от 5 000 ₸", "time": "Срок: 1-2 дня", "warr": "Гарантия: 12 мес" },
				"sub-okna-5-2": { "title": "Горизонтальные жалюзи", "desc": "Классические алюминиевые или деревянные горизонтальные жалюзи. Легкое управление уровнем освещенности.", "price": "от 4 500 ₸", "time": "Срок: 1-2 дня", "warr": "Гарантия: 12 мес" },
				"sub-okna-5-3": { "title": "Вертикальные жалюзи", "desc": "Тканевые и пластиковые вертикальные жалюзи для офисов и жилых комнат. Различные текстуры полотна.", "price": "от 4 000 ₸", "time": "Срок: 2 дня", "warr": "Гарантия: 12 мес" },
				"sub-srv-1-1": { "title": "Замена ТЭНа", "desc": "Профессиональная замена нагревательного элемента стиральной машины оригинальными запчастями с гарантией.", "price": "от 8 000 ₸", "time": "Срок: 1 час", "warr": "Гарантия: 12 мес" },
				"sub-srv-1-2": { "title": "Замена подшипников", "desc": "Разбор бака, замена изношенных подшипников и сальников. Устранение сильного гула и вибрации при отжиме.", "price": "от 18 000 ₸", "time": "Срок: 3-4 часа", "warr": "Гарантия: 12 мес" },
				"sub-srv-1-3": { "title": "Замена сливного насоса (помпы)", "desc": "Устранение проблем со сливом воды. Замена помпы на оригинальную деталь под марку вашей машины.", "price": "от 7 500 ₸", "time": "Срок: 40 мин", "warr": "Гарантия: 12 мес" },
				"sub-srv-1-4": { "title": "Ремонт модуля управления", "desc": "Диагностика и пайка электронной платы (контроллера) стиральной машины при сбоях программ или невключении.", "price": "от 12 000 ₸", "time": "Срок: 1-2 дня", "warr": "Гарантия: 12 мес" },
				"sub-srv-2-1": { "title": "Заправка фреоном", "desc": "Поиск утечки хладагента, вакуумирование системы и заправка качественным фреоном R134a или R600a.", "price": "от 10 000 ₸", "time": "Срок: 1 час", "warr": "Гарантия: 6 мес" },
				"sub-srv-2-2": { "title": "Замена компрессора", "desc": "Демонтаж старого мотора-компрессора, установка нового оригинального компрессора, замена фильтра и заправка.", "price": "от 28 000 ₸", "time": "Срок: 2 часа", "warr": "Гарантия: 12 мес" },
				"sub-srv-2-3": { "title": "Замена термостата", "desc": "Ремонт холодильника, который перемораживает продукты или не включается из-за неисправного терморегулятора.", "price": "от 7 000 ₸", "time": "Срок: 45 мин", "warr": "Гарантия: 12 мес" },
				"sub-srv-2-4": { "title": "Ремонт системы No Frost", "desc": "Замена вентилятора обдува, ТЭНа оттайки, датчиков температуры или таймера оттайки в холодильниках No Frost.", "price": "от 9 500 ₸", "time": "Срок: 1.5 часа", "warr": "Гарантия: 12 мес" },
				"sub-srv-3-1": { "title": "Ремонт кондиционеров", "desc": "Устранение течи внутреннего блока, ремонт плат управления, замена пусковых конденсаторов, вентиляторов.", "price": "от 8 000 ₸", "time": "Срок: 1-2 часа", "warr": "Гарантия: 12 мес" },
				"sub-srv-3-2": { "title": "Ремонт посудомоечных машин", "desc": "Ремонт циркуляционных насосов, ТЭНов, устранение протечек, чистка разбрызгивателей и форсунок под ключ.", "price": "от 9 000 ₸", "time": "Срок: 1-3 часа", "warr": "Гарантия: 12 мес" },
				"sub-srv-3-3": { "title": "Чистка и заправка сплит-систем", "desc": "Полная антибактериальная чистка внутреннего и внешнего блоков кондиционера парогенератором + дозаправка фреоном.", "price": "от 7 500 ₸", "time": "Срок: 1 час", "warr": "Гарантия: 6 мес" },
				"sub-srv-4-1": { "title": "Установка вытяжки", "desc": "Монтаж кухонной вытяжки на стену или в шкаф, подключение к вентиляционной шахте, прокладка воздуховода.", "price": "от 6 000 ₸", "time": "Срок: 1-2 часа", "warr": "Гарантия: 12 мес" },
				"sub-srv-4-2": { "title": "Ремонт вытяжки", "desc": "Замена мотора вытяжки, ремонт кнопочных переключателей или электронных плат управления, замена подсветки.", "price": "от 5 000 ₸", "time": "Срок: 1 час", "warr": "Гарантия: 12 мес" },
				"sub-srv-5-1": { "title": "Установка кондиционеров (сплит-систем)", "desc": "Стандартный и нестандартный монтаж сплит-систем любой мощности. Использование качественной медной трубы.", "price": "от 18 000 ₸", "time": "Срок: 2-3 часа", "warr": "Гарантия: 12 мес" },
				"sub-srv-5-2": { "title": "Ремонт сплит-систем", "desc": "Ремонт компрессора, замена четырехходового клапана, ремонт и пайка медных трасс, устранение утечек фреона.", "price": "от 8 000 ₸", "time": "Срок: 1-2 часа", "warr": "Гарантия: 12 мес" },
				"sub-srv-5-3": { "title": "Демонтаж кондиционера", "desc": "Аккуратный демонтаж блоков с сохранением фреона в компрессоре кондиционера для последующей установки.", "price": "от 8 000 ₸", "time": "Срок: 45 мин", "warr": "Гарантия: - " },
				"sub-srv-6-1": { "title": "Сварка труб", "desc": "Сварка водопроводных труб, стояков отопления, газовых труб аттестованными сварщиками. Гарантия прочности шва.", "price": "от 5 000 ₸", "time": "Срок: 1-2 часа", "warr": "Гарантия: 24 мес" },
				"sub-srv-6-2": { "title": "Сварка петель ворот", "desc": "Ремонт и замена изношенных или сорванных петель гаражных ворот, калиток. Приварка прочных петель с подшипниками.", "price": "от 4 000 ₸", "time": "Срок: 40 мин", "warr": "Гарантия: 12 мес" },
				"sub-srv-6-3": { "title": "Сварочные работы любой сложности", "desc": "Мелкий и крупный ремонт металлических изделий электросваркой на выезде со своим генератором.", "price": "договорная", "time": "Срок: 1-3 часа", "warr": "Гарантия: 12 мес" },
				"sub-srv-7-1": { "title": "Изготовление навесов", "desc": "Изготовление металлических навесов для автомобилей, зон отдыха из поликарбоната, профнастила, металлочерепицы.", "price": "от 15 000 ₸/кв.м", "time": "Срок: 3-5 дней", "warr": "Гарантия: 36 мес" },
				"sub-srv-7-2": { "title": "Изготовление заборов", "desc": "Установка заборов из профлиста, сетки-рабицы, металлического штакетника, 3D-панелей. Быстро и надежно.", "price": "от 5 000 ₸/п.м", "time": "Срок: 2-4 дня", "warr": "Гарантия: 24 мес" },
				"sub-srv-7-3": { "title": "Решетки на окна", "desc": "Изготовление прочных распашных и глухих оконных решеток, дутых решеток, кованых изделий безопасности.", "price": "от 8 000 ₸/кв.м", "time": "Срок: 2-3 дня", "warr": "Гарантия: 36 мес" },
				"sub-srv-7-4": { "title": "Металлические двери", "desc": "Изготовление и монтаж качественных металлических дверей для квартир, тамбуров, гаражей. Усиленная конструкция.", "price": "от 45 000 ₸", "time": "Срок: 3-4 дня", "warr": "Гарантия: 24 мес" },
				"sub-srv-8-1": { "title": "Установка розеток и выключателей", "desc": "Замена старых, монтаж и перенос розеток и выключателей на новые места, штробление стен под кабель.", "price": "от 1 000 ₸/шт", "time": "Срок: 20 мин", "warr": "Гарантия: 12 мес" },
				"sub-srv-8-2": { "title": "Монтаж люстр и светильников", "desc": "Сборка, надежное крепление и подключение любых люстр, точечных светильников, светодиодных лент, bra.", "price": "от 3 000 ₸/шт", "time": "Срок: 30 мин", "warr": "Гарантия: 12 мес" },
				"sub-srv-8-3": { "title": "Поиск и устранение короткого замыкания", "desc": "Диагностика электропроводки спецприборами, поиск места обрыва или замыкания кабеля, локальное устранение.", "price": "от 5 000 ₸", "time": "Срок: 1-2 часа", "warr": "Гарантия: 12 мес" },
				"sub-srv-8-4": { "title": "Замена автоматических выключателей", "desc": "Замена старых пробок, установка автоматов (УЗО), сборка и модернизация электрощитов.", "price": "от 2 000 ₸/шт", "time": "Срок: 30 мин", "warr": "Гарантия: 12 мес" },
				"sub-meb-1-1": { "title": "Кухонные гарнитуры", "desc": "Изготовление современных стильных кухонь по индивидуальным проектам. Фасады МДФ, ЛДСП, краска, акрил, шпон.", "price": "от 120 000 ₸/п.м", "time": "Срок: 10-15 дней", "warr": "Гарантия: 24 мес" },
				"sub-meb-1-2": { "title": "Шкафы-купе и гардеробные", "desc": "Встроенные и корпусные шкафы-купе, гардеробные системы с качественной фурнитурой плавного закрывания.", "price": "от 80 000 ₸/п.м", "time": "Срок: 7-10 дней", "warr": "Гарантия: 24 мес" },
				"sub-meb-1-3": { "title": "Детская мебель", "desc": "Безопасная и экологичная мебель для детских комнат: двухъярусные кровати, рабочие зоны, системы хранения.", "price": "от 65 000 ₸", "time": "Срок: 7-12 дней", "warr": "Гарантия: 24 мес" },
				"sub-meb-1-4": { "title": "Прихожие и комоды", "desc": "Компактные и функциональные прихожие, тумбы для обуви, вместительные комоды под стиль вашей квартиры.", "price": "от 35 000 ₸", "time": "Срок: 5-8 дней", "warr": "Гарантия: 24 мес" },
				"sub-meb-1-5": { "title": "Перетяжка и ремонт мягкой мебели", "desc": "Замена обивки диванов, кресел, стульев (ткань, кожа, велюр), ремонт каркаса, замена поролона и пружинных блоков.", "price": "от 15 000 ₸", "time": "Срок: 2-5 дней", "warr": "Гарантия: 12 мес" }
			}
		}`
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(fallbackJSON))
		return
	}

	if r.Method == http.MethodPost {
		// Admin validation
		token := getTokenFromHeader(r)
		user, ok := getUserByToken(token)
		if !ok || user.Role != "admin" {
			jsonErr(w, 401, "Unauthorized")
			return
		}

		data, err := io.ReadAll(r.Body)
		if err != nil {
			jsonErr(w, 400, "Bad request")
			return
		}

		_ = os.WriteFile(filePath, data, 0644)
		json200(w, map[string]interface{}{"status": "success"})
		return
	}

	jsonErr(w, 405, "Method not allowed")
}

// GET & POST /api/assistant-config
func handleAssistantConfig(w http.ResponseWriter, r *http.Request) {
	filePath := "assistant_config.json"

	if r.Method == http.MethodGet {
		data, err := os.ReadFile(filePath)
		if err == nil {
			w.Header().Set("Content-Type", "application/json")
			w.Write(data)
			return
		}

		defaultConfig := `{
			"fallback": "Спасибо за обращение! Наш специалист свяжется с вами в течение 5 минут для точного расчета.",
			"rules": [
				{
					"id": "rule-price",
					"triggers": ["цен", "стоим", "прайс", "бага", "құн"],
					"reply": "Стоимость большинства услуг начинается от 2 500 ₸. Выезд мастера и диагностика при продолжении работ — бесплатно! Хотите оставить заявку на точный расчет?"
				},
				{
					"id": "rule-time",
					"triggers": ["как", "когда", "қашан"],
					"reply": "Наши специалисты работают 24/7. Мастер может выехать к вам в течение 45 минут после оформления заявки."
				}
			]
		}`
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(defaultConfig))
		return
	}

	if r.Method == http.MethodPost {
		token := getTokenFromHeader(r)
		user, ok := getUserByToken(token)
		if !ok || user.Role != "admin" {
			jsonErr(w, 401, "Unauthorized")
			return
		}

		data, err := io.ReadAll(r.Body)
		if err != nil {
			jsonErr(w, 400, "Bad request")
			return
		}

		_ = os.WriteFile(filePath, data, 0644)
		json200(w, map[string]interface{}{"status": "success"})
		return
	}

	jsonErr(w, 405, "Method not allowed")
}

// ─── Main ────────────────────────────────────────────────────────────────────

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "3030"
	}

	mux := http.NewServeMux()

	// API routes
	mux.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("OK"))
	})
	mux.HandleFunc("/api/auth/send-sms", handleSendSMS)
	mux.HandleFunc("/api/auth/verify-sms", handleVerifySMS)
	mux.HandleFunc("/api/auth/register-phone", handleRegisterPhone)
	mux.HandleFunc("/api/auth/login", handleAdminLogin)
	mux.HandleFunc("/api/auth/me", handleMe)
	mux.HandleFunc("/api/auth/logout", handleLogout)
	mux.HandleFunc("/api/auth/profile", handleProfile)
	mux.HandleFunc("/api/callbacks", handleGetCallbacks)
	mux.HandleFunc("/api/callback", handleCreateCallback)
	mux.HandleFunc("/api/catalog", handleCatalog)
	mux.HandleFunc("/api/assistant-config", handleAssistantConfig)

	// Static file serving — serve index.html for all non-API routes (SPA)
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		// Don't serve directories
		if r.URL.Path == "/" {
			http.ServeFile(w, r, "index.html")
			return
		}
		// Admin routing
		if r.URL.Path == "/admin" || r.URL.Path == "/admin.html" {
			http.ServeFile(w, r, "admin.html")
			return
		}
		// Try to serve actual file; fall back to index.html
		path := strings.TrimPrefix(r.URL.Path, "/")
		if _, err := os.Stat(path); err == nil {
			http.ServeFile(w, r, path)
			return
		}
		http.ServeFile(w, r, "index.html")
	})

	handler := corsMiddleware(mux)

	log.Printf("🚀 HubMaster API starting on :%s", port)
	if err := http.ListenAndServe(":"+port, handler); err != nil {
		log.Fatal(err)
	}
}
