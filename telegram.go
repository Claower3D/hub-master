package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strconv"
	"time"
	"regexp"
	"strings"
)

const tgAPIBase = "https://api.telegram.org/bot"

type tgMessage struct {
	MessageID int `json:"message_id"`
	From      struct {
		ID        int64  `json:"id"`
		FirstName string `json:"first_name"`
		LastName  string `json:"last_name"`
		Username  string `json:"username"`
	} `json:"from"`
	Chat struct {
		ID int64 `json:"id"`
	} `json:"chat"`
	Text           string     `json:"text"`
	ReplyToMessage *tgMessage `json:"reply_to_message"`
}

type tgUpdate struct {
	UpdateID int       `json:"update_id"`
	Message  tgMessage `json:"message"`
}

type tgUpdatesResponse struct {
	OK     bool       `json:"ok"`
	Result []tgUpdate `json:"result"`
}

func tgToken() string {
	if t := os.Getenv("TELEGRAM_BOT_TOKEN"); t != "" {
		return t
	}
	return "8837427955:AAH9tieG7RrxQKr2YJpNmglr58U1oJe9lOs"
}

func tgSendMessage(chatID int64, text string) {
	token := tgToken()
	url := fmt.Sprintf("%s%s/sendMessage", tgAPIBase, token)
	body, _ := json.Marshal(map[string]interface{}{
		"chat_id":    chatID,
		"text":       text,
		"parse_mode": "HTML",
	})
	resp, err := http.Post(url, "application/json", bytes.NewReader(body))
	if err != nil {
		log.Printf("⚠️ Telegram send error: %v", err)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		respBody, _ := io.ReadAll(resp.Body)
		log.Printf("⚠️ Telegram API returned status %d: %s", resp.StatusCode, string(respBody))
	}
}

// NotifyNewOrder sends a notification about a new order to all Telegram subscribers
func NotifyNewOrder(db DB, record *CallbackRecord) {
	log.Printf("📤 [Telegram] Processing new order #%d for notifications...", record.ID)
	subscribers, err := db.GetTelegramSubscribers()
	if err != nil {
		log.Printf("⚠️ [Telegram] Error fetching subscribers: %v", err)
		subscribers = []int64{}
	}

	// Check if a global chat ID is configured via environment variable
	if globalChatStr := os.Getenv("TELEGRAM_CHAT_ID"); globalChatStr != "" {
		if globalChatID, parseErr := strconv.ParseInt(globalChatStr, 10, 64); parseErr == nil {
			// Append to subscribers if not already present
			exists := false
			for _, id := range subscribers {
				if id == globalChatID {
					exists = true
					break
				}
			}
			if !exists {
				subscribers = append(subscribers, globalChatID)
				log.Printf("📢 [Telegram] Added global chat ID from TELEGRAM_CHAT_ID env: %d", globalChatID)
			}
		} else {
			log.Printf("⚠️ [Telegram] Invalid TELEGRAM_CHAT_ID env value: %s", globalChatStr)
		}
	}

	if len(subscribers) == 0 {
		log.Printf("⚠️ [Telegram] No subscribers or global TELEGRAM_CHAT_ID configured. Order notification #%d not sent. To receive notifications, start the bot with /start or set TELEGRAM_CHAT_ID env variable.", record.ID)
		return
	}

	var sb strings.Builder
	sb.WriteString("🌐 <b>HUB MASTER — Новая заявка с сайта</b>\n")
	sb.WriteString("━━━━━━━━━━━━━━━━━━━━\n")
	sb.WriteString(fmt.Sprintf("🔔 <b>Заявка #%d</b>\n\n", record.ID))

	name := strings.TrimSpace(record.Name)
	if name != "" && name != "не указано" {
		sb.WriteString(fmt.Sprintf("👤 <b>Имя:</b> %s\n", name))
	}
	phone := strings.TrimSpace(record.Phone)
	if phone != "" && phone != "не указано" {
		sb.WriteString(fmt.Sprintf("📞 <b>Телефон:</b> %s\n", phone))
	}
	service := strings.TrimSpace(record.Service)
	if service != "" && service != "не указано" {
		sb.WriteString(fmt.Sprintf("🛠 <b>Услуга:</b> %s\n", service))
	}
	city := strings.TrimSpace(record.City)
	if city != "" && city != "не указано" {
		sb.WriteString(fmt.Sprintf("🏙 <b>Город:</b> %s\n", city))
	}
	address := strings.TrimSpace(record.Address)
	if address != "" && address != "не указано" {
		sb.WriteString(fmt.Sprintf("📍 <b>Адрес:</b> %s\n", address))
	}
	comment := strings.TrimSpace(record.Comment)
	if comment != "" && comment != "не указано" {
		sb.WriteString(fmt.Sprintf("💬 <b>Описание/Проблема:</b> %s\n", comment))
	}

	sb.WriteString(fmt.Sprintf("🕐 <b>Время:</b> %s\n", record.CreatedAt.Format("02.01.2006 15:04")))
	sb.WriteString("━━━━━━━━━━━━━━━━━━━━\n")
	sb.WriteString("🔗 <i>master-hub-production.up.railway.app</i>")

	msg := sb.String()

	log.Printf("📤 [Telegram] Sending order #%d notification to %d subscribers...", record.ID, len(subscribers))
	for _, chatID := range subscribers {
		tgSendMessage(chatID, msg)
		log.Printf("✅ [Telegram] Sent notification to chat %d", chatID)
	}
}

// StartTelegramBot starts the bot polling loop in a goroutine
func StartTelegramBot(db DB) {
	token := tgToken()
	if token == "" {
		log.Println("⚠️ TELEGRAM_BOT_TOKEN not set, skipping bot")
		return
	}
	log.Println("🤖 Starting Telegram bot polling...")
	go func() {
		offset := 0
		for {
			updates, err := tgGetUpdates(token, offset)
			if err != nil {
				log.Printf("⚠️ Telegram polling error: %v", err)
				time.Sleep(5 * time.Second)
				continue
			}
			for _, upd := range updates {
				offset = upd.UpdateID + 1
				handleTgUpdate(db, upd)
			}
			if len(updates) == 0 {
				time.Sleep(1 * time.Second)
			}
		}
	}()
}

// tgGetUpdates fetches new Telegram messages
func tgGetUpdates(token string, offset int) ([]tgUpdate, error) {
	url := fmt.Sprintf("%s%s/getUpdates?timeout=30&offset=%d", tgAPIBase, token, offset)
	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	data, _ := io.ReadAll(resp.Body)
	var result tgUpdatesResponse
	if err := json.Unmarshal(data, &result); err != nil {
		return nil, err
	}
	if !result.OK {
		return nil, fmt.Errorf("telegram API returned not OK")
	}
	return result.Result, nil
}

func handleTgUpdate(db DB, upd tgUpdate) {
	if upd.Message.MessageID == 0 {
		return
	}

	chatID := upd.Message.Chat.ID
	text := upd.Message.Text
	firstName := upd.Message.From.FirstName

	// Обработка ответа '+' на уведомление о заявке
	if upd.Message.ReplyToMessage != nil && strings.TrimSpace(text) == "+" {
		re := regexp.MustCompile(`#(\d+)`)
		matches := re.FindStringSubmatch(upd.Message.ReplyToMessage.Text)
		if len(matches) > 1 {
			orderID := matches[1]
			orderIDInt, err := strconv.Atoi(orderID)
			if err == nil {
				if errDb := db.UpdateCallbackStatus(orderIDInt, "in_progress"); errDb != nil {
					log.Printf("⚠️ Ошибка обновления статуса для заявки %d: %v", orderIDInt, errDb)
					tgSendMessage(chatID, fmt.Sprintf("⚠️ Заявка #%s найдена, но не удалось обновить её статус в базе.", orderID))
					return
				}
				subscribers, errSub := db.GetTelegramSubscribers()
				msg := fmt.Sprintf("✅ Оператор %s принял заявку #%s. Статус обновлен на «В обработке».", firstName, orderID)
				
				sentToCurrent := false
				if errSub == nil {
					for _, subChatID := range subscribers {
						tgSendMessage(subChatID, msg)
						if subChatID == chatID {
							sentToCurrent = true
						}
					}
				}
				if !sentToCurrent {
					tgSendMessage(chatID, msg)
				}
				return
			}
		}
	}

	switch text {
	case "/start":
		name := firstName
		if name == "" {
			name = fmt.Sprintf("user_%d", chatID)
		}
		err := db.AddTelegramSubscriber(chatID, name)
		if err != nil {
			tgSendMessage(chatID, "❌ Ошибка подписки, попробуйте позже.")
			return
		}
		tgSendMessage(chatID, fmt.Sprintf(
			"✅ <b>Привет, %s!</b>\n\nВы подписаны на уведомления о новых заявках HUB MASTER.\n\n"+
				"📋 Команды:\n/start — подписаться\n/stop — отписаться",
			name,
		))
	case "/stop":
		_ = db.RemoveTelegramSubscriber(chatID)
		tgSendMessage(chatID, "🔕 Вы отписались от уведомлений.\nЧтобы подписаться снова — отправьте /start")
	default:
		tgSendMessage(chatID, "📋 Команды:\n/start — подписаться на уведомления\n/stop — отписаться")
	}
}
