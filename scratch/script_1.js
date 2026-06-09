
    // DATA
    let servicesData = [
      {
        id: "furniture",
        title: "Сборка мебели",
        titleKz: "Жиһаз жинау",
        titleEn: "Furniture Assembly",
        iconName: "hammer",
        items: [
          { name: "Сборка шкафа-купе", nameKz: "Купе-шкафты жинау", price: "от 8 000 ₸" },
          { name: "Сборка двуспальной кровати", nameKz: "Екі кісілік кереуетті жинау", price: "от 6 000 ₸" },
          { name: "Реставрация и ремонт дивана", nameKz: "Диванды жөндеу", price: "от 10 000 ₸" },
          { name: "Сборка кухонного гарнитура", nameKz: "Ас үй жиһазын жинау", price: "от 25 000 ₸" },
          { name: "Сборка комода / тумбы", nameKz: "Комодты жинау", price: "от 4 000 ₸" },
          { name: "Ремонт мебельной фурнитуры", nameKz: "Жиһаз бөлшектерін жөндеу", price: "от 3 000 ₸" }
        ]
      },
      {
        id: "appliances",
        title: "Ремонт бытовой техники",
        titleKz: "Бытовой техника жөндеу",
        titleEn: "Appliance Repair",
        iconName: "wrench",
        items: [
          { name: "Ремонт стиральной машины", nameKz: "Кір жуғыш машина жөндеу", price: "от 5 000 ₸" },
          { name: "Ремонт холодильника", nameKz: "Тоңазытқыш жөндеу", price: "от 6 000 ₸" },
          { name: "Ремонт посудомоечной машины", nameKz: "Ыдыс жуғыш машина жөндеу", price: "от 7 000 ₸" },
          { name: "Ремонт микроволновки", nameKz: "Қысқа толқынды пеш жөндеу", price: "от 3 000 ₸" },
          { name: "Установка кухонной плиты", nameKz: "Плитаны орнату", price: "от 4 500 ₸" },
          { name: "Ремонт кондиционера", nameKz: "Кондиционер жөндеу", price: "от 8 000 ₸" }
        ]
      },
      {
        id: "computer",
        title: "Компьютерная помощь",
        titleKz: "Компьютерлік көмек",
        titleEn: "Computer Help",
        iconName: "laptop",
        items: [
          { name: "Ремонт ноутбука", nameKz: "Ноутбук жөндеу", price: "от 8 000 ₸" },
          { name: "Установка Windows", nameKz: "Windows орнату", price: "от 4 000 ₸" },
          { name: "Чистка от пыли и замена термопасты", nameKz: "Шаңнан тазалау және термопаста ауыстыру", price: "от 5 000 ₸" },
          { name: "Сборка ПК на заказ", nameKz: "Компьютерді тапсырыспен жинау", price: "от 12 000 ₸" },
          { name: "Удаление вирусов", nameKz: "Вирустарды жою", price: "от 3 000 ₸" }
        ]
      },
      {
        id: "plumbing",
        title: "Сантехник",
        titleKz: "Сантехник қызметі",
        titleEn: "Plumbing",
        iconName: "droplet",
        items: [
          { name: "Устранение засоров", nameKz: "Құбыр бітелуін тазалау", price: "от 3 000 ₸" },
          { name: "Установка смесителя", nameKz: "Смеситель орнату", price: "от 4 000 ₸" },
          { name: "Монтаж унитаза / раковины", nameKz: "Унитазды / раковинаны орнату", price: "от 8 000 ₸" },
          { name: "Установка бойлера", nameKz: "Бойлер орнату", price: "от 6 000 ₸" }
        ]
      },
      {
        id: "electrical",
        title: "Электрик",
        titleKz: "Электрик қызметі",
        titleEn: "Electrical",
        iconName: "bolt",
        items: [
          { name: "Установка розетки / выключателя", nameKz: "Розетка орнату", price: "от 1 500 ₸" },
          { name: "Навеска люстры", nameKz: "Люстра ілу", price: "от 4 000 ₸" },
          { name: "Ремонт проводки", nameKz: "Электр сымын жөндеу", price: "от 5 000 ₸" },
          { name: "Замена автоматов", nameKz: "Автоматтарды ауыстыру", price: "от 3 000 ₸" }
        ]
      },
      {
        id: "cleaning",
        title: "Клининг",
        titleKz: "Тазалық қызметі",
        titleEn: "Cleaning",
        iconName: "sparkles",
        items: [
          { name: "Генеральная уборка", nameKz: "Бас тазалау", price: "от 15 000 ₸" },
          { name: "Экспресс-уборка", nameKz: "Жылдам тазалау", price: "от 8 000 ₸" },
          { name: "Химчистка дивана", nameKz: "Диванды химиялық тазалау", price: "от 6 000 ₸" }
        ]
      },
      {
        id: "auto",
        title: "Автосервис",
        titleKz: "Автокөлік жөндеу",
        titleEn: "Auto Service",
        iconName: "car",
        items: [
          { name: "Замена масла", nameKz: "Майды ауыстыру", price: "от 3 000 ₸" },
          { name: "Шиномонтаж", nameKz: "Дөңгелек жөндеу", price: "от 4 000 ₸" },
          { name: "Диагностика автомобиля", nameKz: "Көлікті диагностикалау", price: "от 5 000 ₸" }
        ]
      },
      {
        id: "movers",
        title: "Грузчики",
        titleKz: "Жүк тасушылар",
        titleEn: "Movers",
        iconName: "users",
        items: [
          { name: "Услуги грузчиков (час)", nameKz: "Жүк тасу қызметі (сағат)", price: "от 2 500 ₸/ч" },
          { name: "Грузоперевозки по городу", nameKz: "Қала бойынша жүк тасымалы", price: "от 5 000 ₸" },
          { name: "Квартирный переезд", nameKz: "Пәтер көшіру", price: "от 15 000 ₸" }
        ]
      },
      {
        id: "delivery",
        title: "Доставка",
        titleKz: "Жеткізу қызметі",
        titleEn: "Delivery",
        iconName: "truck",
        items: [
          { name: "Курьерская доставка", nameKz: "Курьерлік жеткізу", price: "от 1 500 ₸" },
          { name: "Доставка крупных грузов", nameKz: "Ірі жүктерді жеткізу", price: "от 6 000 ₸" }
        ]
      }
    ];

    const reviewsData = [
      { name: "Алина М.", nameKz: "Әлина М.", nameEn: "Alina M.", avatarBg: "#e63333", service: "Ремонт стиральной машины", rating: 5, text: "Мастер приехал уже через час после заявки. Быстро нашёл проблему, заменил деталь. Машина работает отлично!", textKz: "Шебер өтінімнен кейін бір сағатта келді. Ақауды тез тауып, бөлшекті ауыстырды. Машина керемет жұмыс істеп тұр!", textEn: "The specialist arrived within an hour. Quickly found the issue and replaced the part. Works great!" },
      { name: "Дмитрий К.", nameKz: "Дмитрий К.", nameEn: "Dmitriy K.", avatarBg: "#3498db", service: "Ремонт ноутбука", rating: 5, text: "Отнёс ноутбук после того, как залил его водой. Починили за 2 дня, дали гарантию 3 месяца. Всё работает как новый.", textKz: "Су төгілгеннен кейін ноутбугымды апардым. 2 күнде жөндеп, 3 айға кепілдік берді. Жаңа сияқты.", textEn: "Brought my laptop here after spilling water. Fixed it in 2 days, gave a 3-month warranty. Works like new." },
      { name: "Зарина Б.", nameKz: "Зарина Б.", nameEn: "Zarina B.", avatarBg: "#e74c3c", service: "Клининг квартиры", rating: 5, text: "Заказала уборку 3-комнатной квартиры после ремонта. Команда из 3 человек справилась за 4 часа. Результат превзошёл все ожидания!", textKz: "Жөндеуден кейін пәтерді тазалауға тапсырыс бердім. Өте таза, бәрі жарқырап тұр!", textEn: "Ordered post-renovation cleaning. The team of 3 did a fantastic job. The result is sparkling clean!" }
    ];

    const translations = {
      RU: {
        tagline: "Все нужное — в 1 клик!",
        callMaster: "Вызвать мастера",
        catalogTitle: "Каталог услуг",
        catalogSub: "Выберите категорию, чтобы ознакомиться с ценами и сделать быстрый заказ",
        orderBtn: "Заказать услугу",
        whyTitle: "Почему выбирают нас?",
        whySub: "Премиальный сервис для вашего дома и бизнеса",
        why1: "Официальная гарантия",
        why1Desc: "Предоставляем письменную гарантию на все виды работ до 1 года.",
        why2: "Оперативный выезд",
        why2Desc: "Мастер приедет в течение 45 минут после вашего звонка или в удобное время.",
        why3: "Опытные специалисты",
        why3Desc: "Все мастера прошли сертификацию и имеют подтвержденный стаж от 5 лет.",
        why4: "Честные цены",
        why4Desc: "Рассчитываем стоимость до начала работ. Никаких скрытых платежей.",
        reviewsTitle: "Отзывы клиентов",
        reviewsSub: "Более 50 000 довольных клиентов — лучшее подтверждение нашей работы",
        writeReview: "Оставить отзыв",
        yourName: "Ваше имя",
        yourPhone: "Номер телефона",
        selectService: "Выберите услугу",
        reviewText: "Текст отзыва",
        submitReview: "Отправить отзыв",
        leaveRequest: "Оставьте заявку",
        leaveRequestSub: "Наш оператор перезвонит вам в течение 10 минут",
        sendRequest: "Отправить заявку",
        successTitle: "Заявка успешно принята!",
        successDesc: "Мы свяжемся с вами в течение 10 минут. Спасибо!",
        cabinet: "Кабинет",
        contacts: "Контакты",
        copyright: "© 2026 HUB MASTER. Все права защищены.",
        heroSubtextText: "Сборка кухонь, шкафов-купе, ремонт каркасов и перетяжка мягкой мебели с премиальной фурнитурой и гарантией качества.",
        btnCallFurniture: "Вызвать мебельщика",
        btnCallMe: "Перезвонить мне",
        ourMastersTitle: "Наши мастера",
        whyChooseTitle: "Почему выбирают нас",
        tabServices: "Услуги",
        tabMasters: "Мастера",
        tabWindows: "Окна",
        tabRepair: "Ремонт",
        tabCleaning: "Клининг",
        availableLabel: "Свободен",
        whyTitle1: "112 Услуг",
        whyDesc1: "Широкий спектр работ",
        whyTitle2: "24/7 Поддержка",
        whyDesc2: "Круглосуточная помощь",
        whyTitle3: "Прозрачные цены",
        whyDesc3: "Фиксированные прайсы",
        whyTitle4: "Опытные мастера",
        whyDesc4: "Только профессионалы",
        whyTitle5: "Гарантия качества",
        whyDesc5: "До 1 года на работы",
        whyTitle6: "Быстрый выезд",
        whyDesc6: "В течение 1 часа",
        whyTitle7: "Безопасная оплата",
        whyDesc7: "Картой или наличными",
        whyTitle8: "Отзывы клиентов",
        whyDesc8: "Реальные оценки",
        whyTitle9: "Контроль качества",
        whyDesc9: "Постоянный мониторинг",
        ordersCount: "выполненных заказов",
        ratingAvg: "средняя оценка",
        arrivalTime: "среднее время прибытия",
        warrantyLabel: "гарантия на работы",
        highlightArrival: "Прибытие за 45 мин",
        highlightWarranty: "Гарантия 12 месяцев",
        highlightControl: "Контроль 24/7",
        highlightReports: "Фото/Видео отчёты",
        heroTitle: "КАЧЕСТВЕННАЯ<br><span class=\"highlight\">СБОРКА</span><br><span class=\"highlight\">И РЕСТАВРАЦИЯ</span><br><span class=\"highlight\">ВАШЕЙ</span><br>ВАШЕЙ МЕБЕЛИ",
        selectPrompt: "-- Выберите --",
        ratingLabel: "Оценка",
        feat1: "Выезд бесплатно",
        feat2: "Гарантия качества",
        feat3: "Опытные специалисты",
        feat4: "Работаем 24/7",
        minUnit: "мин"
      },
      KZ: {
        tagline: "Барлық қажеттіліктер — 1 басуда!",
        callMaster: "Шеберді шақыру",
        catalogTitle: "Қызметтер каталогы",
        catalogSub: "Бағалармен танысып, жылдам тапсырыс беру үшін санатты таңдаңыз",
        orderBtn: "Қызметке тапсырыс беру",
        whyTitle: "Неліктен бізді таңдайды?",
        whySub: "Сіздің үйіңіз бен бизнесіңіз үшін премиум қызмет",
        why1: "Ресми кепілдік",
        why1Desc: "Барлық жұмыс түрлеріне 1 жылға дейін жазбаша кепілдік береміз.",
        why2: "Жедел келу",
        why2Desc: "Шебер сіздің қоңырауыңыздан кейін 45 минут ішінде немесе ыңғайлы уақытта келеді.",
        why3: "Тәжірибелі мамандар",
        why3Desc: "Барлық шеберлер сертификаттаудан өткен және 5 жылдан астам тәжірибесі бар.",
        why4: "Әділ бағалар",
        why4Desc: "Жұмыс басталғанға дейін құнын есептейміз. Жасырын төлемдер жоқ.",
        reviewsTitle: "Клиенттердің пікірлері",
        reviewsSub: "50 000-нан астам риза клиент — біздің жұмысымыздың ең жақсы дәлелі",
        writeReview: "Пікір қалдыру",
        yourName: "Сіздің есіміңіз",
        yourPhone: "Телефон нөмірі",
        selectService: "Қызметті таңдаңыз",
        reviewText: "Пікір мәтіні",
        submitReview: "Пікірді жіберу",
        leaveRequest: "Өтінім қалдыру",
        leaveRequestSub: "Біздің оператор мәліметтерді нақтылау үшін 10 минут ішінде хабарласады",
        sendRequest: "Өтінімді жіберу",
        successTitle: "Өтінім сәтті қабылданды!",
        successDesc: "Біз сізбен 10 минут ішінде хабарласамыз. Рақмет!",
        cabinet: "Кабинет",
        contacts: "Байланыс",
        copyright: "© 2026 HUB MASTER. Барлық құқықтар қорғалған.",
        heroSubtextText: "Премиум фурнитурамен және сапа кепілдігімен ас үйлерді, шкафтарды жинау, қаңқаларды жөндеу және жұмсақ жиһаздарды қаптау.",
        btnCallFurniture: "Жиһазшыны шақыру",
        btnCallMe: "Маған хабарласыңыз",
        ourMastersTitle: "Біздің шеберлер",
        whyChooseTitle: "Неге бізді таңдайды",
        tabServices: "Қызметтер",
        tabMasters: "Шеберлер",
        tabWindows: "Терезелер",
        tabRepair: "Жөндеу",
        tabCleaning: "Тазалық",
        availableLabel: "Бос",
        whyTitle1: "112 Қызметтер",
        whyDesc1: "Жұмыстардың кең ауқымы",
        whyTitle2: "24/7 Қолдау",
        whyDesc2: "Тәулік бойы көмек",
        whyTitle3: "Ашық бағалар",
        whyDesc3: "Бекітілген бағалар",
        whyTitle4: "Тәжірибелі шеберлер",
        whyDesc4: "Тек кәсіби мамандар",
        whyTitle5: "Сапа кепілдігі",
        whyDesc5: "Жұмысқа 1 жылға дейін",
        whyTitle6: "Жылдам келу",
        whyDesc6: "1 сағат ішінде",
        whyTitle7: "Қауіпсіз төлем",
        whyDesc7: "Картамен немесе қолма-қол",
        whyTitle8: "Клиенттердің пікірлері",
        whyDesc8: "Шынайы бағалар",
        whyTitle9: "Сапаны бақылау",
        whyDesc9: "Тұрақты мониторинг",
        ordersCount: "орындалған тапсырыстар",
        ratingAvg: "орташа бағалау",
        arrivalTime: "орташа келу уақыты",
        warrantyLabel: "жұмыс кепілдігі",
        highlightArrival: "45 минутта келу",
        highlightWarranty: "12 ай кепілдік",
        highlightControl: "24/7 бақылау",
        highlightReports: "Фото/Видео есептер",
        heroTitle: "ЖИҺАЗДАРЫҢЫЗДЫ<br><span class=\"highlight\">САПАЛЫ ЖИНАУ</span><br><span class=\"highlight\">ЖӘНЕ ҚАЛПЫНА КЕЛТІРУ</span>",
        selectPrompt: "-- Таңдаңыз --",
        ratingLabel: "Бағалау",
        feat1: "Келу тегін",
        feat2: "Сапа кепілдігі",
        feat3: "Тәжірибелі мамандар",
        feat4: "24/7 жұмыс істейміз",
        minUnit: "мин"
      },
      EN: {
        tagline: "Everything you need — in 1 click!",
        callMaster: "Call a Master",
        catalogTitle: "Services Catalog",
        catalogSub: "Select a category to view prices and make a quick order",
        orderBtn: "Order Service",
        whyTitle: "Why Choose Us?",
        whySub: "Premium service for your home and business",
        why1: "Official Warranty",
        why1Desc: "We provide a written warranty for all types of work up to 1 year.",
        why2: "Fast Response",
        why2Desc: "Specialist will arrive within 45 minutes after your call or at your convenience.",
        why3: "Expert Techs",
        why3Desc: "All technicians are certified and have a proven background of over 5 years.",
        why4: "Fair Pricing",
        why4Desc: "We estimate the cost before the work starts. No hidden surcharges.",
        reviewsTitle: "Customer Reviews",
        reviewsSub: "Over 50,000 satisfied clients — the best proof of our quality work",
        writeReview: "Write a Review",
        yourName: "Your Name",
        yourPhone: "Phone Number",
        selectService: "Select Service",
        reviewText: "Review Text",
        submitReview: "Submit Review",
        leaveRequest: "Leave a Request",
        leaveRequestSub: "Our operator will call you back within 10 minutes to discuss the details",
        sendRequest: "Submit Request",
        successTitle: "Request Received Successfully!",
        successDesc: "We will contact you within 10 minutes. Thank you!",
        cabinet: "Cabinet",
        contacts: "Contacts",
        copyright: "© 2026 HUB MASTER. All rights reserved.",
        heroSubtextText: "Assembly of kitchens, wardrobes, repair of frames and upholstery of upholstered furniture with premium fittings and quality guarantee.",
        btnCallFurniture: "Call a furniture maker",
        btnCallMe: "Call me back",
        ourMastersTitle: "Our masters",
        whyChooseTitle: "Why choose us",
        tabServices: "Services",
        tabMasters: "Masters",
        tabWindows: "Windows",
        tabRepair: "Repair",
        tabCleaning: "Cleaning",
        availableLabel: "Available",
        whyTitle1: "112 Services",
        whyDesc1: "Wide range of works",
        whyTitle2: "24/7 Support",
        whyDesc2: "Round-the-clock help",
        whyTitle3: "Transparent pricing",
        whyDesc3: "Fixed price lists",
        whyTitle4: "Expert Techs",
        whyDesc4: "Only professionals",
        whyTitle5: "Quality Guarantee",
        whyDesc5: "Up to 1 year warranty",
        whyTitle6: "Fast arrival",
        whyDesc6: "Within 1 hour",
        whyTitle7: "Secure payment",
        whyDesc7: "By card or cash",
        whyTitle8: "Customer reviews",
        whyDesc8: "Real ratings",
        whyTitle9: "Quality control",
        whyDesc9: "Continuous monitoring",
        ordersCount: "completed orders",
        ratingAvg: "average rating",
        arrivalTime: "average arrival time",
        warrantyLabel: "work warranty",
        highlightArrival: "Arrival in 45 min",
        highlightWarranty: "12 months warranty",
        highlightControl: "24/7 Control",
        highlightReports: "Photo/Video reports",
        heroTitle: "QUALITY<br><span class=\"highlight\">ASSEMBLY</span><br><span class=\"highlight\">AND RESTORATION</span><br>OF YOUR FURNITURE",
        selectPrompt: "-- Select --",
        ratingLabel: "Rating",
        feat1: "Free visit",
        feat2: "Quality guarantee",
        feat3: "Certified specialists",
        feat4: "Working 24/7",
        minUnit: "min"
      }
    };

    // STATE
    let currentLang = 'RU';
    let currentCity = 'Алматы';
    let currentTheme = 'dark';
    let selectedCategory = 'furniture';
    let reviewRating = 5;

    // SVG renderers
    const svgIcons = {
      hammer: `<svg viewBox="0 0 24 24"><path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z"/></svg>`,
      wrench: `<svg viewBox="0 0 24 24"><path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z"/></svg>`,
      laptop: `<svg viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/></svg>`,
      droplet: `<svg viewBox="0 0 24 24"><path d="M12 22s-8-4.5-8-11.8A8 8 0 0112 2a8 8 0 018 8.2c0 7.3-8 11.8-8 11.8z"/><circle cx="12" cy="10" r="3"/></svg>`,
      bolt: `<svg viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>`,
      sparkles: `<svg viewBox="0 0 24 24"><path d="M12 3v1M12 20v1M4 12H3M21 12h-1M18.36 5.64l-.7.7M6.34 17.66l-.7.7M18.36 17.66l-.7-.7M6.34 6.34l-.7-.7M12 8a4 4 0 100 8 4 4 0 000-8z"/></svg>`,
      car: `<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>`,
      users: `<svg viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/></svg>`,
      truck: `<svg viewBox="0 0 24 24"><rect x="1" y="3" width="15" height="13" rx="2"/><path d="M16 8h5l2 4v3h-7V8zM5.5 21a1.5 1.5 0 100-3 1.5 1.5 0 000 3zM18.5 21a1.5 1.5 0 100-3 1.5 1.5 0 000 3z"/></svg>`,
      phone: `<svg viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81a19.79 19.79 0 01-3.07-8.68A2 2 0 012 1h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 8.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/></svg>`
    };

    // INIT

    let clientBotConfig = {
      fallback: "Спасибо! Специалист уже рассматривает ваш запрос.",
      rules: []
    };

    async function loadClientBotConfig() {
      try {
        const res = await fetch(API_BASE + '/api/assistant-config');
        if (res.ok) {
          const data = await res.json();
          if (data && data.fallback) {
            clientBotConfig = data;
          }
        }
      } catch (e) {
        console.error("Failed to load assistant configuration:", e);
      }
    }

    window.addEventListener('DOMContentLoaded', async () => {
      switchLang('RU');
      loadClientBotConfig();
      await fetchDynamicCatalog();
      initRouter();
      initScrollReveal();
      renderReviews();
    });

    // RENDER HERO PILLS
    function populatePills() {
      const pillsContainer = document.getElementById('hero-pills');
      if (!pillsContainer) return;
      pillsContainer.innerHTML = '';
      servicesData.forEach(svc => {
        const btn = document.createElement('button');
        btn.className = `svc-pill-button ${selectedCategory === svc.id ? 'active' : ''}`;
        btn.id = `pill-${svc.id}`;
        btn.onclick = () => switchCategory(svc.id, true);

        btn.innerHTML = `
          <div class="svc-pill-icon-box">
            ${svgIcons[svc.iconName]}
          </div>
          <span class="pill-text" data-title-ru="${svc.title}" data-title-kz="${svc.titleKz}" data-title-en="${svc.titleEn}">
            ${svc.title}
          </span>
        `;
        pillsContainer.appendChild(btn);
      });
    }

    // RENDER CATALOG TABS
    function populateCatalogTabs() {
      const tabsContainer = document.getElementById('catalog-tab-headers');
      tabsContainer.innerHTML = '';
      servicesData.forEach(svc => {
        const btn = document.createElement('button');
        btn.className = `catalog-tab-btn ${selectedCategory === svc.id ? 'active' : ''}`;
        btn.id = `tab-${svc.id}`;
        btn.onclick = () => switchCategory(svc.id, false);
        btn.setAttribute('data-title-ru', svc.title);
        btn.setAttribute('data-title-kz', svc.titleKz);
        btn.setAttribute('data-title-en', svc.titleEn);
        btn.innerText = svc.title;
        tabsContainer.appendChild(btn);
      });
    }

    // RENDER CATALOG ITEMS
    function renderCatalogItems() {
      const grid = document.getElementById('catalog-items-grid');
      grid.innerHTML = '';
      const currentSvc = servicesData.find(s => s.id === selectedCategory) || servicesData[0];

      currentSvc.items.forEach(item => {
        const card = document.createElement('div');
        card.className = 'catalog-card';

        const placeholderImages = [
          "https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=600&q=80",
          "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=600&q=80",
          "https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=600&q=80",
          "https://images.unsplash.com/photo-1621905252507-b35492cc74b4?w=600&q=80",
          "https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=600&q=80",
          "https://images.unsplash.com/photo-1581141849291-1125c7b692b5?w=600&q=80",
          "https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?w=600&q=80",
          "https://images.unsplash.com/photo-1542013936693-884638332954?w=600&q=80"
        ];

        card.innerHTML = `
          <div class="catalog-card-img" style="background-image: url('${placeholderImages[Math.floor(Math.random() * placeholderImages.length)]}');"></div>
          <div class="catalog-card-content">
            <div class="catalog-card-title" data-name-ru="${item.name}" data-name-kz="${item.nameKz}" data-name-en="${item.name}">
              ${currentLang === 'RU' || currentLang === 'EN' ? item.name : item.nameKz}
            </div>
            <div class="catalog-card-bottom">
              <div class="catalog-card-price">${item.price.replace('от ', 'от ').replace(' ₸', ' ₸')}<span> за работу</span></div>
              <button class="catalog-card-action" onclick="navigateThematic('${selectedCategory}', '${item.catId}', '${item.id}')">
                ${currentLang === 'RU' ? 'Заказать' : currentLang === 'KZ' ? 'Тапсырыс' : 'Order'}
              </button>
            </div>
          </div>
        `;
        grid.appendChild(card);
      });
      // Translate dynamic catalog elements
      translateUI();
    }

    // RENDER REVIEWS
    function renderReviews() {
      const grid = document.getElementById('reviews-cards-grid');
      grid.innerHTML = '';
      reviewsData.forEach(rev => {
        const card = document.createElement('div');
        card.className = 'review-card';

        const starsStr = '★'.repeat(rev.rating) + '☆'.repeat(5 - rev.rating);

        card.innerHTML = `
          <div>
            <div class="review-header">
              <div class="review-avatar" style="background-color: ${rev.avatarBg || '#e63333'}">
                ${rev.name[0]}
              </div>
              <div>
                <div class="review-name" data-name-ru="${rev.name}" data-name-kz="${rev.nameKz}" data-name-en="${rev.nameEn}">${currentLang === 'RU' ? rev.name : currentLang === 'KZ' ? rev.nameKz : rev.nameEn}</div>
                <div class="review-service">${rev.service}</div>
              </div>
            </div>
            <div class="review-rating-stars">${starsStr}</div>
            <p class="review-text-content" data-text-ru="${rev.text}" data-text-kz="${rev.textKz}" data-text-en="${rev.textEn}">
              "${currentLang === 'RU' ? rev.text : currentLang === 'KZ' ? rev.textKz : rev.textEn}"
            </p>
          </div>
        `;
        grid.appendChild(card);
      });
    }

    // POPULATE DROPDOWNS
    function populateSelectDropdowns() {
      const revSel = document.getElementById('rev-service');
      const leadSel = document.getElementById('lead-service-select');

      revSel.innerHTML = '<option value="" data-i18n="selectPrompt">-- Выберите --</option>';
      leadSel.innerHTML = '';

      servicesData.forEach(s => {
        const optRev = document.createElement('option');
        optRev.value = s.title;
        optRev.setAttribute('data-title-ru', s.title);
        optRev.setAttribute('data-title-kz', s.titleKz);
        optRev.setAttribute('data-title-en', s.titleEn);
        optRev.innerText = s.title;
        revSel.appendChild(optRev);

        const optLead = document.createElement('option');
        optLead.value = s.id;
        optLead.setAttribute('data-title-ru', s.title);
        optLead.setAttribute('data-title-kz', s.titleKz);
        optLead.setAttribute('data-title-en', s.titleEn);
        optLead.innerText = s.title;
        leadSel.appendChild(optLead);
      });
    }

    // ACTIONS
    function switchCategory(id, smoothScroll = false) {
      selectedCategory = id;

      // Update pills
      document.querySelectorAll('.svc-pill-button').forEach(btn => {
        btn.classList.remove('active');
      });
      const activePill = document.getElementById(`pill-${id}`);
      if (activePill) activePill.classList.add('active');

      // Update catalog tabs
      document.querySelectorAll('.catalog-tab-btn').forEach(btn => {
        btn.classList.remove('active');
      });
      const activeTab = document.getElementById(`tab-${id}`);
      if (activeTab) activeTab.classList.add('active');

      // Update nav active link
      document.querySelectorAll('.nav-link-item').forEach(btn => {
        btn.classList.remove('active');
      });
      if (id === 'furniture') {
        document.getElementById('nav-btn-furniture').classList.add('active');
      }

      renderCatalogItems();

      if (typeof updateURL === 'function') {
        updateURL();
      }

      if (smoothScroll) {
        document.getElementById('catalog').scrollIntoView({ behavior: 'smooth' });
      }
    }

    // Dropdown helpers
    function switchCategoryFromMenu(id) {
      closeAllDropdowns();
      switchCategory(id, false);
      setTimeout(() => {
        const el = document.getElementById('catalog');
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 80);
    }

    function toggleDropdown(e, id) {
      e.stopPropagation();
      const el = document.getElementById(id);
      const isShown = el.classList.contains('show');
      closeAllDropdowns();
      if (!isShown) el.classList.add('show');
    }

    function closeAllDropdowns() {
      document.querySelectorAll('.dropdown-menu').forEach(el => el.classList.remove('show'));
    }

    window.addEventListener('click', function (e) {
      if (!e.target.closest('.dropdown')) {
        closeAllDropdowns();
      }
    });

    function selectCity(city) {
      currentCity = city;
      document.getElementById('current-city-label').innerText = currentCity;
      document.getElementById('nav-subtitle').innerText = `${currentCity} • С 2018`;

      const footerAddr = document.getElementById('footer-address');
      if (footerAddr) {
        if (currentCity === 'Алматы') footerAddr.innerText = 'Алматы, пр. Аль-Фараби 77/7';
        else if (currentCity === 'Астана') footerAddr.innerText = 'Астана, пр. Кабанбай Батыра 15';
        else footerAddr.innerText = currentCity + ', ул. Абая 1';
      }

      const heroCityPill = document.getElementById('hero-city-pill');
      if (heroCityPill) {
        heroCityPill.innerText = currentCity;
      }
      closeAllDropdowns();
    }

    function toggleTheme() {
      currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', currentTheme);

      if (currentTheme === 'dark') {
        document.getElementById('theme-sun').style.display = 'block';
        document.getElementById('theme-moon').style.display = 'none';
      } else {
        document.getElementById('theme-sun').style.display = 'none';
        document.getElementById('theme-moon').style.display = 'block';
      }
    }

    // TRANSLATIONS
    function switchLang(langCode) {
      currentLang = langCode;

      // Update lang buttons
      document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.innerText === langCode) btn.classList.add('active');
      });

      translateUI();
      renderCatalogItems();
      renderReviews();
    }

    function translateUI() {
      const data = translations[currentLang];

      // Update elements with data-i18n attributes
      document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (data[key]) {
          if (key === 'heroTitle' || data[key].includes('<')) {
            el.innerHTML = data[key];
          } else {
            el.innerText = data[key];
          }
        }
      });

      // Update custom translated properties
      document.getElementById('stat-arrival-value').innerText = `45 ${data.minUnit}`;
      document.getElementById('footer-desc').innerText = currentLang === 'RU'
        ? 'Профессиональная сборка мебели, ремонт бытовой техники, компьютерная помощь, сантехнические и электромонтажные услуги в Алматы и Астане. Быстро, качественно и с долгосрочной гарантией.'
        : currentLang === 'KZ'
          ? 'Алматы және Астана қалаларында жиһаз жинау, тұрмыстық техниканы жөндеу, компьютерлік көмек, сантехникалық және электр монтаждау қызметтері. Жылдам, сапалы және ұзақ мерзімді кепілдікпен.'
          : 'Professional furniture assembly, appliance repair, computer help, plumbing and electrical services in Almaty and Astana. Fast, high-quality, and with long-term warranty.';

      // Translate options & text attributes
      document.querySelectorAll('[data-title-ru]').forEach(el => {
        el.innerText = el.getAttribute(`data-title-${currentLang.toLowerCase()}`);
      });

      document.querySelectorAll('[data-name-ru]').forEach(el => {
        el.innerText = el.getAttribute(`data-name-${currentLang.toLowerCase()}`);
      });
      renderMastersCarousel();
    }
    // MASTERS CAROUSEL & TAB HANDLERS
    const mastersData = [
      {
        name: "Азамат Т.",
        role: { RU: "Реставратор мебели", KZ: "Жиһаз қалпына келтіруші", EN: "Furniture Restorer" },
        rating: 5,
        avatar: "/public/master_azamat.png"
      },
      {
        name: "Данияр К.",
        role: { RU: "Сборщик мебели", KZ: "Жиһаз жинаушы", EN: "Furniture Assembler" },
        rating: 5,
        avatar: "/public/master_daniyar.png"
      },
      {
        name: "Алибек И.",
        role: { RU: "Мастер по перетяжке", KZ: "Қаптау шебері", EN: "Re-upholstery Master" },
        rating: 5,
        avatar: "/public/master_alibek.png"
      },
      {
        name: "Руслан С.",
        role: { RU: "Электрик", KZ: "Электрик", EN: "Electrician" },
        rating: 5,
        avatar: "/public/master_ruslan.png"
      },
      {
        name: "Арман Б.",
        role: { RU: "Сантехник", KZ: "Сантехник", EN: "Plumber" },
        rating: 5,
        avatar: "/public/master_arman.png"
      }
    ];

    let currentCarouselOffset = 0;

    function renderMastersCarousel() {
      const track = document.getElementById('masters-track');
      if (!track) return;

      const statusText = translations[currentLang].availableLabel || (currentLang === 'RU' ? 'Свободен' : currentLang === 'KZ' ? 'Бос' : 'Available');

      track.innerHTML = mastersData.map(m => `
        <div class="master-card-new">
          <div class="master-avatar-circle">
            <img src="${m.avatar}" alt="${m.name}">
          </div>
          <div class="master-name-new">${m.name}</div>
          <div class="master-role-new">${m.role[currentLang]}</div>
          <div class="master-stars-new">${'★'.repeat(m.rating)}</div>
          <div class="master-status-pill">${statusText}</div>
        </div>
      `).join('');

      currentCarouselOffset = 0;
      track.style.transform = `translateX(0px)`;
    }

    function moveCarousel(direction) {
      const track = document.getElementById('masters-track');
      if (!track) return;

      const cardWidth = 162; // card flex width (150) + gap (12)
      const maxOffset = mastersData.length - 3;

      currentCarouselOffset += direction;
      if (currentCarouselOffset < 0) currentCarouselOffset = 0;
      if (currentCarouselOffset > maxOffset) currentCarouselOffset = maxOffset;

      track.style.transform = `translateX(-${currentCarouselOffset * cardWidth}px)`;
    }

    function handleHeroTabClick(tabType, categoryName) {
      // Prevent default to avoid page reload issues
      if (window.event) window.event.preventDefault();

      document.querySelectorAll('.nav-tab-btn').forEach(btn => {
        btn.classList.remove('active');
      });
      if (window.event && window.event.currentTarget) {
        window.event.currentTarget.classList.add('active');
      }

      if (tabType === 'scroll') {
        const target = document.getElementById(categoryName);
        if (target) {
          target.scrollIntoView({ behavior: 'smooth' });
        }
      } else if (tabType === 'category') {
        switchCategory(categoryName);
        const target = document.getElementById('catalog');
        if (target) {
          target.scrollIntoView({ behavior: 'smooth' });
        }
      }
    }


    // MODAL
    function openModal(serviceName, skipUrlUpdate = false) {
      document.getElementById('modal-overlay').classList.add('active');
      document.body.style.overflow = 'hidden';

      const desc = document.getElementById('modal-selected-service-text');
      if (serviceName) {
        desc.innerText = `${currentLang === 'RU' ? 'Услуга' : currentLang === 'KZ' ? 'Қызмет' : 'Service'}: ${serviceName}`;
        activeServiceName = serviceName;
      } else {
        desc.innerText = translations[currentLang].leaveRequestSub;
        activeServiceName = null;
      }

      // Reset success status
      document.getElementById('modal-form-container').style.display = 'block';
      document.getElementById('modal-success-container').style.display = 'none';

      if (!skipUrlUpdate && typeof updateURL === 'function') {
        updateURL();
      }
    }

    function closeModal(skipUrlUpdate = false) {
      document.getElementById('modal-overlay').classList.remove('active');
      document.body.style.overflow = 'auto';
      activeServiceName = null;

      if (!skipUrlUpdate && typeof updateURL === 'function') {
        updateURL();
      }
    }

    function handleOutsideModalClick(e) {
      if (e.target.id === 'modal-overlay') {
        closeModal();
      }
    }

    // SUBMIT ACTIONS
    function handleModalSubmit(e) {
      e.preventDefault();

      document.getElementById('modal-form-container').style.display = 'none';
      document.getElementById('modal-success-container').style.display = 'block';

      setTimeout(() => {
        closeModal();
        document.getElementById('modal-name').value = '';
        document.getElementById('modal-phone').value = '';
      }, 2500);
    }

    function handleLeadSubmit(e) {
      e.preventDefault();

      document.getElementById('lead-form-container').style.display = 'none';
      document.getElementById('lead-success-container').style.display = 'block';

      setTimeout(() => {
        document.getElementById('lead-form-container').style.display = 'block';
        document.getElementById('lead-success-container').style.display = 'none';
        document.getElementById('lead-name').value = '';
        document.getElementById('lead-phone').value = '';
      }, 4000);
    }

    function handleHeroLeadSubmit(e) {
      e.preventDefault();
      const formActual = document.getElementById('hero-form-actual');
      const formSuccess = document.getElementById('hero-form-success');
      if (formActual && formSuccess) {
        formActual.style.display = 'none';
        formSuccess.style.display = 'flex';

        // You could send lead data to an API here if needed:
        // const name = document.getElementById('hero-lead-name').value;
        // const phone = document.getElementById('hero-lead-phone').value;
        // const service = document.getElementById('hero-lead-service').value;

        setTimeout(() => {
          formActual.style.display = 'block';
          formSuccess.style.display = 'none';
          document.getElementById('hero-lead-name').value = '';
          document.getElementById('hero-lead-phone').value = '';
        }, 4000);
      }
    }

    // STAR RATING FOR REVIEW
    function setReviewRating(rating) {
      reviewRating = rating;
      document.querySelectorAll('#rev-rating-stars .star-select-btn').forEach(btn => {
        const starNum = parseInt(btn.getAttribute('data-rating'));
        if (starNum <= rating) {
          btn.classList.add('active');
        } else {
          btn.classList.remove('active');
        }
      });
    }

    function handleReviewSubmit(e) {
      e.preventDefault();

      const name = document.getElementById('rev-name').value;
      const service = document.getElementById('rev-service').value;
      const text = document.getElementById('rev-text').value;

      if (!name || !service || !text) return;

      const colors = ['#e63333', '#3498db', '#e74c3c', '#9b59b6', '#e67e22', '#1abc9c'];
      const randomColor = colors[Math.floor(Math.random() * colors.length)];

      const newRev = {
        name: name,
        nameKz: name,
        nameEn: name,
        avatarBg: randomColor,
        service: service,
        rating: reviewRating,
        text: text,
        textKz: text,
        textEn: text
      };

      reviewsData.unshift(newRev);
      renderReviews();

      // Reset form
      document.getElementById('rev-name').value = '';
      document.getElementById('rev-service').value = '';
      document.getElementById('rev-text').value = '';
      setReviewRating(5);
    }

    // ═══════════════════════════════════════════════════════════════
    //  PERSONAL CABINET — REAL API LOGIC
    // ═══════════════════════════════════════════════════════════════

    const API_BASE = window.location.hostname && !window.location.hostname.includes('localhost') && !window.location.hostname.includes('127.0.0.1') && window.location.protocol !== 'file:'
      ? ''
      : 'http://localhost:3030';

    let cabSmsTimerInterval = null;
    let cabSmsTimerSeconds = 60;
    let cabVerifiedPhone = '';   // phone confirmed by OTP
    let cabChatHistory = [
      { sender: 'operator', text: 'Здравствуйте! Я ваш Ассистент Иришка. Чем могу помочь?' }
    ];

    // ── Helpers ──────────────────────────────────────────────────────

    function cabSetLoading(btnId, loading, label) {
      const btn = document.getElementById(btnId);
      if (!btn) return;
      btn.disabled = loading;
      btn.innerText = loading ? 'Подождите...' : label;
    }

    function showAuthStep(step) {
      ['cab-auth-phone-step', 'cab-auth-code-step', 'cab-auth-register-step']
        .forEach(id => {
          const el = document.getElementById(id);
          if (el) el.style.display = 'none';
        });
      const target = document.getElementById(step);
      if (target) target.style.display = step === 'cab-auth-register-step' ? 'block' : 'block';
    }


    // MEGA MODAL LOGIC
    let megaActiveSection = null;    // Column 1 (Section)
    let megaActiveCategory = null;   // Column 2 (Category)
    let megaActiveSubcategory = null;// Column 3 (Subcategory / Service)
    let megaSearchQuery = '';
    let megaSortOrder = 'default';   // 'default' | 'asc' | 'desc'

    window.openMegaModal = function () {
      document.getElementById('mega-modal-overlay').classList.add('active');
      const searchInp = document.getElementById('mega-search-input');
      if (searchInp) searchInp.value = '';
      megaSearchQuery = '';
      megaSortOrder = 'default';
      const sortLabel = document.getElementById('mega-sort-label');
      const sortBtn = document.querySelector('.mega-sort-btn');
      if (sortLabel) sortLabel.textContent = 'Сортировка';
      if (sortBtn) sortBtn.innerHTML = `<i class="ri-sort-asc"></i> <span id="mega-sort-label">Сортировка</span>`;

      if (servicesData && servicesData.length > 0) {
        megaActiveSection = servicesData[0];
        megaActiveCategory = (megaActiveSection.categories && megaActiveSection.categories.length > 0) ? megaActiveSection.categories[0] : null;
        megaActiveSubcategory = (megaActiveCategory && megaActiveCategory.items && megaActiveCategory.items.length > 0) ? megaActiveCategory.items[0] : null;
      } else {
        megaActiveSection = null;
        megaActiveCategory = null;
        megaActiveSubcategory = null;
      }
      renderMegaCols();
    };

    window.closeMegaModal = function () {
      document.getElementById('mega-modal-overlay').classList.remove('active');
    };

    window.handleOutsideMegaClick = function (e) {
      if (e.target.id === 'mega-modal-overlay') closeMegaModal();
    };

    window.handleMegaSearch = function(query) {
      megaSearchQuery = query;
      if (megaActiveSection) {
        let categories = megaActiveSection.categories || [];
        if (megaSearchQuery) {
          const q = megaSearchQuery.toLowerCase().trim();
          categories = categories.filter(cat => {
            const titleMatch = (currentLang === 'RU' ? cat.title : (currentLang === 'KZ' ? cat.titleKz : cat.titleEn)).toLowerCase().includes(q);
            const subMatch = (cat.items || []).some(sub => (currentLang === 'RU' ? sub.name : (currentLang === 'KZ' ? sub.nameKz : sub.name)).toLowerCase().includes(q));
            return titleMatch || subMatch;
          });
        }
        if (categories.length > 0) {
          if (!categories.includes(megaActiveCategory)) {
            megaActiveCategory = categories[0];
          }
        } else {
          megaActiveCategory = null;
        }

        if (megaActiveCategory) {
          let subs = megaActiveCategory.items || [];
          if (megaSearchQuery) {
            const q = megaSearchQuery.toLowerCase().trim();
            subs = subs.filter(sub => (currentLang === 'RU' ? sub.name : (currentLang === 'KZ' ? sub.nameKz : sub.name)).toLowerCase().includes(q));
          }
          if (subs.length > 0) {
            if (!subs.includes(megaActiveSubcategory)) {
              megaActiveSubcategory = subs[0];
            }
          } else {
            megaActiveSubcategory = null;
          }
        } else {
          megaActiveSubcategory = null;
        }
      }
      renderMegaCols();
    };

    window.toggleMegaSort = function() {
      const btn = document.querySelector('.mega-sort-btn');
      const label = document.getElementById('mega-sort-label');
      if (megaSortOrder === 'default') {
        megaSortOrder = 'asc';
        label.textContent = 'А-Я';
        btn.innerHTML = `<i class="ri-sort-alphabet-asc"></i> <span id="mega-sort-label">А-Я</span>`;
      } else if (megaSortOrder === 'asc') {
        megaSortOrder = 'desc';
        label.textContent = 'Я-А';
        btn.innerHTML = `<i class="ri-sort-alphabet-desc"></i> <span id="mega-sort-label">Я-А</span>`;
      } else {
        megaSortOrder = 'default';
        label.textContent = 'По умолч.';
        btn.innerHTML = `<i class="ri-sort-asc"></i> <span id="mega-sort-label">По умолч.</span>`;
      }
      renderMegaCols();
    };

    function renderMegaCol4() {
      const col4 = document.getElementById('mega-col-4');
      if (!col4) return;
      
      if (!megaActiveSubcategory) {
        col4.style.display = 'flex';
        col4.style.alignItems = 'center';
        col4.style.justifyContent = 'center';
        col4.innerHTML = `
          <div style="color: var(--text-muted); font-size: 13px; text-align: center; padding: 20px;">
            ${currentLang === 'RU' ? 'Выберите услугу для просмотра деталей' : (currentLang === 'KZ' ? 'Мәліметтерді көру үшін қызметті таңдаңыз' : 'Select service to view details')}
          </div>
        `;
        return;
      }
      
      const name = currentLang === 'RU' ? megaActiveSubcategory.name : (currentLang === 'KZ' ? megaActiveSubcategory.nameKz : megaActiveSubcategory.name);

      const imgs = [
        "https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=600&q=80",
        "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=600&q=80",
        "https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=600&q=80",
        "https://images.unsplash.com/photo-1621905252507-b35492cc74b4?w=600&q=80",
        "https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=600&q=80"
      ];
      const img = imgs[megaActiveSubcategory.name.length % imgs.length];

      col4.style.display = 'block';
      col4.innerHTML = `
        <div class="mega-detail-card">
          <div class="mega-detail-img-wrap">
            <div class="mega-detail-img" style="background-image: url('${img}')"></div>
          </div>
          <div class="mega-detail-content">
            <div class="mega-detail-title">${name}</div>
            <div class="mega-detail-desc">${megaActiveSubcategory.desc || 'Профессиональная услуга от сертифицированных мастеров. Быстро, качественно и с гарантией.'}</div>
            
            <div class="mega-info-grid">
              <div class="mega-info-box">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                <div class="mega-info-text">
                  <span class="mega-info-label">${currentLang === 'RU' ? 'Время работы' : (currentLang === 'KZ' ? 'Жұмыс уақыты' : 'Duration')}</span>
                  <span class="mega-info-val">${megaActiveSubcategory.time}</span>
                </div>
              </div>
              <div class="mega-info-box">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                <div class="mega-info-text">
                  <span class="mega-info-label">${currentLang === 'RU' ? 'Гарантия' : (currentLang === 'KZ' ? 'Кепілдік' : 'Warranty')}</span>
                  <span class="mega-info-val">${megaActiveSubcategory.warr}</span>
                </div>
              </div>
            </div>

            <div class="mega-price-box">
              <span class="mega-price-label">${currentLang === 'RU' ? 'Стоимость работы' : (currentLang === 'KZ' ? 'Жұмыс құны' : 'Price')}</span>
              <span class="mega-price-val">${megaActiveSubcategory.price}</span>
            </div>

            <div class="mega-actions">
              <button class="review-submit-btn" style="padding: 14px; cursor: pointer;" onclick="navigateThematic('${megaActiveSection.id}', '${megaActiveCategory.id}', '${megaActiveSubcategory.id}')">
                ${currentLang === 'RU' ? 'Заказать' : (currentLang === 'KZ' ? 'Тапсырыс беру' : 'Order')}
              </button>
              <a href="https://wa.me/77058462749?text=${encodeURIComponent('Здравствуйте! Хочу заказать услугу: ' + name)}" target="_blank" class="review-submit-btn" style="padding: 14px; background: #25D366; color: #fff; border: none; text-align: center; text-decoration: none; display: block;">
                WhatsApp
              </a>
            </div>
          </div>
        </div>
      `;
    }

    function renderMegaCols() {
      const col1 = document.getElementById('mega-col-1');
      const col2 = document.getElementById('mega-col-2');
      const col3 = document.getElementById('mega-col-3');

      if (!col1 || !col2 || !col3) return;

      // Col 1: Sections
      col1.innerHTML = '';
      servicesData.forEach(sec => {
        const btn = document.createElement('button');
        btn.className = 'mega-cat-btn' + (megaActiveSection && megaActiveSection.id === sec.id ? ' active' : '');
        btn.innerHTML = `
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            ${getIconPath(sec.iconName)}
          </svg>
          ${currentLang === 'RU' ? sec.title : (currentLang === 'KZ' ? sec.titleKz : sec.titleEn)}
        `;
        btn.onmouseenter = () => {
          if (megaActiveSection !== sec) {
            megaActiveSection = sec;
            megaActiveCategory = (sec.categories && sec.categories.length > 0) ? sec.categories[0] : null;
            megaActiveSubcategory = (megaActiveCategory && megaActiveCategory.items && megaActiveCategory.items.length > 0) ? megaActiveCategory.items[0] : null;
            renderMegaCols();
          }
        };
        btn.onclick = () => {
          navigateThematic(sec.id);
        };
        col1.appendChild(btn);
      });

      // Col 2: Categories
      col2.innerHTML = '';
      if (megaActiveSection) {
        col2.innerHTML = `
          <div style="font-size: 11px; font-weight: 700; color: var(--primary); text-transform: uppercase; margin-bottom: 12px; padding: 0 8px; letter-spacing: 0.5px;">
            📁 ${currentLang === 'RU' ? 'Категории' : (currentLang === 'KZ' ? 'Санаттар' : 'Categories')}
          </div>
        `;
        let categories = megaActiveSection.categories || [];
        if (megaSearchQuery) {
          const query = megaSearchQuery.toLowerCase().trim();
          categories = categories.filter(cat => {
            const titleMatch = (currentLang === 'RU' ? cat.title : (currentLang === 'KZ' ? cat.titleKz : cat.titleEn)).toLowerCase().includes(query);
            const subMatch = (cat.items || []).some(sub => (currentLang === 'RU' ? sub.name : (currentLang === 'KZ' ? sub.nameKz : sub.name)).toLowerCase().includes(query));
            return titleMatch || subMatch;
          });
        }
        if (megaSortOrder === 'asc') {
          categories = [...categories].sort((a, b) => {
            const tA = (currentLang === 'RU' ? a.title : (currentLang === 'KZ' ? a.titleKz : a.titleEn));
            const tB = (currentLang === 'RU' ? b.title : (currentLang === 'KZ' ? b.titleKz : b.titleEn));
            return tA.localeCompare(tB);
          });
        } else if (megaSortOrder === 'desc') {
          categories = [...categories].sort((a, b) => {
            const tA = (currentLang === 'RU' ? a.title : (currentLang === 'KZ' ? a.titleKz : a.titleEn));
            const tB = (currentLang === 'RU' ? b.title : (currentLang === 'KZ' ? b.titleKz : b.titleEn));
            return tB.localeCompare(tA);
          });
        }

        categories.forEach(cat => {
          const btn = document.createElement('button');
          btn.className = 'mega-cat-btn' + (megaActiveCategory && megaActiveCategory.id === cat.id ? ' active' : '');
          btn.style.padding = '10px 14px';
          btn.style.fontSize = '13px';
          btn.innerHTML = `
            <span style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
              ${currentLang === 'RU' ? cat.title : (currentLang === 'KZ' ? cat.titleKz : cat.titleEn)}
            </span>
          `;
          btn.onmouseenter = () => {
            if (megaActiveCategory !== cat) {
              megaActiveCategory = cat;
              megaActiveSubcategory = (cat.items && cat.items.length > 0) ? cat.items[0] : null;
              renderMegaCols();
            }
          };
          btn.onclick = () => {
            navigateThematic(megaActiveSection.id, cat.id);
          };
          col2.appendChild(btn);
        });
      }

      // Col 3: Subcategories / Services
      col3.innerHTML = '';
      if (megaActiveCategory) {
        col3.innerHTML = `
          <div style="font-size: 11px; font-weight: 700; color: var(--primary); text-transform: uppercase; margin-bottom: 12px; padding: 0 8px; letter-spacing: 0.5px;">
            🛠️ ${currentLang === 'RU' ? 'Услуги' : (currentLang === 'KZ' ? 'Қызметтер' : 'Services')}
          </div>
        `;
        let subcategories = megaActiveCategory.items || [];
        if (megaSearchQuery) {
          const query = megaSearchQuery.toLowerCase().trim();
          subcategories = subcategories.filter(sub => {
            return (currentLang === 'RU' ? sub.name : (currentLang === 'KZ' ? sub.nameKz : sub.name)).toLowerCase().includes(query);
          });
        }
        if (megaSortOrder === 'asc') {
          subcategories = [...subcategories].sort((a, b) => {
            const nA = currentLang === 'RU' ? a.name : (currentLang === 'KZ' ? a.nameKz : a.name);
            const nB = currentLang === 'RU' ? b.name : (currentLang === 'KZ' ? b.nameKz : b.name);
            return nA.localeCompare(nB);
          });
        } else if (megaSortOrder === 'desc') {
          subcategories = [...subcategories].sort((a, b) => {
            const nA = currentLang === 'RU' ? a.name : (currentLang === 'KZ' ? a.nameKz : a.name);
            const nB = currentLang === 'RU' ? b.name : (currentLang === 'KZ' ? b.nameKz : b.name);
            return nB.localeCompare(nA);
          });
        }

        subcategories.forEach(sub => {
          const btn = document.createElement('button');
          btn.className = 'mega-item-btn' + (megaActiveSubcategory && megaActiveSubcategory.id === sub.id ? ' active' : '');
          btn.innerHTML = `
            <span>${currentLang === 'RU' ? sub.name : (currentLang === 'KZ' ? sub.nameKz : sub.name)}</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>
          `;
          btn.onmouseenter = () => {
            if (megaActiveSubcategory !== sub) {
              megaActiveSubcategory = sub;
              const allBtns = col3.querySelectorAll('.mega-item-btn');
              subcategories.forEach((s, idx) => {
                if (allBtns[idx]) {
                  allBtns[idx].classList.toggle('active', s.id === sub.id);
                }
              });
              renderMegaCol4();
            }
          };
          btn.onclick = () => {
            navigateThematic(megaActiveSection.id, megaActiveCategory.id, sub.id);
          };
          col3.appendChild(btn);
        });
      }

      renderMegaCol4();
    }

    // helper for mega modal icons
    function getIconPath(name) {
      if (name === 'hammer') return '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>';
      if (name === 'wrench') return '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>';
      if (name === 'laptop') return '<rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/>';
      if (name === 'droplet') return '<path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/>';
      if (name === 'bolt') return '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>';
      if (name === 'sparkles') return '<path d="M12 3l2 5h5l-4 3 1.5 5-4.5-3.5-4.5 3.5 1.5-5-4-3h5l2-5z"/>';
      if (name === 'car') return '<rect x="3" y="10" width="18" height="10" rx="2"/><path d="M5 10l2-6h10l2 6"/>';
      if (name === 'users') return '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>';
      if (name === 'truck') return '<rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/>';
      return '<circle cx="12" cy="12" r="10"/>';
    }

    // ── Modal open / close ────────────────────────────────────────────

    window.openCabinetModal = function () {
      document.getElementById('cabinet-modal-overlay').classList.add('active');
      initCabinet();
    };

    window.closeCabinetModal = function () {
      document.getElementById('cabinet-modal-overlay').classList.remove('active');
      if (cabSmsTimerInterval) clearInterval(cabSmsTimerInterval);
    };

    window.handleOutsideCabinetClick = function (e) {
      if (e.target.id === 'cabinet-modal-overlay') closeCabinetModal();
    };

    // ── Init ──────────────────────────────────────────────────────────

    function initCabinet() {
      const token = localStorage.getItem('cab_token');
      if (token) {
        // Restore session from backend
        fetch(API_BASE + '/api/auth/me', {
          headers: { 'Authorization': 'Bearer ' + token }
        })
          .then(r => r.ok ? r.json() : Promise.reject())
          .then(data => showDashboard(data.user, token))
          .catch(() => {
            localStorage.removeItem('cab_token');
            localStorage.removeItem('cab_user');
            showAuthContainer();
          });
      } else {
        showAuthContainer();
      }
    }

    function showAuthContainer() {
      document.getElementById('cab-auth-container').style.display = 'flex';
      document.getElementById('cab-dashboard-container').style.display = 'none';
      showAuthStep('cab-auth-phone-step');
    }

    // ── STEP 1: Send SMS ─────────────────────────────────────────────

    window.sendSmsCode = async function () {
      const phone = document.getElementById('cab-phone-input').value.trim();
      const err = document.getElementById('cab-phone-error');
      err.style.display = 'none';

      if (phone.replace(/\D/g, '').length < 11) {
        err.innerText = 'Введите корректный номер (+7XXXXXXXXXX)';
        err.style.display = 'block';
        return;
      }

      cabSetLoading('cab-send-btn', true, 'Получить SMS-код');

      try {
        const res = await fetch(API_BASE + '/api/auth/send-sms', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ phone })
        });

        let data = {};
        const text = await res.text();
        try {
          data = JSON.parse(text);
        } catch (parseErr) { }

        if (!res.ok) {
          throw new Error(data.error || text || 'Ошибка отправки');
        }

        cabVerifiedPhone = phone;
        localStorage.setItem('cab_temp_phone', phone);

        // Show step 2
        document.getElementById('cab-code-step-desc').innerText = 'Код отправлен на ' + phone;
        document.getElementById('cab-code-input').value = '';
        document.getElementById('cab-code-error').style.display = 'none';

        // Demo-mode hint
        if (data.demo_code) {
          document.getElementById('cab-demo-code').innerText = data.demo_code;
          document.getElementById('cab-demo-hint').style.display = 'block';
        } else {
          document.getElementById('cab-demo-hint').style.display = 'none';
        }

        showAuthStep('cab-auth-code-step');
        startSmsTimer();

      } catch (e) {
        err.innerText = e.message || 'Не удалось отправить SMS. Попробуйте позже.';
        err.style.display = 'block';
      } finally {
        cabSetLoading('cab-send-btn', false, 'Получить SMS-код');
      }
    };

    window.backToPhoneStep = function () {
      showAuthStep('cab-auth-phone-step');
      if (cabSmsTimerInterval) clearInterval(cabSmsTimerInterval);
    };

    // ── SMS Timer ────────────────────────────────────────────────────

    function startSmsTimer() {
      if (cabSmsTimerInterval) clearInterval(cabSmsTimerInterval);
      cabSmsTimerSeconds = 60;
      document.getElementById('cab-sms-timer-desc').style.display = 'inline';
      document.getElementById('cab-sms-resend-btn').style.display = 'none';
      document.getElementById('cab-sms-timer').innerText = 60;

      cabSmsTimerInterval = setInterval(() => {
        cabSmsTimerSeconds--;
        document.getElementById('cab-sms-timer').innerText = cabSmsTimerSeconds;
        if (cabSmsTimerSeconds <= 0) {
          clearInterval(cabSmsTimerInterval);
          document.getElementById('cab-sms-timer-desc').style.display = 'none';
          document.getElementById('cab-sms-resend-btn').style.display = 'inline';
        }
      }, 1000);
    }

    window.resendSmsCode = function () {
      sendSmsCode();
    };

    // ── STEP 2: Verify OTP ───────────────────────────────────────────

    window.verifySmsCode = async function () {
      const phone = cabVerifiedPhone || localStorage.getItem('cab_temp_phone') || '';
      const code = document.getElementById('cab-code-input').value.trim();
      const err = document.getElementById('cab-code-error');
      err.style.display = 'none';

      if (code.length < 4) {
        err.innerText = 'Введите 4-значный код';
        err.style.display = 'block';
        return;
      }

      cabSetLoading('cab-verify-btn', true, 'Подтвердить код');

      try {
        const res = await fetch(API_BASE + '/api/auth/verify-sms', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ phone, code })
        });

        let data = {};
        const text = await res.text();
        try {
          data = JSON.parse(text);
        } catch (parseErr) { }

        if (!res.ok) {
          throw new Error(data.error || text || 'Неверный код');
        }
        if (cabSmsTimerInterval) clearInterval(cabSmsTimerInterval);

        if (data.status === 'new_user') {
          // New user — go to registration form
          cabVerifiedPhone = data.phone;
          showAuthStep('cab-auth-register-step');
        } else {
          // Existing user — go straight to dashboard
          localStorage.setItem('cab_token', data.token);
          localStorage.setItem('cab_user', JSON.stringify(data.user));
          showDashboard(data.user, data.token);
        }

      } catch (e) {
        err.innerText = e.message || 'Ошибка верификации';
        err.style.display = 'block';
      } finally {
        cabSetLoading('cab-verify-btn', false, 'Подтвердить код');
      }
    };

    // ── STEP 3: Registration ─────────────────────────────────────────

    window.submitRegistration = async function () {
      const name = document.getElementById('reg-name').value.trim();
      const email = document.getElementById('reg-email').value.trim();
      const city = document.getElementById('reg-city').value;
      const address = document.getElementById('reg-address').value.trim();
      const errBox = document.getElementById('reg-error');
      errBox.style.display = 'none';

      if (!name || !email || !city) {
        errBox.innerText = 'Пожалуйста, заполните все обязательные поля (ФИО, Email, Город)';
        errBox.style.display = 'block';
        return;
      }
      if (!email.includes('@')) {
        errBox.innerText = 'Введите корректный email-адрес';
        errBox.style.display = 'block';
        return;
      }

      cabSetLoading('reg-submit-btn', true, 'Создать аккаунт →');

      try {
        const res = await fetch(API_BASE + '/api/auth/register-phone', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            phone: cabVerifiedPhone,
            name,
            email,
            city,
            address
          })
        });

        let data = {};
        const text = await res.text();
        try {
          data = JSON.parse(text);
        } catch (parseErr) { }

        if (!res.ok) {
          throw new Error(data.error || text || 'Ошибка регистрации');
        }
        localStorage.setItem('cab_token', data.token);
        localStorage.setItem('cab_user', JSON.stringify(data.user));
        showDashboard(data.user, data.token);

      } catch (e) {
        errBox.innerText = e.message || 'Не удалось создать аккаунт. Попробуйте ещё раз.';
        errBox.style.display = 'block';
      } finally {
        cabSetLoading('reg-submit-btn', false, 'Создать аккаунт →');
      }
    };

    // ── Dashboard ────────────────────────────────────────────────────

    function showDashboard(user, token) {
      document.getElementById('cab-auth-container').style.display = 'none';
      document.getElementById('cab-dashboard-container').style.display = 'flex';

      const name = user.name || 'Пользователь';
      const initials = name.split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2);

      const cabNameEl = document.getElementById('cab-user-name');
      if (cabNameEl) cabNameEl.innerText = name;
      const cabPhoneEl = document.getElementById('cab-user-phone');
      if (cabPhoneEl) cabPhoneEl.innerText = user.phone || '';
      const cabAvatarEl = document.getElementById('cab-avatar');
      if (cabAvatarEl) cabAvatarEl.innerText = initials;

      updateLoyaltyStatusUI(user.bonuses || 0);

      if (window.pendingCabinetTab) {
        switchCabinetTab(window.pendingCabinetTab);
        window.pendingCabinetTab = null;
      } else {
        switchCabinetTab('main');
      }
      loadUserOrders(token);
    }

    window.logoutCabinet = function () {
      const token = localStorage.getItem('cab_token');
      if (token) {
        fetch(API_BASE + '/api/auth/logout', {
          method: 'POST',
          headers: { 'Authorization': 'Bearer ' + token }
        }).catch(() => { });
      }
      localStorage.removeItem('cab_token');
      localStorage.removeItem('cab_user');
      localStorage.removeItem('cab_temp_phone');
      showAuthContainer();
    };

    // ── Tabs ─────────────────────────────────────────────────────────

    window.updateLoyaltyStatusUI = function(bonuses) {
      bonuses = parseInt(bonuses) || 0;
      
      // Update basic balance fields
      const bonusEl = document.getElementById('cab-bonus-amount');
      if (bonusEl) bonusEl.innerText = bonuses;
      const statusBonusEl = document.getElementById('cab-status-bonus-amount');
      if (statusBonusEl) statusBonusEl.innerText = bonuses.toLocaleString();

      // Status levels: Gold starts at 0, Platinum is at 10000.
      let statusText = 'GOLD';
      let statusColor = '#e63333';
      let progressPercent = Math.min(100, Math.max(5, (bonuses / 10000) * 100));
      let targetText = '7 500 ₸';
      
      if (bonuses >= 10000) {
        statusText = 'PLATINUM';
        statusColor = '#3b82f6';
        targetText = 'Максимальный уровень ✨';
        progressPercent = 100;
      } else {
        const needed = 10000 - bonuses;
        targetText = needed.toLocaleString() + ' ₸';
      }

      // Update badge, text, color, progress bar
      const badgeEl = document.querySelector('.cab-sidebar [style*="STATUS"] + span, .cab-sidebar [style*="СТАТУС"] + span');
      if (badgeEl) {
        badgeEl.innerText = statusText;
        badgeEl.style.background = statusColor;
      }
      
      const statusCardEl = document.querySelector('.cab-sidebar [style*="СТАТУС"]');
      if (statusCardEl && statusCardEl.parentElement) {
        statusCardEl.parentElement.style.border = '1px solid ' + statusColor + '26';
        statusCardEl.parentElement.style.background = statusColor + '0a';
      }

      const targetEl = document.getElementById('cab-status-target');
      if (targetEl) targetEl.innerText = targetText;

      const progressEl = document.getElementById('cab-status-progress');
      if (progressEl) {
        progressEl.style.width = progressPercent + '%';
        progressEl.style.background = statusColor;
      }
      
      const statusBonusValEl = document.getElementById('cab-status-bonus-amount');
      if (statusBonusValEl) {
        statusBonusValEl.style.color = statusColor;
      }
      
      // Update visual card design dynamically
      const cardVisual = document.getElementById('loyalty-card-visual');
      if (cardVisual) {
        if (bonuses >= 10000) {
          cardVisual.style.background = 'linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%)';
          cardVisual.style.border = '1px solid rgba(59, 130, 246, 0.4)';
          cardVisual.innerHTML = `
            <div style="position: absolute; top: -20px; right: -20px; width: 150px; height: 150px; background: radial-gradient(circle, rgba(59, 130, 246, 0.15) 0%, transparent 70%); filter: blur(20px);"></div>
            <div style="display: flex; flex-direction: column; gap: 14px; z-index: 2;">
              <div style="font-size: 10px; text-transform: uppercase; font-weight: 800; color: rgba(255,255,255,0.5); letter-spacing: 1.5px;">БАЛАНС БОНУСОВ</div>
              <div style="display: flex; align-items: center; gap: 10px;">
                <span id="cab-bonus-amount" style="font-size: 42px; font-weight: 800; color: #fff; font-family: var(--font-heading); text-shadow: 0 2px 10px rgba(0,0,0,0.3);">${bonuses.toLocaleString()}</span>
                <span style="font-size: 28px; animation: float-sparkle 3s ease-in-out infinite; display: inline-block;">✨</span>
              </div>
              <div style="font-size: 13px; color: rgba(255,255,255,0.7); line-height: 1.6; max-width: 420px;">
                Поздравляем! У вас активирован статус <strong>PLATINUM</strong>. Получайте 10% кэшбэк и приоритетный выезд мастера за 30 минут.
              </div>
              <button onclick="openQrScannerModal()" class="cab-bonus-scan-btn" style="background: #3b82f6; border: none; border-radius: 10px; padding: 12px 20px; color: #fff; font-size: 14px; font-weight: 700; cursor: pointer; display: flex; align-items: center; gap: 10px; transition: all 0.2s; outline: none; margin-top: 12px; font-family: var(--font-sans); box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);">
                <i class="ri-qr-scan-2-line" style="font-size: 16px;"></i>
                Сканировать QR-код с чека
              </button>
            </div>
            <div style="width: 100px; height: 100px; border-radius: 50%; border: 2px solid rgba(59, 130, 246, 0.2); display: flex; align-items: center; justify-content: center; background: rgba(59, 130, 246, 0.05); flex-shrink: 0; z-index: 2; margin-right: 12px; position: relative;">
              <div style="width: 76px; height: 76px; border-radius: 50%; border: 1.5px dashed rgba(59, 130, 246, 0.4); display: flex; align-items: center; justify-content: center;">
                <i class="ri-vip-crown-line" style="font-size: 36px; color: #3b82f6;"></i>
              </div>
            </div>
          `;
        } else {
          cardVisual.style.background = 'linear-gradient(135deg, #022c22 0%, #064e3b 50%, #022c22 100%)';
          cardVisual.style.border = '1px solid rgba(16, 185, 129, 0.3)';
          cardVisual.innerHTML = `
            <div style="position: absolute; top: -20px; right: -20px; width: 150px; height: 150px; background: radial-gradient(circle, rgba(16, 185, 129, 0.15) 0%, transparent 70%); filter: blur(20px);"></div>
            <div style="display: flex; flex-direction: column; gap: 14px; z-index: 2;">
              <div style="font-size: 10px; text-transform: uppercase; font-weight: 800; color: rgba(255,255,255,0.5); letter-spacing: 1.5px;">БАЛАНС БОНУСОВ</div>
              <div style="display: flex; align-items: center; gap: 10px;">
                <span id="cab-bonus-amount" style="font-size: 42px; font-weight: 800; color: #fff; font-family: var(--font-heading); text-shadow: 0 2px 10px rgba(0,0,0,0.3);">${bonuses.toLocaleString()}</span>
                <span style="font-size: 28px; animation: float-sparkle 3s ease-in-out infinite; display: inline-block;">✨</span>
              </div>
              <div style="font-size: 13px; color: rgba(255,255,255,0.7); line-height: 1.6; max-width: 420px;">
                Ваш текущий статус — <strong>EMERALD</strong>. Накапливайте 10 000 бонусов для перехода на уровень Platinum и получения кэшбэка 10%.
              </div>
              <button onclick="openQrScannerModal()" class="cab-bonus-scan-btn" style="background: #10b981; border: none; border-radius: 10px; padding: 12px 20px; color: #fff; font-size: 14px; font-weight: 700; cursor: pointer; display: flex; align-items: center; gap: 10px; transition: all 0.2s; outline: none; margin-top: 12px; font-family: var(--font-sans); box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);">
                <i class="ri-qr-scan-2-line" style="font-size: 16px;"></i>
                Сканировать QR-код с чека
              </button>
            </div>
            <div style="width: 100px; height: 100px; border-radius: 50%; border: 2px solid rgba(16, 185, 129, 0.2); display: flex; align-items: center; justify-content: center; background: rgba(16, 185, 129, 0.05); flex-shrink: 0; z-index: 2; margin-right: 12px; position: relative;">
              <div style="width: 76px; height: 76px; border-radius: 50%; border: 1.5px dashed rgba(16, 185, 129, 0.4); display: flex; align-items: center; justify-content: center;">
                <i class="ri-shield-user-line" style="font-size: 36px; color: #10b981;"></i>
              </div>
            </div>
          `;
        }
      }
    };

    window.renderBonusesTab = function() {
      const rowsContainer = document.getElementById('cab-bonus-history-rows');
      if (!rowsContainer) return;

      const user = JSON.parse(localStorage.getItem('cab_user') || '{}');
      const totalBonuses = user.bonuses || 0;

      let html = '';
      
      html += `
        <tr style="border-bottom: 1px solid #222226;">
          <td style="padding: 12px 16px; color: #a1a1aa;">14.05.2026</td>
          <td style="padding: 12px 16px; color: #fff; font-weight: 600;">Регистрация в программе лояльности</td>
          <td style="padding: 12px 16px; color: #10b981;"><span style="background: rgba(16,185,129,0.1); padding: 2px 8px; border-radius: 6px; font-size: 11px;">Выполнено</span></td>
          <td style="padding: 12px 16px; color: #10b981; font-weight: 700; text-align: right;">+1 500 ₸</td>
        </tr>
      `;

      let remainder = totalBonuses - 1500;
      if (remainder > 0) {
        let qrScansCount = Math.floor(remainder / 1000);
        let orderBonuses = remainder % 1000;

        for (let i = 0; i < qrScansCount; i++) {
          html = `
            <tr style="border-bottom: 1px solid #222226;">
              <td style="padding: 12px 16px; color: #a1a1aa;">Сегодня</td>
              <td style="padding: 12px 16px; color: #fff; font-weight: 600;">Сканирование QR-кода с чека</td>
              <td style="padding: 12px 16px; color: #10b981;"><span style="background: rgba(16,185,129,0.1); padding: 2px 8px; border-radius: 6px; font-size: 11px;">Выполнено</span></td>
              <td style="padding: 12px 16px; color: #10b981; font-weight: 700; text-align: right;">+1 000 ₸</td>
            </tr>
          ` + html;
        }

        if (orderBonuses > 0) {
          html = `
            <tr style="border-bottom: 1px solid #222226;">
              <td style="padding: 12px 16px; color: #a1a1aa;">Вчера</td>
              <td style="padding: 12px 16px; color: #fff; font-weight: 600;">Бонусы за завершенный заказ #3891</td>
              <td style="padding: 12px 16px; color: #10b981;"><span style="background: rgba(16,185,129,0.1); padding: 2px 8px; border-radius: 6px; font-size: 11px;">Выполнено</span></td>
              <td style="padding: 12px 16px; color: #10b981; font-weight: 700; text-align: right;">+${orderBonuses.toLocaleString()} ₸</td>
            </tr>
          ` + html;
        }
      }

      rowsContainer.innerHTML = html;
    };

    window.switchCabinetTab = function (tab) {
      ['main', 'orders', 'profile', 'chat', 'warranties', 'bonuses'].forEach(t => {
        const c = document.getElementById('cab-tab-content-' + t);
        if (c) c.style.display = 'none';
        const b = document.getElementById('cab-tab-btn-' + t);
        if (b) b.classList.remove('active');
      });
      const content = document.getElementById('cab-tab-content-' + tab);
      if (content) content.style.display = tab === 'chat' ? 'flex' : 'block';
      const btn = document.getElementById('cab-tab-btn-' + tab);
      if (btn) btn.classList.add('active');

      if (tab === 'orders') {
        loadUserOrders(localStorage.getItem('cab_token'));
      } else if (tab === 'profile') {
        initProfileForm();
      } else if (tab === 'chat') {
        renderChatMessages();
      } else if (tab === 'warranties') {
        renderWarranties();
      } else if (tab === 'bonuses') {
        renderBonusesTab();
      }
    };

    // ── Orders ───────────────────────────────────────────────────────

    function loadUserOrders(token) {
      if (!token) return;
      fetch(API_BASE + '/api/callbacks', {
        headers: { 'Authorization': 'Bearer ' + token }
      })
        .then(r => r.ok ? r.json() : [])
        .then(orders => {
          localStorage.setItem('cab_orders', JSON.stringify(orders || []));
          renderActiveOrders();
          renderAllOrders();
          // Render warranties whenever orders are loaded
          renderWarranties();
        })
        .catch(() => renderActiveOrders());
    }

    // ── QR Scanner & Warranty System (Real Bonus Feature) ────────────

    window.openQrScannerModal = function() {
      document.getElementById('qr-scanner-modal-overlay').classList.add('active');
      // Reset scanner overlay elements
      document.getElementById('qr-scanner-viewfinder').style.display = 'flex';
      document.getElementById('qr-scanner-success-screen').style.display = 'none';
      const triggerBtn = document.getElementById('qr-trigger-btn');
      if (triggerBtn) {
        triggerBtn.disabled = false;
        triggerBtn.style.opacity = '1';
        triggerBtn.innerText = 'Сканировать чек';
      }
    };

    window.closeQrScannerModal = function() {
      document.getElementById('qr-scanner-modal-overlay').classList.remove('active');
    };

    window.closeQrScannerModalOutside = function(e) {
      if (e.target.id === 'qr-scanner-modal-overlay') closeQrScannerModal();
    };

    window.simulateQrScanSuccess = function() {
      const triggerBtn = document.getElementById('qr-trigger-btn');
      if (triggerBtn) {
        triggerBtn.disabled = true;
        triggerBtn.style.opacity = '0.5';
        triggerBtn.innerHTML = `<i class="ri-loader-4-line ri-spin"></i> Анализ QR-кода...`;
      }
      
      const statusText = document.getElementById('qr-scanner-status');
      if (statusText) statusText.innerHTML = `<i class="ri-loader-4-line ri-spin"></i> Декодирование данных...`;

      // After 1.5 seconds, call API to add bonuses and update UI
      setTimeout(() => {
        const token = localStorage.getItem('cab_token');
        if (!token) return;

        fetch(API_BASE + '/api/auth/add-bonuses', {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
          },
          body: JSON.stringify({ amount: 1000 })
        })
        .then(res => res.json())
        .then(data => {
          if (data.status === 'success') {
            // Update local user object
            let localUser = JSON.parse(localStorage.getItem('cab_user') || '{}');
            localUser.bonuses = data.user.bonuses;
            localStorage.setItem('cab_user', JSON.stringify(localUser));

            // Update UI elements
            updateLoyaltyStatusUI(data.user.bonuses);
            renderBonusesTab();

            // Show success screen in scanner modal
            document.getElementById('qr-scanner-viewfinder').style.display = 'none';
            document.getElementById('qr-scanner-success-screen').style.display = 'flex';

            // Beep sound (using web audio API!)
            playScannerBeep();

            // Refresh warranties just in case
            renderWarranties();
          } else {
            alert('Ошибка при начислении бонусов: ' + (data.error || 'Неизвестная ошибка'));
          }
        })
        .catch(err => {
          console.error(err);
          alert('Сетевая ошибка при сканировании');
        });
      }, 1500);
    };

    function playScannerBeep() {
      try {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioCtx.createOscillator();
        const gainNode = audioCtx.createGain();
        oscillator.connect(gainNode);
        gainNode.connect(audioCtx.destination);
        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(1200, audioCtx.currentTime); // Beep frequency
        gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime);
        oscillator.start();
        oscillator.stop(audioCtx.currentTime + 0.15); // Beep duration
      } catch (e) {
        console.log("Audio not supported or allowed", e);
      }
    }

    function renderWarranties() {
      const list = document.getElementById('cab-warranties-list');
      if (!list) return;
      
      const orders = JSON.parse(localStorage.getItem('cab_orders') || '[]');
      const completed = orders.filter(o => o.status === 'completed');
      
      let html = '';
      
      // If there are completed orders, render them.
      // We also render at least one mockup active warranty so the screen is beautiful.
      const warrantiesToRender = [...completed];
      
      // Add a mockup warranty if empty or to demonstrate
      if (warrantiesToRender.length === 0) {
        warrantiesToRender.push({
          id: 9999,
          service: 'Ремонт стиральной машины Bosch',
          city: 'Алматы',
          created_at: new Date(Date.now() - 30 * 24 * 3600 * 1000).toISOString(), // 30 days ago
          status: 'completed',
          comment: 'Замена сливного насоса и амортизаторов. Установлены оригинальные запчасти Bosch.'
        });
      }
      
      warrantiesToRender.forEach(w => {
        const date = new Date(w.created_at);
        const dateStr = date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' });
        
        // Expiry date (1 year later)
        const expiryDate = new Date(date);
        expiryDate.setFullYear(expiryDate.getFullYear() + 1);
        const expiryStr = expiryDate.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' });
        
        // Serial number
        const serial = 'GT-' + String(100000 + w.id).substring(1) + '-' + date.getFullYear();

        html += `
          <div style="background: linear-gradient(145deg, #181920 0%, #111216 100%); border: 1px solid rgba(212, 175, 55, 0.15); border-radius: 16px; padding: 20px; box-shadow: 0 6px 20px rgba(0,0,0,0.2); position: relative; overflow: hidden; display: flex; flex-direction: column; gap: 14px; font-family: var(--font-sans); text-align: left;">
            <!-- Golden top ribbon -->
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, #d4af37 0%, #f3e5ab 50%, #d4af37 100%);"></div>
            
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
              <div>
                <span style="font-family: monospace; font-size: 11px; text-transform: uppercase; color: #d4af37; font-weight: 700; letter-spacing: 1px; background: rgba(212,175,55,0.08); padding: 4px 8px; border-radius: 4px; border: 1px solid rgba(212,175,55,0.2);">
                  ${serial}
                </span>
                <h4 style="font-family: var(--font-heading); font-size: 16px; font-weight: 800; color: #fff; margin-top: 8px; margin-bottom: 4px;">
                  ${w.service}
                </h4>
                <div style="font-size: 12px; color: var(--text-muted);">
                  Выдан: ${dateStr} &nbsp;•&nbsp; Город: ${w.city}
                </div>
              </div>
              
              <div style="display: flex; align-items: center; gap: 6px; background: rgba(34,197,94,0.08); border: 1px solid rgba(34,197,94,0.2); border-radius: 30px; padding: 4px 12px; font-size: 12px; font-weight: 700; color: #22c55e; text-transform: uppercase;">
                <span style="width: 6px; height: 6px; background: #22c55e; border-radius: 50%; display: inline-block;"></span>
                Действителен
              </div>
            </div>

            <div style="border-top: 1px dashed rgba(255,255,255,0.06); padding-top: 12px; display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px;">
              <div>
                <span style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Срок гарантии</span>
                <div style="font-size: 13px; font-weight: 700; color: #fff; margin-top: 2px;">12 месяцев (1 год)</div>
              </div>
              <div>
                <span style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Истекает</span>
                <div style="font-size: 13px; font-weight: 700; color: #f43f5e; margin-top: 2px;">${expiryStr}</div>
              </div>
              <div>
                <span style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Исполнитель</span>
                <div style="font-size: 13px; font-weight: 700; color: #fff; margin-top: 2px;">Мастерская HUB MASTER</div>
              </div>
            </div>

            <div style="font-size: 12px; color: var(--text-muted); background: rgba(255,255,255,0.02); padding: 10px 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.04); font-style: italic;">
              "${w.comment || 'Мастером выполнен весь необходимый перечень пусконаладочных и ремонтных работ. Замечаний не обнаружено.'}"
            </div>

            <div style="display: flex; gap: 10px; justify-content: flex-end; margin-top: 4px;">
              <button onclick="downloadWarrantyPDF('${serial}', '${w.service.replace(/'/g, "\\'")}', '${dateStr}', '${expiryStr}')" class="review-submit-btn" style="padding: 8px 16px; font-size: 12px; background: rgba(212,175,55,0.1); border: 1px solid rgba(212,175,55,0.3); color: #d4af37; border-radius: 8px; display: flex; align-items: center; gap: 6px; cursor: pointer;">
                <i class="ri-file-pdf-line"></i>
                Скачать PDF
              </button>
            </div>
          </div>
        `;
      });
      
      list.innerHTML = html;
    }

    window.downloadWarrantyPDF = function(serial, service, dateStr, expiryStr) {
      const printWindow = window.open('', '_blank');
      printWindow.document.write(`
        <html>
        <head>
          <title>Гарантийный талон ${serial}</title>
          <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&display=swap" rel="stylesheet">
          <style>
            body { font-family: 'Montserrat', sans-serif; padding: 40px; color: #111; line-height: 1.6; }
            .cert-box { border: 10px double #d4af37; padding: 40px; border-radius: 12px; position: relative; max-width: 650px; margin: 0 auto; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
            .header { text-align: center; margin-bottom: 30px; }
            .logo { font-size: 24px; font-weight: 800; color: #111; letter-spacing: 1px; }
            .title { font-size: 22px; font-weight: 800; color: #d4af37; text-transform: uppercase; margin-top: 10px; letter-spacing: 2px; }
            .serial { font-family: monospace; font-size: 14px; color: #666; margin-top: 5px; font-weight: bold; }
            .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 30px; border-top: 1.5px dashed #ddd; padding-top: 20px; }
            .label { font-size: 11px; text-transform: uppercase; color: #777; font-weight: 600; }
            .value { font-size: 15px; font-weight: 700; color: #111; margin-top: 2px; }
            .footer-text { font-size: 11px; color: #888; text-align: center; margin-top: 40px; border-top: 1px solid #eee; padding-top: 20px; }
            .stamp { position: absolute; bottom: 40px; right: 40px; width: 90px; height: 90px; border: 3px double #d4af37; border-radius: 50%; display: flex; align-items: center; justify-content: center; text-align: center; font-size: 8px; color: #d4af37; font-weight: 800; transform: rotate(-15deg); opacity: 0.8; text-transform: uppercase; line-height: 1.2; }
          </style>
        </head>
        <body onload="window.print()">
          <div class="cert-box">
            <div class="header">
              <div class="logo">HUB MASTER</div>
              <div class="title">Электронный гарантийный талон</div>
              <div class="serial">${serial}</div>
            </div>
            
            <div style="margin-top: 20px;">
              <span class="label">Вид ремонтных работ / Услуга</span>
              <div class="value" style="font-size: 18px; color: #000;">${service}</div>
            </div>

            <div class="grid">
              <div>
                <span class="label">Дата активации</span>
                <div class="value">${dateStr}</div>
              </div>
              <div>
                <span class="label">Статус гарантии</span>
                <div class="value" style="color: #22c55e;">АКТИВЕН / ДЕЙСТВИТЕЛЕН</div>
              </div>
              <div>
                <span class="label">Срок действия</span>
                <div class="value">12 месяцев (365 дней)</div>
              </div>
              <div>
                <span class="label">Дата окончания</span>
                <div class="value" style="color: #f43f5e;">${expiryStr}</div>
              </div>
            </div>

            <div style="margin-top: 25px; background: #f9f9f9; padding: 15px; border-radius: 8px; border: 1px solid #eaeaea;">
              <span class="label">Условия гарантии</span>
              <div style="font-size: 12px; color: #444; margin-top: 6px;">
                Настоящий талон подтверждает право на бесплатное устранение неисправностей в течение указанного срока. Гарантия распространяется на выполненные работы и замененные мастером детали.
              </div>
            </div>

            <div class="stamp">
              <div>
                HUB MASTER<br>
                ОТДЕЛ ОТК<br>
                ДЛЯ ДОКУМЕНТОВ
              </div>
            </div>

            <div class="footer-text">
              Сервисная служба HUB MASTER • Алматы, Казахстан • Поддержка: +7 (705) 846-2749
            </div>
          </div>
        </body>
        </html>
      `);
      printWindow.document.close();
    };

    const STATUS_COLORS = {
      pending: '#9b59b6',
      in_progress: '#f39c12',
      completed: '#25d366'
    };
    const STATUS_LABELS = {
      pending: 'Новая',
      in_progress: 'В работе',
      completed: 'Выполнен'
    };

    function orderCard(o) {
      const color = STATUS_COLORS[o.status] || '#888';
      const label = STATUS_LABELS[o.status] || o.status;
      const date = o.created_at ? new Date(o.created_at).toLocaleDateString('ru-RU') : '';
      return `
        <div style="background:#18181c;border:1px solid #222226;border-radius:10px;padding:14px;display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
          <div>
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
              <span style="font-size:11px;color:var(--text);font-weight:700;">#${o.id}</span>
              <span style="font-size:14px;font-weight:700;color:#fff;">${o.service || 'Заявка'}</span>
            </div>
            <div style="font-size:12px;color:var(--text);">${o.comment || o.city || ''} ${date ? '• ' + date : ''}</div>
          </div>
          <span style="font-size:12px;font-weight:700;color:#fff;background:${color};padding:4px 10px;border-radius:30px;white-space:nowrap;">${label}</span>
        </div>`;
    }

    function renderActiveOrders() {
      const orders = JSON.parse(localStorage.getItem('cab_orders') || '[]');
      const active = orders.filter(o => o.status !== 'completed');
      const el = document.getElementById('cab-active-orders');
      if (!el) return;
      el.innerHTML = active.length
        ? active.map(orderCard).join('')
        : '<div style="color:var(--text);font-size:13px;font-style:italic;padding:20px;border:1px dashed #222226;border-radius:8px;text-align:center;">Нет активных заказов</div>';
    }

    function renderAllOrders() {
      const orders = JSON.parse(localStorage.getItem('cab_orders') || '[]');
      const el = document.getElementById('cab-all-orders');
      if (!el) return;
      el.innerHTML = orders.length
        ? orders.map(orderCard).join('')
        : '<div style="color:var(--text);font-size:13px;font-style:italic;padding:20px;border:1px dashed #222226;border-radius:8px;text-align:center;">История пуста</div>';
    }

    // ── Quick Order ───────────────────────────────────────────────────

    window.createQuickOrder = async function () {
      const token = localStorage.getItem('cab_token');
      const user = JSON.parse(localStorage.getItem('cab_user') || '{}');
      const svc = document.getElementById('cab-quick-service');
      const details = document.getElementById('cab-quick-details');
      const succ = document.getElementById('cab-quick-success');

      if (!token) return;

      const service = svc.options[svc.selectedIndex].text;
      const comment = details.value.trim() || 'Без деталей';

      try {
        await fetch(API_BASE + '/api/callback', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
          },
          body: JSON.stringify({
            name: user.name || 'Клиент',
            phone: user.phone || '',
            service,
            city: user.city || '',
            comment
          })
        });
        succ.style.display = 'block';
        details.value = '';
        setTimeout(() => { succ.style.display = 'none'; }, 3000);
        loadUserOrders(token);
      } catch (e) {
        console.error('Quick order error', e);
      }
    };

    // ── Profile ───────────────────────────────────────────────────────

    function initProfileForm() {
      const user = JSON.parse(localStorage.getItem('cab_user') || '{}');
      const nameEl = document.getElementById('cab-profile-name');
      const emailEl = document.getElementById('cab-profile-email');
      const cityEl = document.getElementById('cab-profile-city');
      if (nameEl) nameEl.value = user.name || '';
      if (emailEl) emailEl.value = user.email || '';
      if (cityEl) cityEl.value = user.city || 'almaty';
      renderAddresses();
    }

    window.saveCabinetProfile = async function () {
      const token = localStorage.getItem('cab_token');
      const name = document.getElementById('cab-profile-name').value.trim();
      const city = document.getElementById('cab-profile-city').value;
      const user = JSON.parse(localStorage.getItem('cab_user') || '{}');
      const success = document.getElementById('cab-profile-success');

      if (!token || !name || !city) return;

      try {
        const res = await fetch(API_BASE + '/api/auth/profile', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
          },
          body: JSON.stringify({ name, phone: user.phone || '', city, password: '' })
        });
        if (res.ok) {
          const data = await res.json();
          localStorage.setItem('cab_user', JSON.stringify(data.user));
          document.getElementById('cab-user-name').innerText = name;
          const initials = name.split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2);
          document.getElementById('cab-avatar').innerText = initials;
          success.style.display = 'block';
          setTimeout(() => { success.style.display = 'none'; }, 3000);
        }
      } catch (e) { console.error(e); }
    };

    // ── Addresses ─────────────────────────────────────────────────────

    function renderAddresses() {
      const list = document.getElementById('cab-address-list');
      const addresses = JSON.parse(localStorage.getItem('cab_addresses') || '[]');
      if (!list) return;
      if (addresses.length === 0) {
        list.innerHTML = '<div style="color:var(--text);font-size:12px;font-style:italic;">Адреса не сохранены</div>';
        return;
      }
      list.innerHTML = addresses.map((addr, idx) => `
        <div class="cab-address-item" style="margin-bottom:6px;">
          <span>${addr}</span>
          <button onclick="deleteCabinetAddress(${idx})" class="cab-address-delete">Удалить</button>
        </div>`).join('');
    }

    window.deleteCabinetAddress = function (idx) {
      const addresses = JSON.parse(localStorage.getItem('cab_addresses') || '[]');
      addresses.splice(idx, 1);
      localStorage.setItem('cab_addresses', JSON.stringify(addresses));
      renderAddresses();
    };

    window.addCabinetAddress = function () {
      const input = document.getElementById('cab-new-address');
      const text = input.value.trim();
      if (!text) return;
      const addresses = JSON.parse(localStorage.getItem('cab_addresses') || '[]');
      addresses.push(text);
      localStorage.setItem('cab_addresses', JSON.stringify(addresses));
      input.value = '';
      renderAddresses();
    };

    // ── Chat ──────────────────────────────────────────────────────────

    function renderChatMessages() {
      const container = document.getElementById('cab-chat-messages');
      if (!container) return;
      container.innerHTML = cabChatHistory.map(m => `
        <div class="cab-chat-msg ${m.sender}">${m.text}</div>`).join('');
      container.scrollTop = container.scrollHeight;
    }

    window.sendCabinetChatMessage = function () {
      const input = document.getElementById('cab-chat-input');
      const text = input.value.trim();
      if (!text) return;
      cabChatHistory.push({ sender: 'user', text });
      input.value = '';
      renderChatMessages();

      let replyText = clientBotConfig.fallback || 'Спасибо! Специалист уже рассматривает ваш запрос.';
      if (clientBotConfig.rules && clientBotConfig.rules.length > 0) {
        const textLower = text.toLowerCase();
        for (const rule of clientBotConfig.rules) {
          if (rule.triggers && rule.triggers.some(trig => textLower.includes(trig.toLowerCase().trim()))) {
            replyText = rule.reply;
            break;
          }
        }
      }

      setTimeout(() => {
        cabChatHistory.push({ sender: 'operator', text: replyText });
        renderChatMessages();
      }, 1200);
    };
  