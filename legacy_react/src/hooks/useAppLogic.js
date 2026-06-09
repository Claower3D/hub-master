import { useState, useEffect, useRef } from 'react';
import { servicesData, initialReviews } from '../data/servicesData';

const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://localhost:3030'
  : '';

export default function useAppLogic() {
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
  
  const [cabinetOrders, setCabinetOrders] = useState([]);

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

  // Assistant Configuration state
  const [assistantConfig, setAssistantConfig] = useState({
    fallback: 'Спасибо за обращение! Наш специалист свяжется с вами в течение 5 минут для точного расчета.',
    rules: [
      {
        id: 'rule-price',
        triggers: ['цен', 'стоим', 'прайс', 'бага', 'құн'],
        reply: 'Стоимость большинства услуг начинается от 2 500 ₸. Выезд мастера и диагностика при продолжении работ — бесплатно! Хотите оставить заявку на точный расчет?'
      },
      {
        id: 'rule-time',
        triggers: ['как', 'когда', 'қашан'],
        reply: 'Наши специалисты работают 24/7. Мастер может выехать к вам в течение 45 минут после оформления заявки.'
      }
    ]
  });

  // Fetch all reviews on mount
  const fetchReviews = () => {
    fetch(`${API_BASE}/api/reviews`)
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data) && data.length > 0) {
          const mapped = data.map((rev, index) => ({
            name: rev.author,
            nameKz: rev.author,
            nameEn: rev.author,
            avatarBg: ['#e63333', '#3498db', '#e74c3c', '#9b59b6', '#e67e22', '#1abc9c'][index % 6],
            service: 'Ремонт и услуги',
            serviceKz: 'Жөндеу және қызметтер',
            serviceEn: 'Repair & Services',
            rating: rev.rating || 5,
            text: rev.text,
            textKz: rev.text,
            textEn: rev.text
          }));
          setReviews(mapped);
        }
      })
      .catch(err => console.error("Error fetching reviews:", err));
  };

  // Fetch callbacks list for logged-in user
  const fetchMyCallbacks = (tokenToUse) => {
    const activeToken = tokenToUse || localStorage.getItem('token');
    if (!activeToken) return;

    fetch(`${API_BASE}/api/callbacks`, {
      headers: {
        'Authorization': `Bearer ${activeToken}`
      }
    })
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch callbacks');
        return res.json();
      })
      .then(data => {
        if (Array.isArray(data)) {
          const mapped = data.map(cb => {
            const cleanService = cb.service || 'Общий вызов мастера';
            // Parse category from service name if possible
            let matchedCategory = 'furniture';
            for (const category of servicesData) {
              if (cleanService.toLowerCase().includes(category.title.toLowerCase()) || 
                  cleanService.toLowerCase().includes(category.id.toLowerCase())) {
                matchedCategory = category.id;
                break;
              }
            }

            let mappedStatus = 'searching';
            if (cb.status === 'completed') mappedStatus = 'completed';
            if (cb.status === 'in_progress') mappedStatus = 'assigned';
            if (cb.status === 'cancelled') mappedStatus = 'cancelled';

            let master = null;
            if (mappedStatus === 'assigned' || mappedStatus === 'completed') {
              master = {
                name: 'Ерлан Сабитов',
                rating: '4.9',
                completedCount: 520,
                experience: 4,
                phone: '77058462749',
                avatarBg: '#e67e22'
              };
            }

            return {
              id: String(cb.id),
              category: matchedCategory,
              serviceName: cleanService,
              serviceNameKz: cleanService,
              serviceNameEn: cleanService,
              date: new Date(cb.created_at).toLocaleDateString('ru-RU'),
              price: mappedStatus === 'completed' ? '10 000 ₸' : 'Расчет цены',
              status: mappedStatus,
              master: master
            };
          });
          setCabinetOrders(mapped);
        }
      })
      .catch(err => console.error("Error fetching callbacks:", err));
  };

  // Fetch assistant config on mount
  const fetchAssistantConfig = () => {
    fetch(`${API_BASE}/api/assistant-config`)
      .then(res => {
        if (!res.ok) throw new Error();
        return res.json();
      })
      .then(data => {
        if (data && data.rules) {
          setAssistantConfig(data);
        }
      })
      .catch(() => {});
  };

  // Verify token and fetch user on load
  useEffect(() => {
    fetchReviews();
    fetchAssistantConfig();

    const token = localStorage.getItem('token');
    if (token) {
      fetch(`${API_BASE}/api/auth/me`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
        .then(res => {
          if (!res.ok) throw new Error('Token invalid');
          return res.json();
        })
        .then(data => {
          if (data && data.user) {
            setIsAuthenticated(true);
            const savedAddrs = localStorage.getItem(`addresses_${data.user.id}`);
            const parsedAddrs = savedAddrs ? JSON.parse(savedAddrs) : ['пр. Аль-Фараби, д. 77/7, кв. 42', 'ул. Абая, д. 10, оф. 5'];

            setUserProfile({
              name: data.user.name,
              phone: data.user.phone,
              email: data.user.email,
              city: data.user.city,
              addresses: parsedAddrs,
              bonuses: data.user.bonuses,
              spent: 45000,
              loyaltyTier: data.user.bonuses > 2000 ? 'Gold' : 'Silver'
            });
            fetchMyCallbacks(token);
          }
        })
        .catch(err => {
          console.error("Token verification failed:", err);
          handleLogout();
        });
    } else {
      // Load fallback session from localStorage
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

    const body = {
      name: modalName,
      phone: modalPhone,
      service: modalService || 'Общий вызов мастера',
      city: city,
      comment: `Заказ через модальное окно на услугу: ${modalService}`
    };

    const headers = { 'Content-Type': 'application/json' };
    const token = localStorage.getItem('token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    fetch(`${API_BASE}/api/callback`, {
      method: 'POST',
      headers,
      body: JSON.stringify(body)
    })
      .then(res => res.json())
      .then(data => {
        setModalSuccess(true);
        if (isAuthenticated) {
          fetchMyCallbacks();
        }
        setTimeout(() => {
          setIsModalOpen(false);
          setModalName('');
          setModalPhone('');
          setModalService('');
          setModalSuccess(false);
        }, 2500);
      })
      .catch(err => {
        console.error("Error creating callback:", err);
        setModalSuccess(true); // Fallback success screen
        setTimeout(() => {
          setIsModalOpen(false);
          setModalName('');
          setModalPhone('');
          setModalService('');
          setModalSuccess(false);
        }, 2500);
      });
  };

  const handleLeadSubmit = (e) => {
    e.preventDefault();
    if (!leadName || !leadPhone) return;

    const body = {
      name: leadName,
      phone: leadPhone,
      service: leadService,
      city: city,
      comment: `Заявка с сайта на категорию: ${leadService}`
    };

    const headers = { 'Content-Type': 'application/json' };
    const token = localStorage.getItem('token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    fetch(`${API_BASE}/api/callback`, {
      method: 'POST',
      headers,
      body: JSON.stringify(body)
    })
      .then(res => res.json())
      .then(data => {
        setLeadSuccess(true);
        if (isAuthenticated) {
          fetchMyCallbacks();
        }
        setTimeout(() => {
          setLeadName('');
          setLeadPhone('');
          setLeadSuccess(false);
        }, 4000);
      })
      .catch(err => {
        console.error("Error creating lead callback:", err);
        setLeadSuccess(true);
        setTimeout(() => {
          setLeadName('');
          setLeadPhone('');
          setLeadSuccess(false);
        }, 4000);
      });
  };

  const handleReviewSubmit = (e) => {
    e.preventDefault();
    if (!newReviewName || !newReviewText) return;

    const body = {
      author: newReviewName,
      text: newReviewText,
      rating: newReviewRating
    };

    const headers = { 'Content-Type': 'application/json' };
    const token = localStorage.getItem('token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    fetch(`${API_BASE}/api/reviews/new`, {
      method: 'POST',
      headers,
      body: JSON.stringify(body)
    })
      .then(res => res.json())
      .then(() => {
        fetchReviews();
        setNewReviewName('');
        setNewReviewService('');
        setNewReviewText('');
        setNewReviewRating(5);
      })
      .catch(err => {
        console.error("Error submitting review:", err);
        const newReview = {
          name: newReviewName,
          nameKz: newReviewName,
          nameEn: newReviewName,
          avatarBg: '#' + Math.floor(Math.random()*16777215).toString(16),
          service: newReviewService || 'Услуга',
          serviceKz: newReviewService || 'Қызмет',
          serviceEn: newReviewService || 'Service',
          rating: newReviewRating,
          text: newReviewText,
          textKz: newReviewText,
          textEn: newReviewText
        };
        setReviews(prev => [newReview, ...prev]);
        setNewReviewName('');
        setNewReviewService('');
        setNewReviewText('');
        setNewReviewRating(5);
      });
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

    setLoginError('');
    fetch(`${API_BASE}/api/auth/send-sms`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phone: loginPhone })
    })
      .then(res => {
        if (!res.ok) {
          return res.json().then(err => { throw new Error(err.error || 'Ошибка отправки SMS'); });
        }
        return res.json();
      })
      .then(data => {
        setLoginStep('code');
        setSmsTimer(60);
        if (data.demo_code) {
          console.log("Demo verification code:", data.demo_code);
        }
      })
      .catch(err => {
        setLoginError(err.message);
      });
  };

  const handleVerifyCode = (e) => {
    e.preventDefault();
    setLoginError('');

    fetch(`${API_BASE}/api/auth/verify-sms`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phone: loginPhone, code: loginCode })
    })
      .then(res => {
        if (!res.ok) {
          return res.json().then(err => { throw new Error(err.error || 'Неверный код'); });
        }
        return res.json();
      })
      .then(data => {
        if (data.status === 'new_user') {
          // Auto register new user post SMS verification
          return fetch(`${API_BASE}/api/auth/register-phone`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              phone: loginPhone,
              name: `Пользователь ${loginPhone}`,
              city: city
            })
          }).then(regRes => {
            if (!regRes.ok) throw new Error('Failed registration');
            return regRes.json();
          });
        }
        return data;
      })
      .then(data => {
        if (data && data.token) {
          localStorage.setItem('token', data.token);
          setIsAuthenticated(true);
          setIsLoginModalOpen(false);
          setIsCabinetOpen(true);
          
          const savedAddrs = localStorage.getItem(`addresses_${data.user.id}`);
          const parsedAddrs = savedAddrs ? JSON.parse(savedAddrs) : ['пр. Аль-Фараби, д. 77/7, кв. 42', 'ул. Абая, д. 10, оф. 5'];

          setUserProfile({
            name: data.user.name,
            phone: data.user.phone,
            email: data.user.email,
            city: data.user.city,
            addresses: parsedAddrs,
            bonuses: data.user.bonuses,
            spent: 45000,
            loyaltyTier: data.user.bonuses > 2000 ? 'Gold' : 'Silver'
          });
          
          fetchMyCallbacks(data.token);
          
          setLoginPhone('');
          setLoginCode('');
          setLoginStep('phone');
        }
      })
      .catch(err => {
        setLoginError(err.message);
      });
  };

  const handleLogout = () => {
    const token = localStorage.getItem('token');
    if (token) {
      fetch(`${API_BASE}/api/auth/logout`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      }).finally(() => {
        localStorage.removeItem('token');
        setIsAuthenticated(false);
        setIsCabinetOpen(false);
        setCabinetOrders([]);
      });
    } else {
      setIsAuthenticated(false);
      setIsCabinetOpen(false);
      setCabinetOrders([]);
    }
  };

  const handleProfileSave = (e) => {
    e.preventDefault();
    const token = localStorage.getItem('token');
    if (!token) return;

    fetch(`${API_BASE}/api/auth/profile`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        name: userProfile.name,
        phone: userProfile.phone,
        city: userProfile.city,
        password: ''
      })
    })
      .then(res => {
        if (!res.ok) throw new Error('Failed to update profile');
        return res.json();
      })
      .then(data => {
        setProfileSaveSuccess(true);
        setTimeout(() => {
          setProfileSaveSuccess(false);
        }, 3000);
      })
      .catch(err => {
        console.error("Error updating profile:", err);
        setProfileSaveSuccess(true);
        setTimeout(() => {
          setProfileSaveSuccess(false);
        }, 3000);
      });
  };

  const handleAddAddress = (e) => {
    e.preventDefault();
    if (!newAddressInput.trim()) return;
    
    const updatedAddresses = [...userProfile.addresses, newAddressInput.trim()];
    const updatedProfile = {
      ...userProfile,
      addresses: updatedAddresses
    };
    setUserProfile(updatedProfile);
    setNewAddressInput('');

    const token = localStorage.getItem('token');
    if (token) {
      // Determine user id if possible, otherwise generic
      fetch(`${API_BASE}/api/auth/me`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
        .then(res => res.json())
        .then(data => {
          if (data && data.user) {
            localStorage.setItem(`addresses_${data.user.id}`, JSON.stringify(updatedAddresses));
          }
        })
        .catch(() => {});
    }
  };

  const handleRemoveAddress = (index) => {
    const updatedAddresses = userProfile.addresses.filter((_, idx) => idx !== index);
    const updatedProfile = {
      ...userProfile,
      addresses: updatedAddresses
    };
    setUserProfile(updatedProfile);

    const token = localStorage.getItem('token');
    if (token) {
      fetch(`${API_BASE}/api/auth/me`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
        .then(res => res.json())
        .then(data => {
          if (data && data.user) {
            localStorage.setItem(`addresses_${data.user.id}`, JSON.stringify(updatedAddresses));
          }
        })
        .catch(() => {});
    }
  };

  const handleCancelOrder = (orderId) => {
    const confirmMsg = lang === 'RU' 
      ? 'Вы уверены, что хотите отменить этот заказ?' 
      : lang === 'KZ'
      ? 'Бұл тапсырысты жойғыңыз келетініне сенімдісіз бе?'
      : 'Are you sure you want to cancel this order?';

    if (window.confirm(confirmMsg)) {
      // Locally cancel order first
      const updated = cabinetOrders.map(order => {
        if (order.id === orderId) {
          return { ...order, status: 'cancelled' };
        }
        return order;
      });
      setCabinetOrders(updated);
    }
  };

  const handleCabinetNewOrder = (e) => {
    e.preventDefault();
    if (!cabNewOrderText) return;
    
    const catData = servicesData.find(s => s.id === cabNewOrderCat);
    const catTitle = catData ? catData.title : 'Услуга';
    
    const body = {
      name: userProfile.name || 'Пользователь',
      phone: userProfile.phone || '',
      service: `${catTitle}: ${cabNewOrderText}`,
      city: userProfile.city || city,
      comment: 'Быстрый заказ из личного кабинета'
    };

    const headers = { 'Content-Type': 'application/json' };
    const token = localStorage.getItem('token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    fetch(`${API_BASE}/api/callback`, {
      method: 'POST',
      headers,
      body: JSON.stringify(body)
    })
      .then(res => res.json())
      .then(() => {
        setCabNewOrderText('');
        setCabNewOrderSuccess(true);
        fetchMyCallbacks(token);
        setTimeout(() => {
          setCabNewOrderSuccess(false);
        }, 3000);
      })
      .catch(err => {
        console.error("Error creating cabinet callback:", err);
        // Fallback local update
        const newOrder = {
          id: Math.floor(1000 + Math.random() * 9000).toString(),
          category: cabNewOrderCat,
          serviceName: `${catTitle}: ${cabNewOrderText}`,
          serviceNameKz: `${catTitle}: ${cabNewOrderText}`,
          serviceNameEn: `${catTitle}: ${cabNewOrderText}`,
          date: new Date().toLocaleDateString('ru-RU'),
          price: 'Расчет цены',
          status: 'searching',
          master: null
        };
        
        const updatedOrders = [newOrder, ...cabinetOrders];
        setCabinetOrders(updatedOrders);
        setCabNewOrderText('');
        setCabNewOrderSuccess(true);
        setTimeout(() => {
          setCabNewOrderSuccess(false);
        }, 3000);
      });
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
    
    setIsTyping(true);
    setTimeout(() => {
      setIsTyping(false);
      let replyText = '';
      const qLower = userMsgText.toLowerCase();
      
      // Match rules from backend assistantConfig
      let matchedRule = null;
      for (const rule of assistantConfig.rules) {
        if (rule.triggers.some(trg => qLower.includes(trg.trim().toLowerCase()))) {
          matchedRule = rule;
          break;
        }
      }

      if (matchedRule) {
        replyText = matchedRule.reply;
      } else {
        replyText = assistantConfig.fallback;
      }
      
      const newReply = {
        sender: 'operator',
        time: new Date().toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' }),
        text: replyText
      };
      
      setChatMessages(prev => [...prev, newReply]);
    }, 1500);
  };

  return {
    lang, setLang,
    city, setCity,
    theme, setTheme,
    selectedServiceId, setSelectedServiceId,
    reviews, setReviews,
    
    isModalOpen, setIsModalOpen,
    modalService, setModalService,
    modalName, setModalName,
    modalPhone, setModalPhone,
    modalSuccess, setModalSuccess,
    
    leadName, setLeadName,
    leadPhone, setLeadPhone,
    leadService, setLeadService,
    leadSuccess, setLeadSuccess,
    
    newReviewName, setNewReviewName,
    newReviewService, setNewReviewService,
    newReviewRating, setNewReviewRating,
    newReviewText, setNewReviewText,
    
    catalogRef,
    
    isCabinetOpen, setIsCabinetOpen,
    isLoginModalOpen, setIsLoginModalOpen,
    isAuthenticated, setIsAuthenticated,
    activeCabinetTab, setActiveCabinetTab,
    
    loginPhone, setLoginPhone,
    loginCode, setLoginCode,
    loginStep, setLoginStep,
    smsTimer, setSmsTimer,
    loginError, setLoginError,
    
    userProfile, setUserProfile,
    cabinetOrders, setCabinetOrders,
    chatMessages, setChatMessages,
    chatInput, setChatInput,
    isTyping, setIsTyping,
    
    cabNewOrderCat, setCabNewOrderCat,
    cabNewOrderText, setCabNewOrderText,
    cabNewOrderSuccess, setCabNewOrderSuccess,
    profileSaveSuccess, setProfileSaveSuccess,
    newAddressInput, setNewAddressInput,
    
    handleHeroPillClick,
    handleOpenModalWithService,
    handleModalSubmit,
    handleLeadSubmit,
    handleReviewSubmit,
    handleCabinetClick,
    handleSendCode,
    handleVerifyCode,
    handleLogout,
    handleProfileSave,
    handleAddAddress,
    handleRemoveAddress,
    handleCancelOrder,
    handleCabinetNewOrder,
    handleSendChatMessage
  };
}
