package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"compress/gzip"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"regexp"
	"time"

	"golang.org/x/crypto/bcrypt"
)

// CallbackRequest represents the incoming callback form data
type CallbackRequest struct {
	Name    string `json:"name"`
	Phone   string `json:"phone"`
	Service string `json:"service"`
	City    string `json:"city"`
	Address string `json:"address"`
	Comment string `json:"comment"`
}

// APIUser represents a user profile safe to send in JSON responses to the frontend client
type APIUser struct {
	ID        int       `json:"id"`
	Name      string    `json:"name"`
	Email     string    `json:"email"`
	Phone     string    `json:"phone"`
	City      string    `json:"city"`
	Bonuses   int       `json:"bonuses"`
	Role      string    `json:"role"`
	CreatedAt time.Time `json:"created_at"`
}

func ToAPIUser(u *User) APIUser {
	if u == nil {
		return APIUser{}
	}
	return APIUser{
		ID:        u.ID,
		Name:      u.Name,
		Email:     u.Email,
		Phone:     u.Phone,
		City:      u.City,
		Bonuses:   u.Bonuses,
		Role:      u.Role,
		CreatedAt: u.CreatedAt,
	}
}

// CallbackResponse represents the API response for callback submission
type CallbackResponse struct {
	Status  string          `json:"status"`
	Message string          `json:"message"`
	Record  *CallbackRecord `json:"record,omitempty"`
}

// StatItem represents a company statistic
type StatItem struct {
	Num   string `json:"num"`
	Label string `json:"label"`
}

// ReviewItem represents a client review
type ReviewItem struct {
	Text   string `json:"text"`
	Author string `json:"author"`
}

// ServiceCategory represents a service category in the catalog
type ServiceCategory struct {
	ID    string `json:"id"`
	Title string `json:"title"`
	Icon  string `json:"icon"`
}

// Global database instance
var dbInstance DB

func resolvePath(p string) string {
	if _, err := os.Stat(p); os.IsNotExist(err) {
		if _, err := os.Stat("../" + p); err == nil {
			return "../" + p
		}
	}
	return p
}

// syncSystemFiles copies essential files from system_public/ to public/ 
// to bypass persistent volume cache issues and repair corrupted templates.
func syncSystemFiles() {
	filesToSync := []string{"builder.html"}
	
	for _, f := range filesToSync {
		src := filepath.Join("system_public", f)
		dst := filepath.Join("public", f)
		
		srcInfo, err := os.Stat(src)
		if err != nil {
			continue // Skip if system_public file doesn't exist
		}
		
		needsCopy := false
		
		if f == "builder.html" {
			// Always copy builder.html if the one in public is older or missing
			dstInfo, err := os.Stat(dst)
			if err != nil || dstInfo.ModTime().Before(srcInfo.ModTime()) {
				needsCopy = true
			}
		}
		
		if needsCopy {
			log.Printf("syncSystemFiles: Copying %s to public/", f)
			srcData, err := os.ReadFile(src)
			if err == nil {
				os.WriteFile(dst, srcData, 0644)
			}
		}
	}

	// Repair corrupted templates on persistent volume
	templates := []string{"template1.html", "template2.html", "index.html"}
	badScriptRegex := regexp.MustCompile(`(?s)[ \t]*<script>window\.builderCustomCatalogStyles = \{.*?\};</script>\s*</body>`)
	
	for _, t := range templates {
		dst := filepath.Join("public", t)
		content, err := os.ReadFile(dst)
		if err == nil {
			if badScriptRegex.Match(content) {
				log.Printf("syncSystemFiles: Repairing corrupted %s", t)
				cleaned := badScriptRegex.ReplaceAll(content, []byte("\n</body>"))
				os.WriteFile(dst, cleaned, 0644)
			}
		}
	}
}


func main() {
	syncSystemFiles()
	
	var err error
	dbInstance, err = InitDB()
	if err != nil {
		log.Fatalf("❌ Failed to initialize database: %v", err)
	}
	defer dbInstance.Close()

	// Sync catalog from JSON to DB on startup if database catalog is empty or has old/incomplete schema
	dbCatalog, dbErr := dbInstance.GetCatalog()
	hasNewSchema := dbErr == nil && dbCatalog != "" && strings.Contains(dbCatalog, "windows")


	if !hasNewSchema {
		log.Println("🔄 Database catalog is empty or has old schema. Initializing from catalog_data.json...")
		catData, catErr := os.ReadFile("catalog_data.json")
		if catErr == nil {
			dbInstance.SaveCatalog(string(catData))
		} else {
			catData, catErr = os.ReadFile("../catalog_data.json")
			if catErr == nil {
				dbInstance.SaveCatalog(string(catData))
			}
		}
	} else {
		log.Println("✅ Database catalog is already initialized with new schema. Skipping overwrite.")
	}

	// Serve Static Files from dist / root directory (needed for deployment)
	staticDir := "."
	if _, err := os.Stat("public/index.html"); err == nil {
		staticDir = "public"
	} else if _, err := os.Stat("index.html"); err == nil {
		staticDir = "."
	} else if _, err := os.Stat("../public/index.html"); err == nil {
		staticDir = "../public"
	} else if _, err := os.Stat("../index.html"); err == nil {
		staticDir = "../"
	}

	// Start Telegram bot notifications
	StartTelegramBot(dbInstance)

	mux := http.NewServeMux()

	// Add debugging endpoint
	mux.HandleFunc("/api/db-status", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		dbType := "Unknown"
		if _, ok := dbInstance.(*PostgresDB); ok {
			dbType = "PostgreSQL"
		} else if _, ok := dbInstance.(*JsonDB); ok {
			dbType = "JSON (Local File)"
		}
		
		catDataRaw, _ := dbInstance.GetCatalog()
		hasNewSch := len(catDataRaw) > 0 && strings.Contains(catDataRaw, "windows")
		
		status := map[string]interface{}{
			"database_type": dbType,
			"has_new_schema": hasNewSch,
			"catalog_length": len(catDataRaw),
			"database_url_set": os.Getenv("DATABASE_URL") != "",
		}
		json.NewEncoder(w).Encode(status)
	}))


	// Health check endpoint
	mux.HandleFunc("/api/health", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte(`{"status":"ok"}`))
	}))

	// Upload endpoint
	mux.HandleFunc("/api/upload", corsMiddleware(handleUpload(dbInstance, staticDir)))

	// Stats endpoint
	mux.HandleFunc("/api/stats", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		stats := []StatItem{
			{Num: "50 000+", Label: "выполненных заказов"},
			{Num: "100+", Label: "видов услуг"},
			{Num: "4.9★", Label: "средняя оценка"},
			{Num: "12 мес", Label: "гарантия"},
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(stats)
	}))

	// Services catalog endpoint
	mux.HandleFunc("/api/services", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		categories := []ServiceCategory{
			{ID: "remont-tehniki", Title: "Ремонт техники", Icon: "ri-home-gear-line"},
			{ID: "transport", Title: "Транспорт", Icon: "ri-roadster-line"},
			{ID: "bytovye-uslugi", Title: "Бытовые услуги", Icon: "ri-sparkling-line"},
			{ID: "specialist", Title: "Специалисты", Icon: "ri-user-star-line"},
			{ID: "stroitelstvo-i-remont", Title: "Строительство", Icon: "ri-building-line"},
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(categories)
	}))

	// Dynamic catalog configuration (GET /api/catalog, POST /api/catalog)
	mux.HandleFunc("/api/catalog", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodOptions {
			return
		}

		filePath := "catalog_data.json"

		if r.Method == http.MethodGet {
			w.Header().Set("Content-Type", "application/json")

			// Check database first
			dbCatalog, err := dbInstance.GetCatalog()
			if err == nil && dbCatalog != "" {
				w.Write([]byte(dbCatalog))
				return
			}

			// Fallback to catalog file if exists
			data, err := os.ReadFile(filePath)
			if err == nil {
				w.Write(data)
				return
			}

			// Return fallback default JSON from code (matching App.jsx default setup)
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
						{ "id": "sub-okna-3-3", "title": "Замена уплонтителей" },
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
					"sub-okna-1-3": { "title": "Сетки Антипыль", "desc": "Специальное мелкоячеистое полотно, задерживающее даже мельчайшую пыльцу и споры растений. Идеяльно для аллергиков.", "price": "от 8 500 ₸", "time": "Установка: 30 мин", "warr": "Гарантия: 12 мес" },
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
					"sub-srv-8-2": { "title": "Монтаж люстр и светильников", "desc": "Сборка, надежное крепление и подключение любых люстр, точечных светильников, светодиодных лент, бра.", "price": "от 3 000 ₸/шт", "time": "Срок: 30 мин", "warr": "Гарантия: 12 мес" },
					"sub-srv-8-3": { "title": "Поиск и устранение короткого замыкания", "desc": "Диагностика электропроводки спецприборами, поиск места обрыва или замыкания кабеля, локальное устранение.", "price": "от 5 000 ₸", "time": "Срок: 1-2 часа", "warr": "Гарантия: 12 мес" },
					"sub-srv-8-4": { "title": "Замена автоматических выключателей", "desc": "Замена старых пробок, установка автоматов (УЗО), сборка и модернизация электрощитов.", "price": "от 2 000 ₸/шт", "time": "Срок: 30 мин", "warr": "Гарантия: 12 мес" },
					"sub-meb-1-1": { "title": "Кухонные гарнитуры", "desc": "Изготовление современных стильных кухонь по индивидуальным проектам. Фасады МДФ, ЛДСП, краска, акрил, шпон.", "price": "от 120 000 ₸/п.м", "time": "Срок: 10-15 дней", "warr": "Гарантия: 24 мес" },
					"sub-meb-1-2": { "title": "Шкафы-купе и гардеробные", "desc": "Встроенные и корпусные шкафы-купе, гардеробные системы с качественной фурнитурой плавного закрывания.", "price": "от 80 000 ₸/п.м", "time": "Срок: 7-10 дней", "warr": "Гарантия: 24 мес" },
					"sub-meb-1-3": { "title": "Детская мебель", "desc": "Безопасная и экологичная мебель для детских комнат: двухъярусные кровати, рабочие зоны, системы хранения.", "price": "от 65 000 ₸", "time": "Срок: 7-12 дней", "warr": "Гарантия: 24 мес" },
					"sub-meb-1-4": { "title": "Прихожие и комоды", "desc": "Компактные и функциональные прихожие, тумбы для обуви, вместительные комоды под стиль вашей квартиры.", "price": "от 35 000 ₸", "time": "Срок: 5-8 дней", "warr": "Гарантия: 24 мес" },
					"sub-meb-1-5": { "title": "Перетяжка и ремонт мягкой мебели", "desc": "Замена обивки диванов, кресел, стульев (ткань, кожа, велюр), ремонт каркаса, замена поролона и пружинных блоков.", "price": "от 15 000 ₸", "time": "Срок: 2-5 дней", "warr": "Гарантия: 12 мес" }
				}
			}`
			w.Write([]byte(fallbackJSON))
		} else if r.Method == http.MethodPost {
			// Admin check
			authHeader := r.Header.Get("Authorization")
			if !strings.HasPrefix(authHeader, "Bearer ") {
				http.Error(w, "Unauthorized", http.StatusUnauthorized)
				return
			}
			token := strings.TrimPrefix(authHeader, "Bearer ")
			sess, err := dbInstance.GetSession(token)
			if err != nil {
				http.Error(w, "Unauthorized", http.StatusUnauthorized)
				return
			}
			user, err := dbInstance.GetUserByID(sess.UserID)
			if err != nil || user.Role != "admin" {
				http.Error(w, "Forbidden", http.StatusForbidden)
				return
			}

			// Save JSON body to database and file
			data, err := io.ReadAll(r.Body)
			if err != nil {
				http.Error(w, "Bad request", http.StatusBadRequest)
				return
			}

			// Save to database
			err = dbInstance.SaveCatalog(string(data))
			if err != nil {
				log.Printf("⚠️ Failed to save catalog to database: %v\n", err)
			}

			// Save to file (as local copy/fallback)
			_ = os.WriteFile(filePath, data, 0644)

			// Git push removed to prevent Railway from redeploying constantly

			w.Header().Set("Content-Type", "application/json")
			w.Write([]byte(`{"status":"success"}`))
		} else {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		}
	}))

	// Assistant configuration (GET /api/assistant-config, POST /api/assistant-config)
	mux.HandleFunc("/api/assistant-config", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodOptions {
			return
		}

		filePath := "assistant_config.json"

		if r.Method == http.MethodGet {
			w.Header().Set("Content-Type", "application/json")
			data, err := os.ReadFile(filePath)
			if err == nil {
				w.Write(data)
				return
			}

			// Return default configuration if file doesn't exist
			defaultConfig := `{
				"fallback": "Спасибо за обращение! Наш специалист свяжется с вами в течение 5 минут для точного расчета.",
				"rules": [
					{
						"id": "rule-price",
						"triggers": ["цен", "стоим", "прайс", "бага", "кун"],
						"reply": "Стоимость большинства услуг начинается от 2 500 Т. Выезд мастера и диагностика при продолжении работ — бесплатно! Хотите оставить заявку на точный расчет?"
					},
					{
						"id": "rule-time",
						"triggers": ["сроч", "быстр", "выезд", "тез", "апат"],
						"reply": "Среднее время прибытия мастера по городу — всего 45 минут! У нас 14 дежурных мастеров онлайн. Оформим срочный выезд?"
					},
					{
						"id": "rule-warranty",
						"triggers": ["гарант", "кепил"],
						"reply": "Мы предоставляем официальную гарантию до 12 месяцев на все виды работ и комплектующие. Выдаем акт выполненных работ!"
					},
					{
						"id": "rule-schedule",
						"triggers": ["график", "работ", "уакыт", "кесте"],
						"reply": "Мы работаем ежедневно, без выходных с 09:00 до 21:00. Готовы принять вашу заявку прямо сейчас!"
					}
				]
			}`
			w.Write([]byte(defaultConfig))
			return
		}

		if r.Method == http.MethodPost {
			authHeader := r.Header.Get("Authorization")
			if authHeader == "" {
				http.Error(w, "Unauthorized", http.StatusUnauthorized)
				return
			}
			token := strings.TrimPrefix(authHeader, "Bearer ")
			sess, err := dbInstance.GetSession(token)
			if err != nil {
				http.Error(w, "Unauthorized", http.StatusUnauthorized)
				return
			}
			user, err := dbInstance.GetUserByID(sess.UserID)
			if err != nil || user.Role != "admin" {
				http.Error(w, "Forbidden", http.StatusForbidden)
				return
			}

			data, err := io.ReadAll(r.Body)
			if err != nil {
				http.Error(w, "Bad request", http.StatusBadRequest)
				return
			}

			err = os.WriteFile(filePath, data, 0644)
			if err != nil {
				http.Error(w, "Failed to save configuration", http.StatusInternalServerError)
				return
			}

			w.Header().Set("Content-Type", "application/json")
			w.Write([]byte(`{"status":"success"}`))
			return
		}

		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
	}))

	// Callback form submission endpoint (supports optional authentication)
	mux.HandleFunc("/api/callback", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodOptions {
			return
		}
		if r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		var req CallbackRequest
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			http.Error(w, "Bad request", http.StatusBadRequest)
			return
		}

		// Optional auth check
		var userID *int
		authHeader := r.Header.Get("Authorization")
		if strings.HasPrefix(authHeader, "Bearer ") {
			token := strings.TrimPrefix(authHeader, "Bearer ")
			sess, err := dbInstance.GetSession(token)
			if err == nil {
				userID = &sess.UserID
			}
		}

		record, err := dbInstance.CreateCallback(req, userID)
		if err != nil {
			log.Printf("Error saving callback: %v\n", err)
			http.Error(w, "Internal server error", http.StatusInternalServerError)
			return
		}

		log.Printf("Новая заявка: Имя: %s, Тел: %s, Услуга: %s, Город: %s, Адрес: %s, Проблема: %s (UserID: %v)\n", req.Name, req.Phone, req.Service, req.City, req.Address, req.Comment, userID)

		// Send Telegram notification to all subscribers
		go NotifyNewOrder(dbInstance, record)

		resp := CallbackResponse{
			Status:  "success",
			Message: "Заявка успешно принята! Оператор свяжется с вами в течение 15 минут.",
			Record:  record,
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(resp)
	}))

	// ---- AUTH ENDPOINTS ----

	// POST /api/auth/send-sms  — send a 4-digit OTP to the given phone
	mux.HandleFunc("/api/auth/send-sms", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		if r.Method == http.MethodOptions {
			return
		}
		if r.Method != http.MethodPost {
			w.WriteHeader(http.StatusMethodNotAllowed)
			json.NewEncoder(w).Encode(map[string]string{"error": "Method not allowed"})
			return
		}

		var input struct {
			Phone string `json:"phone"`
		}
		if err := json.NewDecoder(r.Body).Decode(&input); err != nil || input.Phone == "" {
			w.WriteHeader(http.StatusBadRequest)
			json.NewEncoder(w).Encode(map[string]string{"error": "Укажите номер телефона"})
			return
		}

		code, err := SendVerificationSMS(input.Phone)
		if err != nil {
			log.Printf("⚠️ SMS send error: %v", err)
			w.WriteHeader(http.StatusInternalServerError)
			json.NewEncoder(w).Encode(map[string]string{"error": "Не удалось отправить SMS"})
			return
		}

		// In demo/dev mode return the code in response so frontend can show it
		demoCode := ""
		if smscLogin() == "" {
			demoCode = code
		}

		json.NewEncoder(w).Encode(map[string]interface{}{
			"status":    "sent",
			"demo_code": demoCode, // empty in production
		})
	}))

	// POST /api/auth/verify-sms  — verify OTP and login (or return "new_user" flag)
	mux.HandleFunc("/api/auth/verify-sms", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		if r.Method == http.MethodOptions {
			return
		}
		if r.Method != http.MethodPost {
			w.WriteHeader(http.StatusMethodNotAllowed)
			json.NewEncoder(w).Encode(map[string]string{"error": "Method not allowed"})
			return
		}

		var input struct {
			Phone string `json:"phone"`
			Code  string `json:"code"`
		}
		if err := json.NewDecoder(r.Body).Decode(&input); err != nil || input.Phone == "" || input.Code == "" {
			w.WriteHeader(http.StatusBadRequest)
			json.NewEncoder(w).Encode(map[string]string{"error": "Укажите телефон и код"})
			return
		}

		ok, errMsg := verifySmsCodeStore(input.Phone, input.Code)
		if !ok {
			w.WriteHeader(http.StatusUnauthorized)
			json.NewEncoder(w).Encode(map[string]string{"error": errMsg})
			return
		}

		// Check if user already exists by phone
		user, err := dbInstance.GetUserByPhone(input.Phone)

		if err != nil {
			// New user — front-end should show registration form
			json.NewEncoder(w).Encode(map[string]interface{}{
				"status": "new_user",
				"phone":  input.Phone,
				"token":  "",
				"user":   nil,
			})
			return
		}

		// Existing user — create session
		sess, err := dbInstance.CreateSession(user.ID)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			json.NewEncoder(w).Encode(map[string]string{"error": "Ошибка создания сессии"})
			return
		}

		json.NewEncoder(w).Encode(map[string]interface{}{
			"status": "ok",
			"token":  sess.Token,
			"user":   ToAPIUser(user),
		})
	}))

	// POST /api/auth/register-phone — complete registration after SMS verification
	mux.HandleFunc("/api/auth/register-phone", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")

		if r.Method == http.MethodOptions {
			return
		}
		if r.Method != http.MethodPost {
			w.WriteHeader(http.StatusMethodNotAllowed)
			json.NewEncoder(w).Encode(map[string]string{"error": "Method not allowed"})
			return
		}

		var input struct {
			Phone   string `json:"phone"`
			Name    string `json:"name"`
			Email   string `json:"email"`
			City    string `json:"city"`
			Address string `json:"address"`
		}
		if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
			w.WriteHeader(http.StatusBadRequest)
			json.NewEncoder(w).Encode(map[string]string{"error": "Неверный формат данных"})
			return
		}
		if input.Phone == "" || input.Name == "" {
			w.WriteHeader(http.StatusBadRequest)
			json.NewEncoder(w).Encode(map[string]string{"error": "Номер телефона и имя обязательны"})
			return
		}

		// Email is optional — auto-generate from phone if not provided
		if input.Email == "" {
			cleanPhone := strings.TrimPrefix(input.Phone, "+")
			cleanPhone = strings.ReplaceAll(cleanPhone, " ", "")
			input.Email = "user_" + cleanPhone + "@hubmaster.kz"
		}

		// City defaults to Алматы if not provided
		if input.City == "" {
			input.City = "Алматы"
		}

		// Use phone as default password (user can change later via profile)
		password := input.Phone

		user, err := dbInstance.CreateUser(input.Name, input.Email, input.Phone, input.City, password)
		if err != nil {
			// Maybe already exists — return existing user session
			existingUser, fetchErr := dbInstance.GetUserByPhone(input.Phone)
			if fetchErr == nil {
				user = existingUser
			} else {
				// Return the original CreateUser error as JSON
				w.WriteHeader(http.StatusConflict)
				json.NewEncoder(w).Encode(map[string]string{"error": err.Error()})
				return
			}
		}

		sess, err := dbInstance.CreateSession(user.ID)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			json.NewEncoder(w).Encode(map[string]string{"error": "Ошибка создания сессии"})
			return
		}

		// Store address in user notes (saved via Telegram / admin panel)
		if input.Address != "" {
			log.Printf("📍 Address for user %d (%s): %s", user.ID, input.Phone, input.Address)
		}

		json.NewEncoder(w).Encode(map[string]interface{}{
			"status": "ok",
			"token":  sess.Token,
			"user":   ToAPIUser(user),
		})
	}))

	// POST /api/auth/register

	mux.HandleFunc("/api/auth/register", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodOptions {
			return
		}
		if r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		var input struct {
			Name     string `json:"name"`
			Email    string `json:"email"`
			Phone    string `json:"phone"`
			City     string `json:"city"`
			Password string `json:"password"`
		}
		if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
			http.Error(w, "Bad request", http.StatusBadRequest)
			return
		}

		if input.Name == "" || input.Email == "" || input.Phone == "" || input.City == "" || len(input.Password) < 6 {
			http.Error(w, "Invalid inputs (password must be at least 6 characters)", http.StatusBadRequest)
			return
		}

		user, err := dbInstance.CreateUser(input.Name, input.Email, input.Phone, input.City, input.Password)
		if err != nil {
			http.Error(w, err.Error(), http.StatusConflict)
			return
		}

		sess, err := dbInstance.CreateSession(user.ID)
		if err != nil {
			http.Error(w, "Session creation failed", http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]interface{}{
			"token": sess.Token,
			"user":  ToAPIUser(user),
		})
	}))

	// POST /api/auth/login
	mux.HandleFunc("/api/auth/login", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodOptions {
			return
		}
		if r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		var input struct {
			Email    string `json:"email"`
			Password string `json:"password"`
		}
		if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
			http.Error(w, "Bad request", http.StatusBadRequest)
			return
		}

		user, err := dbInstance.GetUserByEmail(input.Email)
		if err != nil {
			http.Error(w, "Неверный email или пароль", http.StatusUnauthorized)
			return
		}

		err = bcrypt.CompareHashAndPassword([]byte(user.PasswordHash), []byte(input.Password))
		if err != nil {
			http.Error(w, "Неверный email или пароль", http.StatusUnauthorized)
			return
		}

		sess, err := dbInstance.CreateSession(user.ID)
		if err != nil {
			http.Error(w, "Session creation failed", http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]interface{}{
			"token": sess.Token,
			"user":  ToAPIUser(user),
		})
	}))

	// POST /api/auth/logout
	mux.HandleFunc("/api/auth/logout", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodOptions {
			return
		}
		if r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		authHeader := r.Header.Get("Authorization")
		if strings.HasPrefix(authHeader, "Bearer ") {
			token := strings.TrimPrefix(authHeader, "Bearer ")
			_ = dbInstance.DeleteSession(token)
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]string{"status": "success"})
	}))

	// GET /api/auth/me
	mux.HandleFunc("/api/auth/me", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodOptions {
			return
		}
		if r.Method != http.MethodGet {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		user, err := getAuthenticatedUser(r, dbInstance)
		if err != nil {
			http.Error(w, err.Error(), http.StatusUnauthorized)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]interface{}{
			"user": ToAPIUser(user),
		})
	}))

	// PUT /api/auth/profile
	mux.HandleFunc("/api/auth/profile", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodOptions {
			return
		}
		if r.Method != http.MethodPut {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		user, err := getAuthenticatedUser(r, dbInstance)
		if err != nil {
			http.Error(w, err.Error(), http.StatusUnauthorized)
			return
		}

		var input struct {
			Name     string `json:"name"`
			Phone    string `json:"phone"`
			City     string `json:"city"`
			Password string `json:"password"`
		}
		if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
			http.Error(w, "Bad request", http.StatusBadRequest)
			return
		}

		if input.Name == "" || input.Phone == "" || input.City == "" {
			http.Error(w, "Name, phone and city are required", http.StatusBadRequest)
			return
		}

		updatedUser, err := dbInstance.UpdateUser(user.ID, input.Name, input.Phone, input.City, input.Password)
		if err != nil {
			http.Error(w, "Failed to update profile: "+err.Error(), http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]interface{}{
			"status": "success",
			"user":   ToAPIUser(updatedUser),
		})
	}))

	// POST /api/auth/add-bonuses
	mux.HandleFunc("/api/auth/add-bonuses", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodOptions {
			return
		}
		if r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		user, err := getAuthenticatedUser(r, dbInstance)
		if err != nil {
			http.Error(w, err.Error(), http.StatusUnauthorized)
			return
		}

		var input struct {
			Amount int `json:"amount"`
		}
		if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
			http.Error(w, "Bad request", http.StatusBadRequest)
			return
		}

		if input.Amount <= 0 {
			http.Error(w, "Invalid amount", http.StatusBadRequest)
			return
		}

		updatedUser, err := dbInstance.AddUserBonuses(user.ID, input.Amount)
		if err != nil {
			http.Error(w, "Failed to add bonuses: "+err.Error(), http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]interface{}{
			"status": "success",
			"user":   ToAPIUser(updatedUser),
		})
	}))

	// ---- CALLBACK QUERY & STATUS ENDPOINTS ----

	// GET /api/callbacks (list callbacks for logged-in user or all if admin)
	mux.HandleFunc("/api/callbacks", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodOptions {
			return
		}
		if r.Method != http.MethodGet {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		user, err := getAuthenticatedUser(r, dbInstance)
		if err != nil {
			http.Error(w, err.Error(), http.StatusUnauthorized)
			return
		}

		var list []CallbackRecord
		if user.Role == "admin" {
			list, err = dbInstance.GetAllCallbacks()
		} else {
			list, err = dbInstance.GetCallbacks(user.ID, user.Phone)
		}

		if err != nil {
			http.Error(w, "Database error", http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(list)
	}))

	// PUT /api/callbacks/status (admin only, update callback status)
	mux.HandleFunc("/api/callbacks/status", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodOptions {
			return
		}
		if r.Method != http.MethodPut {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		user, err := getAuthenticatedUser(r, dbInstance)
		if err != nil {
			http.Error(w, err.Error(), http.StatusUnauthorized)
			return
		}

		if user.Role != "admin" {
			http.Error(w, "Forbidden (Admin only)", http.StatusForbidden)
			return
		}

		var input struct {
			ID     int    `json:"id"`
			Status string `json:"status"`
		}
		if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
			http.Error(w, "Bad request", http.StatusBadRequest)
			return
		}

		if input.ID == 0 || input.Status == "" {
			http.Error(w, "Invalid callback ID or status", http.StatusBadRequest)
			return
		}

		err = dbInstance.UpdateCallbackStatus(input.ID, input.Status)
		if err != nil {
			http.Error(w, "Failed to update status", http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]string{"status": "success"})
	}))

	// DELETE /api/callbacks/delete (admin only, delete callback)
	mux.HandleFunc("/api/callbacks/delete", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodOptions {
			return
		}
		if r.Method != http.MethodDelete {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		user, err := getAuthenticatedUser(r, dbInstance)
		if err != nil {
			http.Error(w, err.Error(), http.StatusUnauthorized)
			return
		}

		if user.Role != "admin" {
			http.Error(w, "Forbidden (Admin only)", http.StatusForbidden)
			return
		}

		idStr := r.URL.Query().Get("id")
		if idStr == "" {
			http.Error(w, "Missing id parameter", http.StatusBadRequest)
			return
		}

		id, err := strconv.Atoi(idStr)
		if err != nil {
			http.Error(w, "Invalid id parameter", http.StatusBadRequest)
			return
		}

		err = dbInstance.DeleteCallback(id)
		if err != nil {
			http.Error(w, "Failed to delete callback: "+err.Error(), http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]string{"status": "success"})
	}))

	// GET /api/reviews
	mux.HandleFunc("/api/reviews", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodOptions {
			return
		}
		if r.Method != http.MethodGet {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		reviews, err := dbInstance.GetReviews()
		if err != nil {
			http.Error(w, "Failed to get reviews", http.StatusInternalServerError)
			return
		}

		// Fallback to default reviews if DB is empty
		if len(reviews) == 0 {
			reviews = []ReviewRecord{
				{ID: 1, Author: "— Алия, Бостандыкский р-н", Text: "«Заказали клининг после ремонта + вывоз мусора. Приехали через час, всё сделали за вечер. Цена не выросла ни на тенге».", Rating: 5, CreatedAt: time.Now()},
				{ID: 2, Author: "— Ержан, мкр Самал", Text: "«Сломалась стиралка вечером. Мастер был у нас в 9 утра, починил за 40 минут. Дали гарантию на год».", Rating: 5, CreatedAt: time.Now()},
				{ID: 3, Author: "— Динара, ЖК «Альпийский»", Text: "«Перетяжка дивана — как новый. Забрали, через 4 дня привезли. Очень аккуратно».", Rating: 5, CreatedAt: time.Now()},
			}
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(reviews)
	}))

	// POST /api/reviews/new
	mux.HandleFunc("/api/reviews/new", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodOptions {
			return
		}
		if r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		var userID *int
		var defaultAuthor = "Аноним"

		user, err := getAuthenticatedUser(r, dbInstance)
		if err == nil && user != nil {
			userID = &user.ID
			defaultAuthor = user.Name
		}

		var input struct {
			Author string `json:"author"`
			Text   string `json:"text"`
			Rating int    `json:"rating"`
		}
		if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
			http.Error(w, "Bad request", http.StatusBadRequest)
			return
		}

		author := input.Author
		if author == "" {
			author = defaultAuthor
		}
		text := input.Text
		rating := input.Rating
		if rating < 1 || rating > 5 {
			rating = 5
		}

		if text == "" {
			http.Error(w, "Review text is required", http.StatusBadRequest)
			return
		}

		rev, err := dbInstance.CreateReview(author, text, rating, userID)
		if err != nil {
			http.Error(w, "Failed to create review", http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(rev)
	}))

	// GET /api/category-reviews?category_id=XXX
	mux.HandleFunc("/api/category-reviews", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodOptions {
			return
		}
		if r.Method != http.MethodGet {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		catID := r.URL.Query().Get("category_id")
		if catID == "" {
			http.Error(w, "Missing category_id parameter", http.StatusBadRequest)
			return
		}

		reviews, err := dbInstance.GetCategoryReviews(catID)
		if err != nil {
			http.Error(w, "Failed to get category reviews", http.StatusInternalServerError)
			return
		}

		if len(reviews) == 0 {
			reviews = []CategoryReviewRecord{
				{
					ID:         1,
					CategoryID: catID,
					Author:     "Арман, Алматы",
					Text:       "Отличный сервис! Мастер приехал вовремя, всё сделал быстро и качественно. Очень рекомендую.",
					Rating:     5,
					CreatedAt:  time.Now().Add(-24 * time.Hour),
				},
				{
					ID:         2,
					CategoryID: catID,
					Author:     "Айгерим",
					Text:       "Все супер, цена соответствует качеству. Спасибо большое за оперативность!",
					Rating:     5,
					CreatedAt:  time.Now().Add(-3 * 24 * time.Hour),
				},
			}
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(reviews)
	}))

	// POST /api/category-reviews/new
	mux.HandleFunc("/api/category-reviews/new", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodOptions {
			return
		}
		if r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		var userID *int
		var defaultAuthor = "Аноним"

		user, err := getAuthenticatedUser(r, dbInstance)
		if err == nil && user != nil {
			userID = &user.ID
			defaultAuthor = user.Name
		}

		var input struct {
			CategoryID string `json:"category_id"`
			Author     string `json:"author"`
			Text       string `json:"text"`
			Rating     int    `json:"rating"`
		}
		if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
			http.Error(w, "Bad request", http.StatusBadRequest)
			return
		}

		if input.CategoryID == "" {
			http.Error(w, "category_id is required", http.StatusBadRequest)
			return
		}

		author := input.Author
		if author == "" {
			author = defaultAuthor
		}
		text := input.Text
		rating := input.Rating
		if rating < 1 || rating > 5 {
			rating = 5
		}

		if text == "" {
			http.Error(w, "Review text is required", http.StatusBadRequest)
			return
		}

		rev, err := dbInstance.CreateCategoryReview(input.CategoryID, author, text, rating, userID)
		if err != nil {
			http.Error(w, "Failed to create category review", http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(rev)
	}))

	// GET /api/admin/pages (admin only)
	mux.HandleFunc("/api/admin/pages", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodOptions {
			return
		}
		if r.Method != http.MethodGet {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}
		user, err := getAuthenticatedUser(r, dbInstance)
		if err != nil {
			http.Error(w, err.Error(), http.StatusUnauthorized)
			return
		}
		if user.Role != "admin" {
			http.Error(w, "Forbidden (Admin only)", http.StatusForbidden)
			return
		}
		handleGetCustomPages(dbInstance)(w, r)
	}))

	// POST /api/admin/create-page (admin only)
	mux.HandleFunc("/api/admin/create-page", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodOptions {
			return
		}
		if r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}
		user, err := getAuthenticatedUser(r, dbInstance)
		if err != nil {
			http.Error(w, err.Error(), http.StatusUnauthorized)
			return
		}
		if user.Role != "admin" {
			http.Error(w, "Forbidden (Admin only)", http.StatusForbidden)
			return
		}
		handleCreateCustomPage(dbInstance)(w, r)
	}))

	// PUT /api/admin/update-page (admin only)
	mux.HandleFunc("/api/admin/update-page", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodOptions {
			return
		}
		if r.Method != http.MethodPut && r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}
		user, err := getAuthenticatedUser(r, dbInstance)
		if err != nil {
			http.Error(w, err.Error(), http.StatusUnauthorized)
			return
		}
		if user.Role != "admin" {
			http.Error(w, "Forbidden (Admin only)", http.StatusForbidden)
			return
		}
		handleUpdateCustomPage(dbInstance)(w, r)
	}))

	// DELETE /api/admin/delete-page (admin only)
	mux.HandleFunc("/api/admin/delete-page", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodOptions {
			return
		}
		if r.Method != http.MethodDelete && r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}
		user, err := getAuthenticatedUser(r, dbInstance)
		if err != nil {
			http.Error(w, err.Error(), http.StatusUnauthorized)
			return
		}
		if user.Role != "admin" {
			http.Error(w, "Forbidden (Admin only)", http.StatusForbidden)
			return
		}
		handleDeleteCustomPage(dbInstance)(w, r)
	}))

	// POST /api/admin/save-page-html (admin only)
	mux.HandleFunc("/api/admin/save-page-html", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodOptions {
			return
		}
		if r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}
		user, err := getAuthenticatedUser(r, dbInstance)
		if err != nil {
			http.Error(w, err.Error(), http.StatusUnauthorized)
			return
		}
		if user.Role != "admin" {
			http.Error(w, "Forbidden (Admin only)", http.StatusForbidden)
			return
		}

		var input struct {
			Page string `json:"page"`
			HTML string `json:"html"`
		}
		if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
			http.Error(w, "Bad request", http.StatusBadRequest)
			return
		}

		// Ensure we don't save outside of static directory
		cleanPage := filepath.Clean(input.Page)
		if strings.Contains(cleanPage, "..") {
			http.Error(w, "Invalid page path", http.StatusBadRequest)
			return
		}

		targetPath := filepath.Join(staticDir, cleanPage)
		err = os.WriteFile(targetPath, []byte(input.HTML), 0644)
		if err != nil {
			http.Error(w, "Failed to write file", http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]string{"status": "success"})
	}))

	// POST /api/admin/save-page-html-gz (admin only) - for large payloads
	mux.HandleFunc("/api/admin/save-page-html-gz", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodOptions {
			return
		}
		if r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}
		user, err := getAuthenticatedUser(r, dbInstance)
		if err != nil {
			http.Error(w, err.Error(), http.StatusUnauthorized)
			return
		}
		if user.Role != "admin" {
			http.Error(w, "Forbidden (Admin only)", http.StatusForbidden)
			return
		}

		err = r.ParseMultipartForm(10 << 20) // 10 MB
		if err != nil {
			http.Error(w, "Failed to parse form", http.StatusBadRequest)
			return
		}

		page := r.FormValue("page")
		file, _, err := r.FormFile("html")
		if err != nil {
			http.Error(w, "Missing file", http.StatusBadRequest)
			return
		}
		defer file.Close()

		cleanPage := filepath.Clean(page)
		if strings.Contains(cleanPage, "..") {
			http.Error(w, "Invalid page path", http.StatusBadRequest)
			return
		}

		// We need to decompress it!
		gzReader, err := gzip.NewReader(file)
		if err != nil {
			http.Error(w, "Failed to initialize gzip reader: " + err.Error(), http.StatusBadRequest)
			return
		}
		defer gzReader.Close()

		targetPath := filepath.Join(staticDir, cleanPage)
		
		htmlData, err := io.ReadAll(gzReader)
		if err != nil {
			http.Error(w, "Failed to read decompressed data", http.StatusInternalServerError)
			return
		}

		err = os.WriteFile(targetPath, htmlData, 0644)
		if err != nil {
			http.Error(w, "Failed to write target file", http.StatusInternalServerError)
			return
		}

		// Save the HTML to the DB files table so it persists across Railway deployments
		err = dbInstance.SaveFile(cleanPage, htmlData, "text/html; charset=utf-8")
		if err != nil {
			log.Printf("⚠️ Failed to save %s to db: %v\n", cleanPage, err)
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]string{"status": "success"})
	}))



	// staticDir is initialized at the start of main()

	mux.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "text/plain")
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte("ok"))
	})

	mux.Handle("/sitemap.xml", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/xml")
		http.ServeFile(w, r, filepath.Join(staticDir, "sitemap.xml"))
	}))

	mux.Handle("/robots.txt", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "text/plain")
		http.ServeFile(w, r, filepath.Join(staticDir, "robots.txt"))
	}))

	fileServer := http.FileServer(http.Dir(staticDir))
	mux.Handle("/", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		if strings.HasPrefix(r.URL.Path, "/api/") {
			http.NotFound(w, r)
			return
		}
		if r.URL.Path == "/admin" || r.URL.Path == "/admin/" {
			http.ServeFile(w, r, filepath.Join(staticDir, "admin.html"))
			return
		}
		if strings.HasPrefix(r.URL.Path, "/uploads/") {
			filename := strings.TrimPrefix(r.URL.Path, "/uploads/")
			data, mimeType, err := dbInstance.GetFile(filename)
			if err == nil {
				w.Header().Set("Content-Type", mimeType)
				w.Header().Set("Cache-Control", "public, max-age=31536000") // Cache for 1 year
				w.Write(data)
				return
			}
		}
		
		// Check if file exists in static directory
		cleanPath := filepath.Clean(r.URL.Path)
		
		// First check if the page exists in the DB (from visual builder)
		if cleanPath == "/" || cleanPath == "." || cleanPath == "" {
			cleanPath = "index.html"
		} else if strings.HasPrefix(cleanPath, "/") {
			cleanPath = cleanPath[1:]
		}
		dbData, dbMime, dbErr := dbInstance.GetFile(cleanPath)
		if dbErr == nil {
			w.Header().Set("Content-Type", dbMime)
			if strings.Contains(dbMime, "text/html") {
				htmlStr := string(dbData)
				if !strings.Contains(htmlStr, "favicon.svg") {
					htmlStr = strings.Replace(htmlStr, "<head>", "<head>\n  <link rel=\"icon\" type=\"image/svg+xml\" href=\"/favicon.svg\">", 1)
					dbData = []byte(htmlStr)
				}
			}
			w.Write(dbData)
			return
		}

		filePath := filepath.Join(staticDir, cleanPath)
		fi, err := os.Stat(filePath)
		if err == nil && !fi.IsDir() {
			fileServer.ServeHTTP(w, r)
			return
		}
		
		// If page wasn't found in DB or disk, serve index.html from DB if it exists, otherwise from disk
		dbIndex, dbIndexMime, err := dbInstance.GetFile("index.html")
		if err == nil {
			w.Header().Set("Content-Type", dbIndexMime)
			if strings.Contains(dbIndexMime, "text/html") {
				htmlStr := string(dbIndex)
				if !strings.Contains(htmlStr, "favicon.svg") {
					htmlStr = strings.Replace(htmlStr, "<head>", "<head>\n  <link rel=\"icon\" type=\"image/svg+xml\" href=\"/favicon.svg\">", 1)
					dbIndex = []byte(htmlStr)
				}
			}
			w.Write(dbIndex)
			return
		}
		http.ServeFile(w, r, filepath.Join(staticDir, "index.html"))
	}))

	// Check environment PORT or fallback to 3030
	port := os.Getenv("PORT")
	if port == "" {
		port = "3030"
	}

	fmt.Printf("🚀 HUB MASTER Go Backend server running on http://localhost:%s (serving from %s)\n", port, staticDir)
	log.Fatal(http.ListenAndServe(":"+port, mux))
}

// Helper to authenticate request and get User
func getAuthenticatedUser(r *http.Request, db DB) (*User, error) {
	authHeader := r.Header.Get("Authorization")
	if !strings.HasPrefix(authHeader, "Bearer ") {
		return nil, errors.New("unauthorized (missing token)")
	}
	token := strings.TrimPrefix(authHeader, "Bearer ")
	sess, err := db.GetSession(token)
	if err != nil {
		return nil, errors.New("unauthorized (invalid or expired session)")
	}
	user, err := db.GetUserByID(sess.UserID)
	if err != nil {
		return nil, errors.New("unauthorized (user not found)")
	}
	return user, nil
}

// corsMiddleware handles CORS headers for preflight and actual requests
func corsMiddleware(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusOK)
			return
		}

		next(w, r)
	}
}

func handleUpload(db DB, staticDir string) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		if r.Method != http.MethodPost {
			w.WriteHeader(http.StatusMethodNotAllowed)
			json.NewEncoder(w).Encode(map[string]string{
				"status":  "error",
				"message": "Only POST requests are allowed",
			})
			return
		}

		// Auth check
		authHeader := r.Header.Get("Authorization")
		if !strings.HasPrefix(authHeader, "Bearer ") {
			w.WriteHeader(http.StatusUnauthorized)
			json.NewEncoder(w).Encode(map[string]string{
				"status":  "error",
				"message": "Unauthorized",
			})
			return
		}
		token := strings.TrimPrefix(authHeader, "Bearer ")
		sess, err := db.GetSession(token)
		if err != nil {
			w.WriteHeader(http.StatusUnauthorized)
			json.NewEncoder(w).Encode(map[string]string{
				"status":  "error",
				"message": "Unauthorized",
			})
			return
		}
		user, err := db.GetUserByID(sess.UserID)
		if err != nil || user.Role != "admin" {
			w.WriteHeader(http.StatusForbidden)
			json.NewEncoder(w).Encode(map[string]string{
				"status":  "error",
				"message": "Forbidden",
			})
			return
		}

		// Parse multipart form, limit size to 10MB
		err = r.ParseMultipartForm(10 << 20)
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			json.NewEncoder(w).Encode(map[string]string{
				"status":  "error",
				"message": "Failed to parse form: " + err.Error(),
			})
			return
		}

		file, header, err := r.FormFile("file")
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			json.NewEncoder(w).Encode(map[string]string{
				"status":  "error",
				"message": "Failed to get file: " + err.Error(),
			})
			return
		}
		defer file.Close()

		// Validate extension
		ext := strings.ToLower(filepath.Ext(header.Filename))
		if ext != ".jpg" && ext != ".jpeg" && ext != ".png" && ext != ".gif" && ext != ".webp" && ext != ".svg" {
			w.WriteHeader(http.StatusBadRequest)
			json.NewEncoder(w).Encode(map[string]string{
				"status":  "error",
				"message": "Invalid file type. Only images are allowed.",
			})
			return
		}

		// Read file data
		fileData, err := io.ReadAll(file)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			json.NewEncoder(w).Encode(map[string]string{
				"status":  "error",
				"message": "Failed to read file: " + err.Error(),
			})
			return
		}

		// Determine mime type from extension
		mimeType := "application/octet-stream"
		switch ext {
		case ".jpg", ".jpeg":
			mimeType = "image/jpeg"
		case ".png":
			mimeType = "image/png"
		case ".gif":
			mimeType = "image/gif"
		case ".webp":
			mimeType = "image/webp"
		case ".svg":
			mimeType = "image/svg+xml"
		}

		filename := fmt.Sprintf("%d%s", time.Now().UnixNano(), ext)

		// Save to database
		err = db.SaveFile(filename, fileData, mimeType)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			json.NewEncoder(w).Encode(map[string]string{
				"status":  "error",
				"message": "Failed to save file to database: " + err.Error(),
			})
			return
		}

		json.NewEncoder(w).Encode(map[string]string{
			"status": "success",
			"url":    "/uploads/" + filename,
		})
	}
}
