import { useState, useEffect, useRef } from 'react';
import { servicesData, initialReviews } from './data/servicesData';
import './App.css';

// SVG Icons helper component to keep markup clean
const Icon = ({ name, className = "" }) => {
  switch (name) {
    case 'hammer':
      return (
        <svg className={className} viewBox="0 0 24 24">
          <path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z"/>
        </svg>
      );
    case 'wrench':
      return (
        <svg className={className} viewBox="0 0 24 24">
          <path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z"/>
        </svg>
      );
    case 'laptop':
      return (
        <svg className={className} viewBox="0 0 24 24">
          <rect x="2" y="3" width="20" height="14" rx="2"/>
          <path d="M8 21h8M12 17v4"/>
        </svg>
      );
    case 'droplet':
      return (
        <svg className={className} viewBox="0 0 24 24">
          <path d="M12 22s-8-4.5-8-11.8A8 8 0 0112 2a8 8 0 018 8.2c0 7.3-8 11.8-8 11.8z"/>
          <circle cx="12" cy="10" r="3"/>
        </svg>
      );
    case 'bolt':
      return (
        <svg className={className} viewBox="0 0 24 24">
          <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
        </svg>
      );
    case 'sparkles':
      return (
        <svg className={className} viewBox="0 0 24 24">
          <path d="M12 3v1M12 20v1M4 12H3M21 12h-1M18.36 5.64l-.7.7M6.34 17.66l-.7.7M18.36 17.66l-.7-.7M6.34 6.34l-.7-.7M12 8a4 4 0 100 8 4 4 0 000-8z"/>
        </svg>
      );
    case 'car':
      return (
        <svg className={className} viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="10"/>
          <path d="M12 8v4M12 16h.01"/>
        </svg>
      );
    case 'users':
      return (
        <svg className={className} viewBox="0 0 24 24">
          <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/>
          <circle cx="9" cy="7" r="4"/>
          <path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/>
        </svg>
      );
    case 'truck':
      return (
        <svg className={className} viewBox="0 0 24 24">
          <rect x="1" y="3" width="15" height="13" rx="2"/>
          <path d="M16 8h5l2 4v3h-7V8zM5.5 21a1.5 1.5 0 100-3 1.5 1.5 0 000 3zM18.5 21a1.5 1.5 0 100-3 1.5 1.5 0 000 3z"/>
        </svg>
      );
    case 'check':
      return (
        <svg className={className} viewBox="0 0 24 24" stroke="currentColor" fill="none" strokeWidth="2.5">
          <polyline points="20 6 9 17 4 12"/>
        </svg>
      );
    case 'star':
      return (
        <svg className={className} viewBox="0 0 24 24" stroke="none" fill="currentColor">
          <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
        </svg>
      );
    case 'time':
      return (
        <svg className={className} viewBox="0 0 24 24" stroke="currentColor" fill="none" strokeWidth="2">
          <circle cx="12" cy="12" r="10"/>
          <polyline points="12 6 12 12 16 14"/>
        </svg>
      );
    case 'phone':
      return (
        <svg className={className} viewBox="0 0 24 24" stroke="currentColor" fill="none" strokeWidth="2">
          <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81a19.79 19.79 0 01-3.07-8.68A2 2 0 012 1h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 8.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/>
        </svg>
      );
    case 'user':
      return (
        <svg className={className} viewBox="0 0 24 24" stroke="currentColor" fill="none" strokeWidth="2">
          <circle cx="12" cy="8" r="4"/>
          <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/>
        </svg>
      );
    case 'sun':
      return (
        <svg className={className} viewBox="0 0 24 24" fill="none" strokeWidth="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
      );
    case 'moon':
      return (
        <svg className={className} viewBox="0 0 24 24" fill="none" strokeWidth="2"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/></svg>
      );
    default:
      return null;
  }
};

function App() {
  const [lang, setLang] = useState('RU');
  const [city, setCity] = useState('Алматы');
  const [theme, setTheme] = useState('dark');
  const [selectedServiceId, setSelectedServiceId] = useState('furniture');
  const [reviews, setReviews] = useState(initialReviews);
  
  // Modals and form states
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalService, setModalService] = useState('');
  const [modalName, setModalName] = useState('');
  const [modalPhone, setModalPhone] = useState('');
  const [modalSuccess, setModalSuccess] = useState(false);

  const [leadName, setLeadName] = useState('');
  const [leadPhone, setLeadPhone] = useState('');
  const [leadService, setLeadService] = useState('furniture');
  const [leadSuccess, setLeadSuccess] = useState(false);

  // Review form states
  const [newReviewName, setNewReviewName] = useState('');
  const [newReviewService, setNewReviewService] = useState('');
  const [newReviewRating, setNewReviewRating] = useState(5);
  const [newReviewText, setNewReviewText] = useState('');

  const catalogRef = useRef(null);

  // Cabinet States
  const [isCabinetOpen, setIsCabinetOpen] = useState(false);
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [activeCabinetTab, setActiveCabinetTab] = useState('dashboard');
  
  // Login input states
  const [loginPhone, setLoginPhone] = useState('');
  const [loginCode, setLoginCode] = useState('');
  const [loginStep, setLoginStep] = useState('phone'); // 'phone' | 'code'
  const [smsTimer, setSmsTimer] = useState(0);
  const [loginError, setLoginError] = useState('');
  
  // User Cabinet data
  const [userProfile, setUserProfile] = useState({
    name: 'Алексей Иванов',
    phone: '',
    email: 'alex.ivanov@mail.ru',
    city: 'Алматы',
    addresses: ['пр. Аль-Фараби, д. 77/7, кв. 42', 'ул. Абая, д. 10, оф. 5'],
    bonuses: 2500,
    spent: 45000,
    loyaltyTier: 'Gold'
  });
  
  const [cabinetOrders, setCabinetOrders] = useState([
    {
      id: '4829',
      category: 'furniture',
      serviceName: 'Сборка шкафа-купе и комода',
      serviceNameKz: 'Купе-шкафты және комодты жинау',
      serviceNameEn: 'Wardrobe and dresser assembly',
      date: '30.05.2026',
      price: '12 000 ₸',
      status: 'assigned', // 'searching' | 'assigned' | 'completed' | 'cancelled'
      master: {
        name: 'Сергей Петров',
        rating: '4.9',
        completedCount: 1240,
        experience: 5,
        phone: '77058462749',
        avatarBg: '#3498db'
      }
    },
    {
      id: '4711',
      category: 'plumbing',
      serviceName: 'Установка смесителя на кухне',
      serviceNameKz: 'Ас үйде смесительді орнату',
      serviceNameEn: 'Kitchen faucet installation',
      date: '29.05.2026',
      price: '4 000 ₸',
      status: 'completed',
      master: {
        name: 'Данияр Сериков',
        rating: '4.8',
        completedCount: 890,
        experience: 6,
        phone: '77058462749',
        avatarBg: '#1abc9c'
      }
    },
    {
      id: '4602',
      category: 'cleaning',
      serviceName: 'Генеральная уборка квартиры',
      serviceNameKz: 'Пәтерді бас тазалау',
      serviceNameEn: 'General apartment cleaning',
      date: '12.05.2026',
      price: '15 000 ₸',
      status: 'completed',
      master: {
        name: 'Игорь Власов',
        rating: '5.0',
        completedCount: 410,
        experience: 7,
        phone: '77058462749',
        avatarBg: '#9b59b6'
      }
    }
  ]);

  const [chatMessages, setChatMessages] = useState([
    {
      sender: 'operator',
      time: '11:30',
      text: 'Здравствуйте! Вас приветствует служба поддержки HUB MASTER. Чем я могу помочь вам сегодня?'
    }
  ]);
  const [chatInput, setChatInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  
  // Fast booking states inside cabinet
  const [cabNewOrderCat, setCabNewOrderCat] = useState('furniture');
  const [cabNewOrderText, setCabNewOrderText] = useState('');
  const [cabNewOrderSuccess, setCabNewOrderSuccess] = useState(false);
  const [profileSaveSuccess, setProfileSaveSuccess] = useState(false);
  const [newAddressInput, setNewAddressInput] = useState('');

  // Load session from localStorage
  useEffect(() => {
    const savedUser = localStorage.getItem('hubmaster_user');
    if (savedUser) {
      try {
        const parsed = JSON.parse(savedUser);
        setIsAuthenticated(true);
        if (parsed.profile) setUserProfile(parsed.profile);
        if (parsed.orders) setCabinetOrders(parsed.orders);
        if (parsed.chat) setChatMessages(parsed.chat);
      } catch (e) {
        console.error(e);
      }
    }
  }, []);

  // SMS Timer countdown
  useEffect(() => {
    let interval = null;
    if (smsTimer > 0) {
      interval = setInterval(() => {
        setSmsTimer((prev) => prev - 1);
      }, 1000);
    } else {
      clearInterval(interval);
    }
    return () => clearInterval(interval);
  }, [smsTimer]);

  // Apply theme to document element
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);


  // Dictionary for localizations
  const t = {
    RU: {
      tagline: "Все нужное — в 1 клик!",
      callMaster: "Вызвать мастера",
      catalogTitle: "Каталог услуг",
      catalogSub: "Выберите категорию, чтобы ознакомиться с ценами и сделать быстрый заказ",
      orderBtn: "Заказать услугу",
      whyTitle: "Почему выбирают нас?",
      whySub: "Премиальный сервис для вашего дома и бизнеса",
      reviewsTitle: "Отзывы клиентов",
      reviewsSub: "Более 50 000 довольных клиентов — лучшее подтверждение нашей работы",
      writeReview: "Оставить отзыв",
      yourName: "Ваше имя",
      yourPhone: "Номер телефона",
      selectService: "Выберите услугу",
      reviewText: "Текст отзыва",
      submitReview: "Отправить отзыв",
      leaveRequest: "Оставьте заявку",
      leaveRequestSub: "Наш оператор перезвонит вам в течение 10 минут для уточнения деталей",
      sendRequest: "Отправить заявку",
      successTitle: "Заявка успешно принята!",
      successDesc: "Мы свяжемся с вами в течение 10 минут. Спасибо!",
      cityLabel: "Алматы",
      cabinet: "Кабинет",
      contacts: "Контакты",
      masters: "Наши мастера",
      about: "О нас",
      copyright: "© 2026 HUB MASTER. Все права защищены.",
      phoneNum: "+7 705 846 2749",
      
      // Cabinet translations
      cabinetTitle: "Личный кабинет",
      logout: "Выйти из кабинета",
      loginTitle: "Вход в личный кабинет",
      loginSub: "Введите ваш номер телефона для входа или регистрации",
      phoneLabel: "Номер телефона",
      codeLabel: "Введите 4-значный код из SMS",
      getCodeBtn: "Получить код",
      verifyBtn: "Войти в кабинет",
      resendCode: "Отправить код повторно",
      codeSentMsg: "Код отправлен на номер",
      demoCodeHint: "Для входа введите код: 1234",
      smsTimerMsg: "Повторная отправка через {time} сек",
      invalidCode: "Неверный код. Попробуйте еще раз.",
      phonePlaceholder: "Не указан",
      saveChanges: "Сохранить изменения",
      
      tabDashboard: "Главная",
      tabOrders: "Мои заказы",
      tabProfile: "Профиль",
      tabChat: "Поддержка 24/7",
      
      welcomeBack: "С возвращением",
      bonusBalance: "Бонусный баланс",
      bonusPoints: "бонусов",
      loyaltyTier: "Уровень лояльности",
      tierGold: "Золотой (10% кэшбэк)",
      tierSilver: "Серебряный (5% кэшбэк)",
      tierPlatinum: "Платиновый (15% кэшбэк)",
      nextTierProgress: "До следующего уровня (Платина): {spent} / 100 000 ₸",
      
      activeOrdersTitle: "Активные заказы",
      noActiveOrders: "У вас нет активных заказов",
      orderNumber: "Заказ №",
      orderStatus: "Статус",
      orderPrice: "Стоимость",
      orderDate: "Дата заказа",
      orderCancel: "Отменить заказ",
      orderConfirmCancel: "Вы уверены, что хотите отменить этот заказ?",
      ordersCount: "выполненных заказов",
      
      assignedMasterTitle: "Назначенный специалист",
      masterRating: "Рейтинг",
      masterExperience: "Опыт работы",
      masterExperienceVal: "лет",
      masterCompleted: "Выполнено заказов",
      masterPhone: "Связаться в WhatsApp",
      
      statusSearching: "Поиск специалиста...",
      statusAssigned: "Мастер назначен",
      statusCompleted: "Выполнен",
      statusCancelled: "Отменен",
      
      orderNewCabinetBtn: "Создать быстрый заказ",
      selectCategoryCabinet: "Выберите категорию услуги",
      orderSpecCabinet: "Что именно нужно сделать?",
      priceCabinet: "Ориентировочная цена",
      createOrderSuccess: "Заказ успешно создан! Специалист свяжется с вами.",
      
      profileName: "Ваше ФИО",
      profileEmail: "Электронная почта",
      profileCity: "Ваш город",
      profileAddress: "Адреса для выезда мастера",
      addAddressBtn: "Добавить адрес",
      profileSaveSuccess: "Профиль успешно обновлен!",
      
      chatTitle: "Онлайн-поддержка HUB MASTER",
      chatSub: "На связи оператор. Задайте любой вопрос по заказам или услугам.",
      chatInputPlaceholder: "Напишите сообщение...",
      chatSendBtn: "Отправить"
    },
    KZ: {
      tagline: "Барлық қажеттіліктер — 1 басуда!",
      callMaster: "Шеберді шақыру",
      catalogTitle: "Қызметтер каталогы",
      catalogSub: "Бағалармен танысып, жылдам тапсырыс беру үшін санатты таңдаңыз",
      orderBtn: "Қызметке тапсырыс беру",
      whyTitle: "Неліктен бізді таңдайды?",
      whySub: "Сіздің үйіңіз бен бизнесіңіз үшін премиум қызмет",
      reviewsTitle: "Клиенттердің пікірлері",
      reviewsSub: "50 000-нан астам риза клиент — біздің жұмысымыздың ең жақсы дәлелі",
      writeReview: "Пікір қалдыру",
      yourName: "Сіздің есіміңіз",
      yourPhone: "Телефон нөмірі",
      selectService: "Қызметті таңдаңыз",
      reviewText: "Пікір мәтіні",
      submitReview: "Пікірді жіберу",
      leaveRequest: "Өтінім қалдыру",
      leaveRequestSub: "Біздің оператор мәліметтерді нақтылау үшін 10 минут ішінде сізге хабарласады",
      sendRequest: "Өтінімді жіберу",
      successTitle: "Өтінім сәтті қабылданды!",
      successDesc: "Біз сібзен 10 минут ішінде хабарласамыз. Рақмет!",
      cityLabel: "Алматы",
      cabinet: "Кабинет",
      contacts: "Байланыс",
      masters: "Шеберлеріміз",
      about: "Біз туралы",
      copyright: "© 2026 HUB MASTER. Барлық құқықтар қорғалған.",
      phoneNum: "+7 705 846 2749",
      
      // Cabinet translations
      cabinetTitle: "Жеке кабинет",
      logout: "Кабинеттен шығу",
      loginTitle: "Жеке кабинетке кіру",
      loginSub: "Кіру немесе тіркелу үшін телефон нөміріңізді енгізіңіз",
      phoneLabel: "Телефон нөмірі",
      codeLabel: "SMS-тен 4 таңбалы кодты енгізіңіз",
      getCodeBtn: "Кодты алу",
      verifyBtn: "Кабинетке кіру",
      resendCode: "Кодты қайта жіберу",
      codeSentMsg: "Код нөмірге жіберілді",
      demoCodeHint: "Кіру үшін кодты енгізіңіз: 1234",
      smsTimerMsg: "Қайта жіберу {time} сек кейін",
      invalidCode: "Қате код. Қайта байқап көріңіз.",
      phonePlaceholder: "Көрсетілмеген",
      saveChanges: "Өзгерістерді сақтау",
      
      tabDashboard: "Басты бет",
      tabOrders: "Менің тапсырыстарым",
      tabProfile: "Профиль",
      tabChat: "Қолдау 24/7",
      
      welcomeBack: "Қош келдіңіз",
      bonusBalance: "Бонустық баланс",
      bonusPoints: "бонус",
      loyaltyTier: "Лоялдылық деңгейі",
      tierGold: "Алтын (10% кэшбэк)",
      tierSilver: "Күміс (5% кэшбэк)",
      tierPlatinum: "Платина (15% кэшбэк)",
      nextTierProgress: "Келесі деңгейге дейін (Платина): {spent} / 100 000 ₸",
      
      activeOrdersTitle: "Белсенді тапсырыстар",
      noActiveOrders: "Сізде белсенді тапсырыстар жоқ",
      orderNumber: "Тапсырыс №",
      orderStatus: "Мәртебесі",
      orderPrice: "Құны",
      orderDate: "Тапсырыс күні",
      orderCancel: "Тапсырысты жою",
      orderConfirmCancel: "Бұл тапсырысты жойғыңыз келетініне сенімдісіз бе?",
      ordersCount: "орындалған тапсырыстар",
      
      assignedMasterTitle: "Тағайындалған маман",
      masterRating: "Рейтинг",
      masterExperience: "Жұмыс тәжірибесі",
      masterExperienceVal: "жыл",
      masterCompleted: "Орындалған тапсырыстар",
      masterPhone: "WhatsApp арқылы хабарласу",
      
      statusSearching: "Маман ізделуде...",
      statusAssigned: "Шебер тағайындалды",
      statusCompleted: "Орындалды",
      statusCancelled: "Жоылды",
      
      orderNewCabinetBtn: "Жылдам тапсырыс жасау",
      selectCategoryCabinet: "Қызмет санатын таңдаңыз",
      orderSpecCabinet: "Дәл не істеу керек?",
      priceCabinet: "Болжалды бағасы",
      createOrderSuccess: "Тапсырыс сәтті жасалды! Шебер сізге хабарласады.",
      
      profileName: "Сіздің Т.А.Ә.",
      profileEmail: "Электрондық пошта",
      profileCity: "Қалаңыз",
      profileAddress: "Шебер келетін мекенжайлар",
      addAddressBtn: "Мекенжайды қосу",
      profileSaveSuccess: "Профиль сәтті жаңартылды!",
      
      chatTitle: "HUB MASTER онлайн-қолдау көрсету қызметі",
      chatSub: "Оператор желіде. Тапсырыстар немесе қызметтер бойынша кез келген сұрақ қойыңыз.",
      chatInputPlaceholder: "Хабарлама енгізіңіз...",
      chatSendBtn: "Жіберу"
    },
    EN: {
      tagline: "Everything you need — in 1 click!",
      callMaster: "Call a Master",
      catalogTitle: "Services Catalog",
      catalogSub: "Select a category to view prices and make a quick order",
      orderBtn: "Order Service",
      whyTitle: "Why Choose Us?",
      whySub: "Premium service for your home and business",
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
      cityLabel: "Almaty",
      cabinet: "Cabinet",
      contacts: "Contacts",
      masters: "Our Specialists",
      about: "About Us",
      copyright: "© 2026 HUB MASTER. All rights reserved.",
      phoneNum: "+7 705 846 2749",
      
      // Cabinet translations
      cabinetTitle: "Personal Cabinet",
      logout: "Log Out",
      loginTitle: "Log In to Cabinet",
      loginSub: "Enter your phone number to log in or register",
      phoneLabel: "Phone Number",
      codeLabel: "Enter 4-digit code from SMS",
      getCodeBtn: "Get Code",
      verifyBtn: "Verify & Log In",
      resendCode: "Resend Code",
      codeSentMsg: "Code sent to",
      demoCodeHint: "Enter code: 1234 to log in",
      smsTimerMsg: "Resend in {time} sec",
      invalidCode: "Invalid code. Please try again.",
      phonePlaceholder: "Not specified",
      saveChanges: "Save Changes",
      
      tabDashboard: "Dashboard",
      tabOrders: "My Orders",
      tabProfile: "Profile",
      tabChat: "Support 24/7",
      
      welcomeBack: "Welcome back",
      bonusBalance: "Bonus Balance",
      bonusPoints: "bonuses",
      loyaltyTier: "Loyalty Tier",
      tierGold: "Gold (10% cashback)",
      tierSilver: "Silver (5% cashback)",
      tierPlatinum: "Platinum (15% cashback)",
      nextTierProgress: "To next tier (Platinum): {spent} / 100,000 ₸",
      
      activeOrdersTitle: "Active Orders",
      noActiveOrders: "You have no active orders",
      orderNumber: "Order #",
      orderStatus: "Status",
      orderPrice: "Price",
      orderDate: "Order Date",
      orderCancel: "Cancel Order",
      orderConfirmCancel: "Are you sure you want to cancel this order?",
      ordersCount: "orders completed",
      
      assignedMasterTitle: "Assigned Specialist",
      masterRating: "Rating",
      masterExperience: "Experience",
      masterExperienceVal: "years",
      masterCompleted: "Orders completed",
      masterPhone: "Contact via WhatsApp",
      
      statusSearching: "Searching for tech...",
      statusAssigned: "Technician assigned",
      statusCompleted: "Completed",
      statusCancelled: "Cancelled",
      
      orderNewCabinetBtn: "Quick Order",
      selectCategoryCabinet: "Select service category",
      orderSpecCabinet: "What exactly needs to be done?",
      priceCabinet: "Estimated price",
      createOrderSuccess: "Order created successfully! A specialist will contact you.",
      
      profileName: "Your Full Name",
      profileEmail: "Email Address",
      profileCity: "Your City",
      profileAddress: "Service Addresses",
      addAddressBtn: "Add Address",
      profileSaveSuccess: "Profile updated successfully!",
      
      chatTitle: "HUB MASTER Live Support",
      chatSub: "Operator online. Ask any question about your orders or services.",
      chatInputPlaceholder: "Type a message...",
      chatSendBtn: "Send"
    }
  };

  const handleHeroPillClick = (id) => {
    setSelectedServiceId(id);
    if (catalogRef.current) {
      catalogRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleOpenModalWithService = (serviceName) => {
    setModalService(serviceName);
    setModalSuccess(false);
    setIsModalOpen(true);
  };

  const handleModalSubmit = (e) => {
    e.preventDefault();
    if (!modalName || !modalPhone) return;
    setModalSuccess(true);
    setTimeout(() => {
      setIsModalOpen(false);
      setModalName('');
      setModalPhone('');
      setModalService('');
      setModalSuccess(false);
    }, 2500);
  };

  const handleLeadSubmit = (e) => {
    e.preventDefault();
    if (!leadName || !leadPhone) return;
    setLeadSuccess(true);
    setTimeout(() => {
      setLeadName('');
      setLeadPhone('');
      setLeadSuccess(false);
    }, 4000);
  };

  const handleReviewSubmit = (e) => {
    e.preventDefault();
    if (!newReviewName || !newReviewText || !newReviewService) return;

    const newReview = {
      name: newReviewName,
      nameKz: newReviewName,
      nameEn: newReviewName,
      avatarBg: '#' + Math.floor(Math.random()*16777215).toString(16),
      service: newReviewService,
      serviceKz: newReviewService,
      serviceEn: newReviewService,
      rating: newReviewRating,
      text: newReviewText,
      textKz: newReviewText,
      textEn: newReviewText
    };

    setReviews([newReview, ...reviews]);
    setNewReviewName('');
    setNewReviewService('');
    setNewReviewText('');
    setNewReviewRating(5);
  };

  // Cabinet Handlers
  const handleCabinetClick = () => {
    if (isAuthenticated) {
      setIsCabinetOpen(true);
    } else {
      setIsLoginModalOpen(true);
      setLoginStep('phone');
      setLoginPhone('');
      setLoginCode('');
      setLoginError('');
    }
  };

  const handleSendCode = (e) => {
    e.preventDefault();
    if (!loginPhone || loginPhone.length < 10) {
      setLoginError(lang === 'RU' ? 'Введите корректный номер телефона' : lang === 'KZ' ? 'Дұрыс телефон нөмірін енгізіңіз' : 'Enter a valid phone number');
      return;
    }
    setLoginStep('code');
    setSmsTimer(60);
    setLoginError('');
  };

  const handleVerifyCode = (e) => {
    e.preventDefault();
    if (loginCode === '1234') {
      const updatedProfile = { ...userProfile, phone: loginPhone };
      setUserProfile(updatedProfile);
      setIsAuthenticated(true);
      setIsLoginModalOpen(false);
      setIsCabinetOpen(true);
      setLoginPhone('');
      setLoginCode('');
      setLoginStep('phone');
      setLoginError('');
      
      // Save session
      localStorage.setItem('hubmaster_user', JSON.stringify({
        profile: updatedProfile,
        orders: cabinetOrders,
        chat: chatMessages
      }));
    } else {
      setLoginError(t[lang].invalidCode);
    }
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setIsCabinetOpen(false);
    localStorage.removeItem('hubmaster_user');
  };

  const handleProfileSave = (e) => {
    e.preventDefault();
    localStorage.setItem('hubmaster_user', JSON.stringify({
      profile: userProfile,
      orders: cabinetOrders,
      chat: chatMessages
    }));
    setProfileSaveSuccess(true);
    setTimeout(() => {
      setProfileSaveSuccess(false);
    }, 3000);
  };

  const handleAddAddress = (e) => {
    e.preventDefault();
    if (!newAddressInput.trim()) return;
    const updatedProfile = {
      ...userProfile,
      addresses: [...userProfile.addresses, newAddressInput.trim()]
    };
    setUserProfile(updatedProfile);
    setNewAddressInput('');
    localStorage.setItem('hubmaster_user', JSON.stringify({
      profile: updatedProfile,
      orders: cabinetOrders,
      chat: chatMessages
    }));
  };

  const handleRemoveAddress = (index) => {
    const updatedAddresses = userProfile.addresses.filter((_, idx) => idx !== index);
    const updatedProfile = {
      ...userProfile,
      addresses: updatedAddresses
    };
    setUserProfile(updatedProfile);
    localStorage.setItem('hubmaster_user', JSON.stringify({
      profile: updatedProfile,
      orders: cabinetOrders,
      chat: chatMessages
    }));
  };

  const handleCancelOrder = (orderId) => {
    if (window.confirm(t[lang].orderConfirmCancel)) {
      const updated = cabinetOrders.map(order => {
        if (order.id === orderId) {
          return { ...order, status: 'cancelled' };
        }
        return order;
      });
      setCabinetOrders(updated);
      localStorage.setItem('hubmaster_user', JSON.stringify({
        profile: userProfile,
        orders: updated,
        chat: chatMessages
      }));
    }
  };

  const handleCabinetNewOrder = (e) => {
    e.preventDefault();
    if (!cabNewOrderText) return;
    
    const catData = servicesData.find(s => s.id === cabNewOrderCat);
    const catTitle = catData ? catData.title : 'Услуга';
    const catTitleKz = catData ? catData.titleKz : 'Қызмет';
    const catTitleEn = catData ? catData.titleEn : 'Service';
    
    const newOrder = {
      id: Math.floor(1000 + Math.random() * 9000).toString(),
      category: cabNewOrderCat,
      serviceName: `${catTitle}: ${cabNewOrderText}`,
      serviceNameKz: `${catTitleKz}: ${cabNewOrderText}`,
      serviceNameEn: `${catTitleEn}: ${cabNewOrderText}`,
      date: new Date().toLocaleDateString('ru-RU'),
      price: 'Расчет цены',
      status: 'searching',
      master: null
    };
    
    const updatedOrders = [newOrder, ...cabinetOrders];
    setCabinetOrders(updatedOrders);
    setCabNewOrderText('');
    setCabNewOrderSuccess(true);
    
    localStorage.setItem('hubmaster_user', JSON.stringify({
      profile: userProfile,
      orders: updatedOrders,
      chat: chatMessages
    }));
    
    setTimeout(() => {
      setCabNewOrderSuccess(false);
    }, 3000);

    // Simulate tech assignment after 10s
    setTimeout(() => {
      setCabinetOrders(currentOrders => {
        return currentOrders.map(order => {
          if (order.id === newOrder.id) {
            return {
              ...order,
              status: 'assigned',
              price: 'от 5 000 ₸',
              master: {
                name: 'Ерлан Сабитов',
                rating: '4.9',
                completedCount: 520,
                experience: 4,
                phone: '77058462749',
                avatarBg: '#e67e22'
              }
            };
          }
          return order;
        });
      });
      
      setChatMessages(prev => {
        const timeNow = new Date().toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
        const updatedChat = [
          ...prev,
          {
            sender: 'operator',
            time: timeNow,
            text: lang === 'RU' 
              ? `Специалист Ерлан Сабитов назначен по вашему заказу №${newOrder.id}. Он свяжется с вами в течение 10 минут.`
              : lang === 'KZ'
              ? `Сіздің №${newOrder.id} тапсырысыңыз бойынша Ерлан Сәбитов маман тағайындалды. Ол сізге 10 минут ішінде хабарласады.`
              : `Specialist Erlan Sabitov has been assigned to your order #${newOrder.id}. He will contact you within 10 minutes.`
          }
        ];
        // save chat to local storage
        const saved = localStorage.getItem('hubmaster_user');
        if (saved) {
          const parsed = JSON.parse(saved);
          parsed.chat = updatedChat;
          localStorage.setItem('hubmaster_user', JSON.stringify(parsed));
        }
        return updatedChat;
      });
    }, 10000);
  };

  const handleSendChatMessage = (e) => {
    e.preventDefault();
    if (!chatInput.trim()) return;
    
    const timeNow = new Date().toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
    const userMsg = {
      sender: 'user',
      time: timeNow,
      text: chatInput
    };
    
    const updatedChat = [...chatMessages, userMsg];
    setChatMessages(updatedChat);
    const userMsgText = chatInput;
    setChatInput('');
    
    localStorage.setItem('hubmaster_user', JSON.stringify({
      profile: userProfile,
      orders: cabinetOrders,
      chat: updatedChat
    }));
    
    setIsTyping(true);
    setTimeout(() => {
      setIsTyping(false);
      let replyText = '';
      const lowered = userMsgText.toLowerCase();
      
      if (lowered.includes('привет') || lowered.includes('здравствуй') || lowered.includes('hello') || lowered.includes('сәлем')) {
        replyText = lang === 'RU' 
          ? 'Здравствуйте! Рад помочь вам. Какой у вас вопрос?' 
          : lang === 'KZ'
          ? 'Сәлеметсіз бе! Сізге көмектесуге қуаныштымын. Қандай сұрағыңыз бар?'
          : 'Hello! Happy to help you. What is your question?';
      } else if (lowered.includes('заказ') || lowered.includes('мастер') || lowered.includes('order') || lowered.includes('шебер') || lowered.includes('тапсырыс')) {
        replyText = lang === 'RU'
          ? 'Статус ваших заказов вы можете посмотреть во вкладке "Мои заказы" в личном кабинете. Мастера обычно связываются за 30-40 минут до прибытия.'
          : lang === 'KZ'
          ? 'Тапсырыстарыңыздың мәртебесін жеке кабинеттегі "Менің тапсырыстарым" қосымшасынан көре аласыз. Шеберлер әдетте келуден 30-40 минут бұрын хабарласады.'
          : 'You can check your order status in the "My Orders" tab of your cabinet. Technicians usually contact you 30-40 minutes before arrival.';
      } else if (lowered.includes('цена') || lowered.includes('стоимость') || lowered.includes('баға') || lowered.includes('сколько') || lowered.includes('price') || lowered.includes('cost')) {
        replyText = lang === 'RU'
          ? 'Приблизительные тарифы указаны в каталоге услуг. Точную смету составит мастер после оценки сложности работ на месте.'
          : lang === 'KZ'
          ? 'Шамалы тарифтер қызметтер каталогында көрсетілген. Нақты сметаны шебер жұмыс орнындағы күрделілікті бағалағаннан кейін жасайды.'
          : 'Approximate rates are listed in the services catalog. The exact cost will be determined by the technician after on-site evaluation.';
      } else {
        replyText = lang === 'RU'
          ? 'Спасибо за сообщение! Я передал ваш запрос дежурному оператору. Мы перезвоним вам на указанный номер в течение 5 минут для консультации.'
          : lang === 'KZ'
          ? 'Хабарламаңызға рақмет! Мен сіздің сұранысыңызды кезекші операторға бердім. Біз сізге 5 минут ішінде кеңес беру үшін хабарласамыз.'
          : 'Thank you for your message! I have forwarded your inquiry to the operator on duty. We will call you back on your registered phone within 5 minutes.';
      }
      
      const newReply = {
        sender: 'operator',
        time: new Date().toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' }),
        text: replyText
      };
      
      const updatedChatWithReply = [...updatedChat, newReply];
      setChatMessages(updatedChatWithReply);
      
      localStorage.setItem('hubmaster_user', JSON.stringify({
        profile: userProfile,
        orders: cabinetOrders,
        chat: updatedChatWithReply
      }));
    }, 1500);
  };


  const currentServices = servicesData.find(s => s.id === selectedServiceId) || servicesData[0];

  return (
    <div className="app-container">
      {/* NAVBAR */}
      <nav className="navbar">
        <div className="max-width-wrap navbar-inner">
          <div className="logo-section">
            <div className="logo-box">
              <div className="logo-hub">HUB</div>
              <div className="logo-master">MASTER</div>
            </div>
            <div className="logo-subtitle">
              {city} • С 2018
            </div>
          </div>

          <div className="navbar-links">
            <button onClick={() => handleHeroPillClick('furniture')} className="nav-link-item active">
              {lang === 'RU' ? 'Сборка мебели' : lang === 'KZ' ? 'Жиһаз жинау' : 'Furniture Assembly'}
            </button>
            <a href="#catalog" className="nav-link-item">{t[lang].catalogTitle}</a>
            <a href="#why-choose" className="nav-link-item">{t[lang].whyTitle}</a>
            <a href="#reviews" className="nav-link-item">{t[lang].reviewsTitle}</a>
          </div>

          <div className="navbar-right">
            <button className="city-select" onClick={() => setCity(city === 'Алматы' ? 'Астана' : 'Алматы')}>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" strokeWidth="2.5">
                <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/>
                <circle cx="12" cy="9" r="2.5"/>
              </svg>
              {city} ▾
            </button>

            <div className="lang-selector">
              {['RU', 'KZ', 'EN'].map(ln => (
                <button
                  key={ln}
                  className={`lang-btn ${lang === ln ? 'active' : ''}`}
                  onClick={() => setLang(ln)}
                >
                  {ln}
                </button>
              ))}
            </div>

            <button 
              className="theme-toggle-btn" 
              onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
              aria-label="Toggle theme"
            >
              <Icon name={theme === 'dark' ? 'sun' : 'moon'} />
            </button>

            <a href="https://wa.me/77058462749" target="_blank" rel="noopener noreferrer" className="contact-phone-btn">
              <Icon name="phone" />
              {t[lang].phoneNum}
            </a>

            <button className="cabinet-btn" onClick={handleCabinetClick}>
              <Icon name="user" />
              {t[lang].cabinetTitle}
            </button>
          </div>
        </div>
      </nav>

      {/* HERO SECTION */}
      <section className="hero-section">
        <div className="max-width-wrap">
          <div className="hero-grid">
            <div className="hero-info">
              <span className="hero-badge">HUB MASTER PLATFORM</span>
              <h1 className="hero-heading">
                {lang === 'RU' ? 'Мультисервис услуг и товаров' : lang === 'KZ' ? 'Қызметтер мен тауарлар мультисервисі' : 'Multi-service for Home & Business'}
              </h1>
              <p className="hero-subtext">{t[lang].tagline}</p>
              <button 
                className="hero-cta-btn"
                onClick={() => handleOpenModalWithService('Общий вызов мастера')}
              >
                {t[lang].callMaster}
              </button>
            </div>

            <div className="hero-illustration">
              <div className="worker-background-oval"></div>
              <svg className="worker-illustration-svg" viewBox="0 0 160 240" width="160" height="240" xmlns="http://www.w3.org/2000/svg">
                {/* Body */}
                <rect x="30" y="100" width="100" height="120" rx="10" fill="#1a4fa0"/>
                <rect x="30" y="100" width="38" height="120" rx="6" fill="#c0392b"/>
                {/* Head */}
                <ellipse cx="80" cy="72" rx="30" ry="32" fill="#f5c89a"/>
                {/* Cap */}
                <rect x="48" y="38" width="64" height="26" rx="5" fill="#1a4fa0"/>
                <rect x="42" y="36" width="76" height="14" rx="7" fill="#1566c8"/>
                <rect x="44" y="50" width="72" height="8" rx="0" fill="#1a4fa0"/>
                {/* Face details */}
                <ellipse cx="70" cy="70" rx="4" ry="4.5" fill="#e8b080"/>
                <ellipse cx="90" cy="70" rx="4" ry="4.5" fill="#e8b080"/>
                <ellipse cx="70" cy="69" rx="2.5" ry="3" fill="#5a3010"/>
                <ellipse cx="90" cy="69" rx="2.5" ry="3" fill="#5a3010"/>
                <path d="M72 82 Q80 88 88 82" stroke="#c0704a" stroke-width="1.5" fill="none"/>
                {/* Arms */}
                <rect x="8" y="102" width="26" height="72" rx="8" fill="#1a4fa0"/>
                <rect x="126" y="102" width="26" height="72" rx="8" fill="#1a4fa0"/>
                {/* Tablet in hand */}
                <rect x="110" y="130" width="32" height="24" rx="4" fill="#e8e8e8" stroke="#ccc" stroke-width="1"/>
                <rect x="113" y="133" width="26" height="18" rx="2" fill="#a0c4f0"/>
                {/* Legs */}
                <rect x="38" y="200" width="34" height="38" rx="6" fill="#222"/>
                <rect x="88" y="200" width="34" height="38" rx="6" fill="#222"/>
                {/* Collar */}
                <rect x="62" y="100" width="16" height="18" rx="3" fill="#fff" opacity="0.15"/>
              </svg>
            </div>

            <div className="hero-service-selector">
              <div className="svc-pills-layout">
                {servicesData.map(service => (
                  <button
                    key={service.id}
                    className={`svc-pill-button ${selectedServiceId === service.id ? 'active' : ''}`}
                    onClick={() => handleHeroPillClick(service.id)}
                  >
                    <div className="svc-pill-icon-box">
                      <Icon name={service.iconName} />
                    </div>
                    {lang === 'RU' ? service.title : lang === 'KZ' ? service.titleKz : service.titleEn}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* STATS SECTION */}
      <section className="stats-section">
        <div className="max-width-wrap">
          <div className="stats-grid">
            <div className="stat-item-box">
              <div className="stat-icon-wrapper">
                <Icon name="check" />
              </div>
              <div>
                <div className="stat-value">70 000+</div>
                <div className="stat-label">
                  {lang === 'RU' ? 'выполненных заказов' : lang === 'KZ' ? 'орындалған тапсырыстар' : 'completed orders'}
                </div>
              </div>
            </div>
            <div className="stat-item-box">
              <div className="stat-icon-wrapper">
                <Icon name="star" />
              </div>
              <div>
                <div className="stat-value">4.9 ★</div>
                <div className="stat-label">
                  {lang === 'RU' ? 'средняя оценка клиентов' : lang === 'KZ' ? 'клиенттердің орташа бағасы' : 'average customer rating'}
                </div>
              </div>
            </div>
            <div className="stat-item-box">
              <div className="stat-icon-wrapper">
                <Icon name="time" />
              </div>
              <div>
                <div className="stat-value">45 {lang === 'RU' ? 'мин' : lang === 'KZ' ? 'мин' : 'min'}</div>
                <div className="stat-label">
                  {lang === 'RU' ? 'среднее время прибытия' : lang === 'KZ' ? 'орташа келу уақыты' : 'average arrival time'}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CATALOG SECTION */}
      <section className="catalog-section" id="catalog" ref={catalogRef}>
        <div className="max-width-wrap">
          <div className="section-header">
            <h2 className="section-title-main">{t[lang].catalogTitle}</h2>
            <p className="section-subtitle-text">{t[lang].catalogSub}</p>
          </div>

          <div className="catalog-tabs">
            {servicesData.map(service => (
              <button
                key={service.id}
                className={`catalog-tab-btn ${selectedServiceId === service.id ? 'active' : ''}`}
                onClick={() => setSelectedServiceId(service.id)}
              >
                {lang === 'RU' ? service.title : lang === 'KZ' ? service.titleKz : service.titleEn}
              </button>
            ))}
          </div>

          <div className="catalog-grid">
            {currentServices.items.map((item, idx) => (
              <div className="catalog-card" key={idx}>
                <div className="catalog-card-header">
                  <div className="catalog-card-title">
                    {lang === 'RU' || lang === 'EN' ? item.name : item.nameKz}
                  </div>
                  <div className="catalog-card-price">{item.price}</div>
                </div>
                <button
                  className="catalog-card-action"
                  onClick={() => handleOpenModalWithService(lang === 'RU' || lang === 'EN' ? item.name : item.nameKz)}
                >
                  <Icon name="phone" />
                  {t[lang].orderBtn}
                </button>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* WHY CHOOSE US */}
      <section className="why-section" id="why-choose">
        <div className="max-width-wrap">
          <div className="section-header">
            <h2 className="section-title-main">{t[lang].whyTitle}</h2>
            <p className="section-subtitle-text">{t[lang].whySub}</p>
          </div>

          <div className="why-grid">
            <div className="why-card">
              <div className="why-icon">
                <Icon name="check" />
              </div>
              <h4 className="why-title">
                {lang === 'RU' ? 'Официальная гарантия' : lang === 'KZ' ? 'Ресми кепілдік' : 'Official Warranty'}
              </h4>
              <p className="why-desc">
                {lang === 'RU' 
                  ? 'Предоставляем письменную гарантию на все виды работ до 1 года.' 
                  : lang === 'KZ' 
                  ? 'Барлық жұмыс түрлеріне 1 жылға дейін жазбаша кепілдік береміз.' 
                  : 'We provide a written warranty for all types of work up to 1 year.'}
              </p>
            </div>
            <div className="why-card">
              <div className="why-icon">
                <Icon name="time" />
              </div>
              <h4 className="why-title">
                {lang === 'RU' ? 'Оперативный выезд' : lang === 'KZ' ? 'Жедел келу' : 'Fast Response'}
              </h4>
              <p className="why-desc">
                {lang === 'RU' 
                  ? 'Мастер приедет в течение 45 минут после вашего звонка или в удобное время.' 
                  : lang === 'KZ' 
                  ? 'Шебер сіздің қоңырауыңыздан кейін 45 минут ішінде немесе ыңғайлы уақытта келеді.' 
                  : 'Specialist will arrive within 45 minutes after your call or at your convenience.'}
              </p>
            </div>
            <div className="why-card">
              <div className="why-icon">
                <Icon name="users" />
              </div>
              <h4 className="why-title">
                {lang === 'RU' ? 'Опытные специалисты' : lang === 'KZ' ? 'Тәжірибелі мамандар' : 'Expert Techs'}
              </h4>
              <p className="why-desc">
                {lang === 'RU' 
                  ? 'Все мастера прошли сертификацию и имеют подтвержденный стаж от 5 лет.' 
                  : lang === 'KZ' 
                  ? 'Барлық шеберлер сертификаттаудан өткен және 5 жылдан астам тәжірибесі бар.' 
                  : 'All technicians are certified and have a proven background of over 5 years.'}
              </p>
            </div>
            <div className="why-card">
              <div className="why-icon">
                <Icon name="star" />
              </div>
              <h4 className="why-title">
                {lang === 'RU' ? 'Честные цены' : lang === 'KZ' ? 'Әділ бағалар' : 'Fair Pricing'}
              </h4>
              <p className="why-desc">
                {lang === 'RU' 
                  ? 'Рассчитываем стоимость до начала работ. Никаких скрытых платежей.' 
                  : lang === 'KZ' 
                  ? 'Жұмыс басталғанға дейін құнын есептейміз. Жасырын төлемдер жоқ.' 
                  : 'We estimate the cost before the work starts. No hidden surcharges.'}
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* REVIEWS SECTION */}
      <section className="reviews-section" id="reviews">
        <div className="max-width-wrap">
          <div className="section-header">
            <h2 className="section-title-main">{t[lang].reviewsTitle}</h2>
            <p className="section-subtitle-text">{t[lang].reviewsSub}</p>
          </div>

          <div className="reviews-grid">
            {reviews.map((rev, idx) => (
              <div className="review-card" key={idx}>
                <div>
                  <div className="review-header">
                    <div className="review-avatar" style={{ backgroundColor: rev.avatarBg || '#e63333' }}>
                      {rev.name[0]}
                    </div>
                    <div>
                      <div className="review-name">{lang === 'RU' ? rev.name : lang === 'KZ' ? rev.nameKz : rev.nameEn}</div>
                      <div className="review-service">{lang === 'RU' ? rev.service : lang === 'KZ' ? rev.serviceKz : rev.serviceEn}</div>
                    </div>
                  </div>
                  <div className="review-rating-stars">
                    {'★'.repeat(rev.rating)}{'☆'.repeat(5 - rev.rating)}
                  </div>
                  <p className="review-text-content">
                    "{lang === 'RU' ? rev.text : lang === 'KZ' ? rev.textKz : rev.textEn}"
                  </p>
                </div>
              </div>
            ))}
          </div>

          {/* WRITE REVIEW FORM */}
          <div className="write-review-container">
            <h3 className="review-form-title">{t[lang].writeReview}</h3>
            <form onSubmit={handleReviewSubmit}>
              <div className="review-form-grid">
                <div className="form-group">
                  <label className="form-label">{t[lang].yourName}</label>
                  <input
                    type="text"
                    className="form-input"
                    value={newReviewName}
                    onChange={(e) => setNewReviewName(e.target.value)}
                    required
                    placeholder="Алексей"
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">{t[lang].selectService}</label>
                  <select
                    className="form-select"
                    value={newReviewService}
                    onChange={(e) => setNewReviewService(e.target.value)}
                    required
                  >
                    <option value="">-- Выберите --</option>
                    {servicesData.map(s => (
                      <option key={s.id} value={s.title}>
                        {lang === 'RU' ? s.title : lang === 'KZ' ? s.titleKz : s.titleEn}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="form-group-full">
                  <label className="form-label">Оценка</label>
                  <div className="rating-stars-select">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <button
                        type="button"
                        key={star}
                        className={`star-select-btn ${newReviewRating >= star ? 'active' : ''}`}
                        onClick={() => setNewReviewRating(star)}
                      >
                        ★
                      </button>
                    ))}
                  </div>
                </div>
                <div className="form-group-full">
                  <label className="form-label">{t[lang].reviewText}</label>
                  <textarea
                    rows="3"
                    className="form-textarea"
                    value={newReviewText}
                    onChange={(e) => setNewReviewText(e.target.value)}
                    required
                    placeholder="Напишите ваш отзыв здесь..."
                  ></textarea>
                </div>
              </div>
              <button type="submit" className="review-submit-btn">
                {t[lang].submitReview}
              </button>
            </form>
          </div>
        </div>
      </section>

      {/* LEAD SECTION (FOOTER FORM) */}
      <section className="lead-section">
        <div className="max-width-wrap lead-inner-box">
          <div className="lead-text-box">
            <h3>{t[lang].leaveRequest}</h3>
            <p>{t[lang].leaveRequestSub}</p>
            <div className="lead-features-small">
              <div className="lead-feat-item">
                <Icon name="check" />
                Выезд бесплатно
              </div>
              <div className="lead-feat-item">
                <Icon name="check" />
                Гарантия качества
              </div>
              <div className="lead-feat-item">
                <Icon name="check" />
                Опытные специалисты
              </div>
              <div className="lead-feat-item">
                <Icon name="check" />
                Работаем 24/7
              </div>
            </div>
          </div>

          <div className="lead-form-box">
            {leadSuccess ? (
              <div className="lead-form-success animate-fade">
                <div className="success-icon-badge">
                  <Icon name="check" />
                </div>
                <h4 className="success-title">{t[lang].successTitle}</h4>
                <p className="success-message">{t[lang].successDesc}</p>
              </div>
            ) : (
              <form onSubmit={handleLeadSubmit}>
                <div className="form-group" style={{ marginBottom: '14px' }}>
                  <label className="form-label">{t[lang].yourName}</label>
                  <input
                    type="text"
                    className="form-input"
                    value={leadName}
                    onChange={(e) => setLeadName(e.target.value)}
                    required
                    placeholder="Ерлан"
                  />
                </div>
                <div className="form-group" style={{ marginBottom: '14px' }}>
                  <label className="form-label">{t[lang].yourPhone}</label>
                  <input
                    type="tel"
                    className="form-input"
                    value={leadPhone}
                    onChange={(e) => setLeadPhone(e.target.value)}
                    required
                    placeholder="+7 (705) 846-2749"
                  />
                </div>
                <div className="form-group" style={{ marginBottom: '20px' }}>
                  <label className="form-label">{t[lang].selectService}</label>
                  <select
                    className="form-select"
                    value={leadService}
                    onChange={(e) => setLeadService(e.target.value)}
                  >
                    {servicesData.map(s => (
                      <option key={s.id} value={s.id}>
                        {lang === 'RU' ? s.title : lang === 'KZ' ? s.titleKz : s.titleEn}
                      </option>
                    ))}
                  </select>
                </div>
                <button type="submit" className="review-submit-btn">
                  {t[lang].sendRequest}
                </button>
              </form>
            )}
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="app-footer">
        <div className="max-width-wrap">
          <div className="footer-grid">
            <div className="footer-about-col">
              <div className="footer-logo-title">
                HUB<span>MASTER</span>
              </div>
              <p className="footer-desc-text">
                {lang === 'RU' 
                  ? 'Профессиональная сборка мебели, ремонт бытовой техники, компьютерная помощь, сантехнические и электромонтажные услуги в Алматы и Астане. Быстро, качественно и с долгосрочной гарантией.' 
                  : lang === 'KZ' 
                  ? 'Алматы және Астана қалаларында жиһаз жинау, тұрмыстық техниканы жөндеу, компьютерлік көмек, сантехникалық және электр монтаждау қызметтері. Жылдам, сапалы және ұзақ мерзімді кепілдікпен.' 
                  : 'Professional furniture assembly, appliance repair, computer help, plumbing and electrical services in Almaty and Astana. Fast, high-quality, and with long-term warranty.'}
              </p>
            </div>

            <div>
              <h4 className="footer-col-title">{t[lang].catalogTitle}</h4>
              <ul className="footer-links-list">
                {servicesData.slice(0, 5).map(s => (
                  <li key={s.id}>
                    <button onClick={() => handleHeroPillClick(s.id)} className="footer-link-btn">
                      {lang === 'RU' ? s.title : lang === 'KZ' ? s.titleKz : s.titleEn}
                    </button>
                  </li>
                ))}
              </ul>
            </div>

            <div className="footer-contact-info">
              <h4 className="footer-col-title">{t[lang].contacts}</h4>
              <div className="footer-contact-item">
                <Icon name="phone" />
                {t[lang].phoneNum}
              </div>
              <div className="footer-contact-item">
                <svg viewBox="0 0 24 24" fill="none" strokeWidth="2" stroke="currentColor">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                  <polyline points="22,6 12,13 2,6"/>
                </svg>
                info@hubmaster.kz
              </div>
              <div className="footer-contact-item">
                <svg viewBox="0 0 24 24" fill="none" strokeWidth="2" stroke="currentColor">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                  <circle cx="12" cy="10" r="3"/>
                </svg>
                {city === 'Алматы' ? 'Алматы, пр. Аль-Фараби 77/7' : 'Астана, пр. Кабанбай Батыра 15'}
              </div>
            </div>
          </div>

          <div className="footer-bottom">
            <div>{t[lang].copyright}</div>
            <div>Powered by React & Vite</div>
          </div>
        </div>
      </footer>

      {/* BOOKING MODAL */}
      <div className={`modal-overlay ${isModalOpen ? 'active' : ''}`} onClick={(e) => e.target.classList.contains('modal-overlay') && setIsModalOpen(false)}>
        <div className="modal-box">
          <button className="modal-close-btn" onClick={() => setIsModalOpen(false)} aria-label="Close modal">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>

          {modalSuccess ? (
            <div className="modal-overlay-success animate-fade">
              <div className="success-icon-badge">
                <Icon name="check" />
              </div>
              <h4 className="success-title">{t[lang].successTitle}</h4>
              <p className="success-message">{t[lang].successDesc}</p>
            </div>
          ) : (
            <>
              <h3 className="modal-title-text">{t[lang].leaveRequest}</h3>
              <p className="modal-desc-text">
                {modalService ? `${lang === 'RU' ? 'Услуга' : lang === 'KZ' ? 'Қызмет' : 'Service'}: ${modalService}` : t[lang].leaveRequestSub}
              </p>
              <form onSubmit={handleModalSubmit}>
                <div className="form-group" style={{ marginBottom: '14px' }}>
                  <label className="form-label">{t[lang].yourName}</label>
                  <input
                    type="text"
                    className="form-input"
                    value={modalName}
                    onChange={(e) => setModalName(e.target.value)}
                    required
                    placeholder="Азамат"
                  />
                </div>
                <div className="form-group" style={{ marginBottom: '20px' }}>
                  <label className="form-label">{t[lang].yourPhone}</label>
                  <input
                    type="tel"
                    className="form-input"
                    value={modalPhone}
                    onChange={(e) => setModalPhone(e.target.value)}
                    required
                    placeholder="+7 (705) 846-2749"
                  />
                </div>
                <button type="submit" className="review-submit-btn">
                  {t[lang].sendRequest}
                </button>
              </form>
            </>
          )}
        </div>
      </div>

      {/* CABINET LOGIN MODAL */}
      {isLoginModalOpen && (
        <div className="modal-overlay active" onClick={(e) => e.target.classList.contains('modal-overlay') && setIsLoginModalOpen(false)}>
          <div className="modal-box auth-modal-box">
            <button className="modal-close-btn" onClick={() => setIsLoginModalOpen(false)} aria-label="Close modal">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>

            <h3 className="modal-title-text">{t[lang].loginTitle}</h3>
            <p className="modal-desc-text">{t[lang].loginSub}</p>

            {loginError && <div className="auth-error-msg">{loginError}</div>}

            {loginStep === 'phone' ? (
              <form onSubmit={handleSendCode}>
                <div className="form-group" style={{ marginBottom: '20px' }}>
                  <label className="form-label">{t[lang].phoneLabel}</label>
                  <input
                    type="tel"
                    className="form-input"
                    value={loginPhone}
                    onChange={(e) => setLoginPhone(e.target.value)}
                    required
                    placeholder="+7 (707) 123-4567"
                  />
                </div>
                <button type="submit" className="review-submit-btn">
                  {t[lang].getCodeBtn}
                </button>
              </form>
            ) : (
              <form onSubmit={handleVerifyCode}>
                <div className="auth-sms-info">
                  {t[lang].codeSentMsg} <strong>{loginPhone}</strong>
                </div>
                <div className="form-group" style={{ marginBottom: '15px' }}>
                  <label className="form-label">{t[lang].codeLabel}</label>
                  <input
                    type="text"
                    maxLength="4"
                    className="form-input code-input-field"
                    value={loginCode}
                    onChange={(e) => setLoginCode(e.target.value)}
                    required
                    placeholder="1234"
                    autoFocus
                  />
                </div>
                <div className="auth-code-hint">
                  {t[lang].demoCodeHint}
                </div>
                <div className="auth-timer-box">
                  {smsTimer > 0 ? (
                    <span>{t[lang].smsTimerMsg.replace('{time}', smsTimer)}</span>
                  ) : (
                    <button type="button" className="auth-resend-btn" onClick={() => { setSmsTimer(60); setLoginError(''); }}>
                      {t[lang].resendCode}
                    </button>
                  )}
                </div>
                <button type="submit" className="review-submit-btn" style={{ marginTop: '10px' }}>
                  {t[lang].verifyBtn}
                </button>
              </form>
            )}
          </div>
        </div>
      )}

      {/* CABINET DASHBOARD OVERLAY */}
      {isCabinetOpen && (
        <div className="cabinet-overlay active">
          <div className="cabinet-dialog">
            <header className="cabinet-header">
              <div className="cabinet-header-title">
                <Icon name="user" />
                {t[lang].cabinetTitle}
              </div>
              <div className="cabinet-header-right">
                <button className="cabinet-close-btn" onClick={() => setIsCabinetOpen(false)}>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <line x1="18" y1="6" x2="6" y2="18"/>
                    <line x1="6" y1="6" x2="18" y2="18"/>
                  </svg>
                </button>
              </div>
            </header>

            <div className="cabinet-body">
              {/* Sidebar */}
              <aside className="cabinet-sidebar">
                <div className="cabinet-user-card">
                  <div className="cabinet-avatar" style={{ backgroundColor: '#e63333' }}>
                    {userProfile.name ? userProfile.name[0] : 'U'}
                  </div>
                  <div className="cabinet-user-info">
                    <div className="cabinet-user-name">{userProfile.name}</div>
                    <div className="cabinet-user-phone">{userProfile.phone || t[lang].phonePlaceholder}</div>
                    <span className="cabinet-badge">{t[lang].tierGold}</span>
                  </div>
                </div>

                <div className="cabinet-bonus-card">
                  <div className="bonus-header">
                    <div className="bonus-lbl">{t[lang].bonusBalance}</div>
                    <div className="bonus-val">{userProfile.bonuses} ₸</div>
                  </div>
                  <div className="bonus-progress-wrap">
                    <div className="bonus-progress-bar" style={{ width: '45%' }}></div>
                  </div>
                  <div className="bonus-progress-lbl">
                    {t[lang].nextTierProgress.replace('{spent}', `${userProfile.spent} ₸`)}
                  </div>
                </div>

                <nav className="cabinet-nav">
                  <button className={`cab-nav-item ${activeCabinetTab === 'dashboard' ? 'active' : ''}`} onClick={() => setActiveCabinetTab('dashboard')}>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="3" width="7" height="9" rx="1"/><rect x="14" y="3" width="7" height="5" rx="1"/><rect x="14" y="12" width="7" height="9" rx="1"/><rect x="3" y="16" width="7" height="5" rx="1"/></svg>
                    {t[lang].tabDashboard}
                  </button>
                  <button className={`cab-nav-item ${activeCabinetTab === 'orders' ? 'active' : ''}`} onClick={() => setActiveCabinetTab('orders')}>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
                    {t[lang].tabOrders}
                  </button>
                  <button className={`cab-nav-item ${activeCabinetTab === 'profile' ? 'active' : ''}`} onClick={() => setActiveCabinetTab('profile')}>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                    {t[lang].tabProfile}
                  </button>
                  <button className={`cab-nav-item ${activeCabinetTab === 'chat' ? 'active' : ''}`} onClick={() => setActiveCabinetTab('chat')}>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>
                    {t[lang].tabChat}
                    {chatMessages.filter(m => m.sender === 'operator').length > 0 && <span className="chat-badge-notify"></span>}
                  </button>
                </nav>

                <button className="cab-logout-btn" onClick={handleLogout}>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
                  {t[lang].logout}
                </button>
              </aside>

              {/* Main Panel Content */}
              <main className="cabinet-main-panel">
                {/* 1. DASHBOARD VIEW */}
                {activeCabinetTab === 'dashboard' && (
                  <div className="cabinet-tab-content animate-fade">
                    <div className="cabinet-welcome-header">
                      <h2>{t[lang].welcomeBack}, {userProfile.name.split(' ')[0]}!</h2>
                      <p>{t[lang].loyaltyTier}: <strong>{t[lang].tierGold}</strong></p>
                    </div>

                    <div className="cabinet-dashboard-grid">
                      {/* Active Orders List */}
                      <div className="cabinet-dashboard-orders">
                        <h3>{t[lang].activeOrdersTitle}</h3>
                        {cabinetOrders.filter(o => o.status === 'searching' || o.status === 'assigned').length === 0 ? (
                          <div className="no-orders-box">
                            <p>{t[lang].noActiveOrders}</p>
                          </div>
                        ) : (
                          <div className="cab-orders-list">
                            {cabinetOrders.filter(o => o.status === 'searching' || o.status === 'assigned').map(order => (
                              <div className="cab-order-card" key={order.id}>
                                <div className="cab-order-card-header">
                                  <div className="cab-order-id">
                                    {t[lang].orderNumber}{order.id}
                                  </div>
                                  <div className={`cab-order-status status-${order.status}`}>
                                    {order.status === 'searching' ? t[lang].statusSearching : t[lang].statusAssigned}
                                  </div>
                                </div>
                                <div className="cab-order-name">
                                  {lang === 'RU' ? order.serviceName : lang === 'KZ' ? order.serviceNameKz : order.serviceNameEn}
                                </div>
                                <div className="cab-order-meta">
                                  <div>{t[lang].orderDate}: <strong>{order.date}</strong></div>
                                  <div>{t[lang].orderPrice}: <strong className="price-tag">{order.price}</strong></div>
                                </div>

                                {order.master && (
                                  <div className="cab-order-master-box">
                                    <div className="master-title">{t[lang].assignedMasterTitle}</div>
                                    <div className="master-profile-mini">
                                      <div className="master-avatar" style={{ backgroundColor: order.master.avatarBg }}>
                                        {order.master.name[0]}
                                      </div>
                                      <div className="master-details">
                                        <div className="master-name">{order.master.name}</div>
                                        <div className="master-rating">★ {order.master.rating} ({order.master.completedCount} {t[lang].ordersCount.split(' ')[0]})</div>
                                      </div>
                                      <a href={`https://wa.me/${order.master.phone}`} target="_blank" rel="noopener noreferrer" className="master-wa-btn">
                                        <Icon name="phone" />
                                      </a>
                                    </div>
                                  </div>
                                )}

                                <button className="cab-order-cancel-btn" onClick={() => handleCancelOrder(order.id)}>
                                  {t[lang].orderCancel}
                                </button>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>

                      {/* Quick Order Column */}
                      <div className="cabinet-dashboard-quickorder">
                        <h3>{t[lang].orderNewCabinetBtn}</h3>
                        {cabNewOrderSuccess ? (
                          <div className="lead-form-success animate-fade" style={{ background: 'var(--bg-dark)', border: '1px solid var(--border)' }}>
                            <div className="success-icon-badge">
                              <Icon name="check" />
                            </div>
                            <h4 className="success-title">{t[lang].successTitle}</h4>
                            <p className="success-message">{t[lang].createOrderSuccess}</p>
                          </div>
                        ) : (
                          <form onSubmit={handleCabinetNewOrder} className="cab-quickorder-form">
                            <div className="form-group" style={{ marginBottom: '14px' }}>
                              <label className="form-label">{t[lang].selectCategoryCabinet}</label>
                              <select
                                className="form-select"
                                value={cabNewOrderCat}
                                onChange={(e) => setCabNewOrderCat(e.target.value)}
                              >
                                {servicesData.map(s => (
                                  <option key={s.id} value={s.id}>
                                    {lang === 'RU' ? s.title : lang === 'KZ' ? s.titleKz : s.titleEn}
                                  </option>
                                ))}
                              </select>
                            </div>
                            <div className="form-group" style={{ marginBottom: '20px' }}>
                              <label className="form-label">{t[lang].orderSpecCabinet}</label>
                              <textarea
                                rows="3"
                                className="form-textarea"
                                value={cabNewOrderText}
                                onChange={(e) => setCabNewOrderText(e.target.value)}
                                required
                                placeholder={lang === 'RU' ? 'Например: Собрать распашной шкаф 3 секции в гостиной' : lang === 'KZ' ? 'Мысалы: Қонақ бөлмесінде 3 секциялы шкафты жинау' : 'E.g. Assemble a 3-section wardrobe in the living room'}
                              ></textarea>
                            </div>
                            <button type="submit" className="review-submit-btn">
                              {t[lang].orderNewCabinetBtn}
                            </button>
                          </form>
                        )}
                      </div>
                    </div>
                  </div>
                )}

                {/* 2. ORDERS HISTORY VIEW */}
                {activeCabinetTab === 'orders' && (
                  <div className="cabinet-tab-content animate-fade">
                    <h2 className="panel-title">{t[lang].tabOrders}</h2>
                    <div className="cab-orders-full-list">
                      {cabinetOrders.map(order => (
                        <div className="cab-order-card-full" key={order.id}>
                          <div className="card-full-left">
                            <div className="card-full-icon" style={{ background: order.status === 'completed' ? 'rgba(37,211,102,0.1)' : order.status === 'cancelled' ? 'rgba(230,51,51,0.1)' : 'rgba(230,51,51,0.1)' }}>
                              <Icon name={order.category === 'furniture' ? 'hammer' : order.category === 'plumbing' ? 'droplet' : order.category === 'cleaning' ? 'sparkles' : 'wrench'} />
                            </div>
                            <div>
                              <div className="order-full-name">
                                {lang === 'RU' ? order.serviceName : lang === 'KZ' ? order.serviceNameKz : order.serviceNameEn}
                              </div>
                              <div className="order-full-date">
                                {t[lang].orderDate}: <strong>{order.date}</strong> • {t[lang].orderPrice}: <strong>{order.price}</strong>
                              </div>
                            </div>
                          </div>
                          <div className="card-full-right">
                            <div className={`cab-order-status status-${order.status}`}>
                              {order.status === 'searching' && t[lang].statusSearching}
                              {order.status === 'assigned' && t[lang].statusAssigned}
                              {order.status === 'completed' && t[lang].statusCompleted}
                              {order.status === 'cancelled' && t[lang].statusCancelled}
                            </div>
                            {order.status === 'assigned' && (
                              <button className="cab-order-cancel-btn-small" onClick={() => handleCancelOrder(order.id)}>
                                {t[lang].orderCancel}
                              </button>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* 3. PROFILE SETTINGS VIEW */}
                {activeCabinetTab === 'profile' && (
                  <div className="cabinet-tab-content animate-fade">
                    <h2 className="panel-title">{t[lang].tabProfile}</h2>
                    
                    {profileSaveSuccess && (
                      <div className="profile-save-success-msg animate-fade">
                        {t[lang].profileSaveSuccess}
                      </div>
                    )}

                    <form onSubmit={handleProfileSave} className="cabinet-profile-form">
                      <div className="profile-form-grid">
                        <div className="form-group">
                          <label className="form-label">{t[lang].profileName}</label>
                          <input
                            type="text"
                            className="form-input"
                            value={userProfile.name}
                            onChange={(e) => setUserProfile({ ...userProfile, name: e.target.value })}
                            required
                          />
                        </div>
                        <div className="form-group">
                          <label className="form-label">{t[lang].yourPhone}</label>
                          <input
                            type="tel"
                            className="form-input"
                            value={userProfile.phone}
                            disabled
                            style={{ opacity: 0.6, cursor: 'not-allowed' }}
                          />
                        </div>
                        <div className="form-group">
                          <label className="form-label">{t[lang].profileEmail}</label>
                          <input
                            type="email"
                            className="form-input"
                            value={userProfile.email}
                            onChange={(e) => setUserProfile({ ...userProfile, email: e.target.value })}
                            required
                          />
                        </div>
                        <div className="form-group">
                          <label className="form-label">{t[lang].profileCity}</label>
                          <select
                            className="form-select"
                            value={userProfile.city}
                            onChange={(e) => setUserProfile({ ...userProfile, city: e.target.value })}
                          >
                            <option value="Алматы">Алматы</option>
                            <option value="Астана">Астана</option>
                          </select>
                        </div>
                      </div>

                      <div className="profile-address-section">
                        <label className="form-label">{t[lang].profileAddress}</label>
                        <ul className="profile-address-list">
                          {userProfile.addresses.map((addr, idx) => (
                            <li key={idx} className="profile-address-item">
                              <span>{addr}</span>
                              <button type="button" className="remove-address-btn" onClick={() => handleRemoveAddress(idx)}>
                                &times;
                              </button>
                            </li>
                          ))}
                        </ul>

                        <div className="add-address-form">
                          <input
                            type="text"
                            className="form-input"
                            placeholder={lang === 'RU' ? 'Введите новый адрес...' : lang === 'KZ' ? 'Жаңа мекенжайды енгізіңіз...' : 'Enter new address...'}
                            value={newAddressInput}
                            onChange={(e) => setNewAddressInput(e.target.value)}
                          />
                          <button type="button" className="add-address-btn-action" onClick={handleAddAddress}>
                            {t[lang].addAddressBtn}
                          </button>
                        </div>
                      </div>

                      <button type="submit" className="review-submit-btn" style={{ maxWidth: '200px', marginTop: '20px' }}>
                        {t[lang].saveChanges}
                      </button>
                    </form>
                  </div>
                )}

                {/* 4. SUPPORT CHAT VIEW */}
                {activeCabinetTab === 'chat' && (
                  <div className="cabinet-tab-content animate-fade chat-tab-layout">
                    <div className="chat-panel-header">
                      <h3>{t[lang].chatTitle}</h3>
                      <p>{t[lang].chatSub}</p>
                    </div>

                    <div className="chat-messages-container">
                      {chatMessages.map((msg, idx) => (
                        <div className={`chat-message-bubble ${msg.sender === 'user' ? 'msg-user' : 'msg-operator'}`} key={idx}>
                          <div className="msg-avatar">
                            {msg.sender === 'user' ? 'U' : 'H'}
                          </div>
                          <div className="msg-content-box">
                            <div className="msg-text">{msg.text}</div>
                            <div className="msg-time">{msg.time}</div>
                          </div>
                        </div>
                      ))}
                      {isTyping && (
                        <div className="chat-message-bubble msg-operator typing-bubble">
                          <div className="msg-avatar">H</div>
                          <div className="msg-content-box">
                            <div className="typing-indicator">
                              <span></span><span></span><span></span>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>

                    <form onSubmit={handleSendChatMessage} className="chat-input-form">
                      <input
                        type="text"
                        className="form-input chat-input-field"
                        placeholder={t[lang].chatInputPlaceholder}
                        value={chatInput}
                        onChange={(e) => setChatInput(e.target.value)}
                      />
                      <button type="submit" className="chat-send-btn-action">
                        {t[lang].chatSendBtn}
                      </button>
                    </form>
                  </div>
                )}
              </main>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
