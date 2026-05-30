package main

import (
	"crypto/rand"
	"encoding/json"
	"fmt"
	"log"
	"math/big"
	"net/http"
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
	users    = map[int]User{}          // id → User
	phones   = map[string]int{}        // phone → userID
	sessions = map[string]Session{}    // token → Session
	callbacks []Callback
	nextUserID = 1
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

	// Try Twilio if env vars set
	twilioSID := os.Getenv("TWILIO_ACCOUNT_SID")
	twilioToken := os.Getenv("TWILIO_AUTH_TOKEN")
	twilioFrom := os.Getenv("TWILIO_FROM")

	demoCode := ""
	if twilioSID == "" || twilioToken == "" || twilioFrom == "" {
		// Demo mode: return code in response
		demoCode = code
		log.Printf("[SMS] Demo mode — no Twilio configured. Code: %s", code)
	} else {
		// Send via Twilio REST
		err := sendTwilioSMS(twilioSID, twilioToken, twilioFrom, req.Phone,
			fmt.Sprintf("Ваш код HubMaster: %s", code))
		if err != nil {
			log.Printf("[SMS] Twilio error: %v", err)
			// Fall back to demo mode
			demoCode = code
		}
	}

	resp := map[string]interface{}{"ok": true}
	if demoCode != "" {
		resp["demo_code"] = demoCode
	}
	json200(w, resp)
}

func sendTwilioSMS(sid, token, from, to, body string) error {
	v := strings.NewReader(fmt.Sprintf("To=%s&From=%s&Body=%s",
		urlEncode(to), urlEncode(from), urlEncode(body)))
	req, _ := http.NewRequest("POST",
		fmt.Sprintf("https://api.twilio.com/2010-04-01/Accounts/%s/Messages.json", sid), v)
	req.SetBasicAuth(sid, token)
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	if resp.StatusCode >= 400 {
		return fmt.Errorf("twilio status %d", resp.StatusCode)
	}
	return nil
}

func urlEncode(s string) string {
	return strings.ReplaceAll(strings.ReplaceAll(
		strings.ReplaceAll(s, "%", "%25"),
		"+", "%2B"), " ", "+")
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

// ─── Main ────────────────────────────────────────────────────────────────────

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "3030"
	}

	mux := http.NewServeMux()

	// API routes
	mux.HandleFunc("/api/auth/send-sms", handleSendSMS)
	mux.HandleFunc("/api/auth/verify-sms", handleVerifySMS)
	mux.HandleFunc("/api/auth/register-phone", handleRegisterPhone)
	mux.HandleFunc("/api/auth/me", handleMe)
	mux.HandleFunc("/api/auth/logout", handleLogout)
	mux.HandleFunc("/api/auth/profile", handleProfile)
	mux.HandleFunc("/api/callbacks", handleGetCallbacks)
	mux.HandleFunc("/api/callback", handleCreateCallback)

	// Static file serving — serve index.html for all non-API routes (SPA)
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		// Don't serve directories
		if r.URL.Path == "/" {
			http.ServeFile(w, r, "index.html")
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
