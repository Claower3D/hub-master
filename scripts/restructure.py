import os

def process_file(filepath):
    print(f"Processing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Landmark 1: <!-- STATS SECTION -->
    # Landmark 2: <!-- COVERAGE ZONES SECTION -->
    
    start_landmark = "<!-- STATS SECTION -->"
    end_landmark = "<!-- COVERAGE ZONES SECTION -->"
    
    if start_landmark not in content or end_landmark not in content:
        print("ERROR: landmarks not found!")
        return
        
    start_idx = content.find(start_landmark)
    end_idx = content.find(end_landmark)
    
    new_sections = """<!-- STATS SECTION -->
    <section class="stats-section">
      <div class="max-width-wrap">
        <div class="stats-container-new">

          <!-- Row 1: Stats Grid -->
          <div class="stats-row-grid">

            <!-- Stat 1 -->
            <div class="stat-new-item">
              <div class="stat-new-icon-box">
                <svg viewBox="0 0 24 24">
                  <circle cx="9" cy="21" r="1" />
                  <circle cx="20" cy="21" r="1" />
                  <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6" />
                </svg>
              </div>
              <div class="stat-new-text">
                <span class="stat-new-val">70 000+</span>
                <span class="stat-new-lbl" data-i18n="ordersCount">выполненных заказов</span>
              </div>
            </div>

            <!-- Stat 2 -->
            <div class="stat-new-item">
              <div class="stat-new-icon-box">
                <svg viewBox="0 0 24 24" fill="currentColor" stroke="none">
                  <polygon
                    points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
                </svg>
              </div>
              <div class="stat-new-text">
                <span class="stat-new-val">4.9 ★</span>
                <span class="stat-new-lbl" data-i18n="ratingAvg">средняя оценка</span>
              </div>
            </div>

            <!-- Stat 3 -->
            <div class="stat-new-item">
              <div class="stat-new-icon-box">
                <svg viewBox="0 0 24 24">
                  <circle cx="12" cy="12" r="10" />
                  <polyline points="12 6 12 12 16 14" />
                </svg>
              </div>
              <div class="stat-new-text">
                <span class="stat-new-val" id="stat-arrival-value">45 мин</span>
                <span class="stat-new-lbl" data-i18n="arrivalTime">среднее время прибытия</span>
              </div>
            </div>

            <!-- Stat 4 -->
            <div class="stat-new-item">
              <div class="stat-new-icon-box">
                <svg viewBox="0 0 24 24">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                </svg>
              </div>
              <div class="stat-new-text">
                <span class="stat-new-val">12 мес</span>
                <span class="stat-new-lbl" data-i18n="warrantyLabel">гарантия на работы</span>
              </div>
            </div>

          </div>

          <!-- Divider -->
          <div class="stats-divider"></div>

          <!-- Row 2: Highlights -->
          <div class="highlights-row">
            <div class="highlight-item">
              <svg viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="10" />
                <polyline points="12 6 12 12 16 14" />
              </svg>
              <span data-i18n="highlightArrival">Прибытие за 45 мин</span>
            </div>

            <div class="highlight-item">
              <svg viewBox="0 0 24 24">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                <polyline points="9 11 11 13 15 9" />
              </svg>
              <span data-i18n="highlightWarranty">Гарантия 12 месяцев</span>
            </div>

            <div class="highlight-item">
              <svg viewBox="0 0 24 24">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                <circle cx="12" cy="11" r="3" />
              </svg>
              <span data-i18n="highlightControl">Контроль 24/7</span>
            </div>

            <div class="highlight-item">
              <svg viewBox="0 0 24 24">
                <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" />
                <circle cx="12" cy="13" r="4" />
              </svg>
              <span data-i18n="highlightReports">Фото/Видео отчёты</span>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- CATALOG SECTION -->
    <section class="catalog-section" id="catalog">
      <div class="max-width-wrap">
        <div class="section-header">
          <span class="section-pretitle">Каталог</span>
          <h2 class="section-title-main" data-i18n="catalogTitle">Каталог услуг</h2>
          <p class="section-subtitle-text" data-i18n="catalogSub">Более 112 видов услуг в одном месте — выберите то, что нужно</p>
        </div>

        <div class="catalog-tabs" id="catalog-tab-headers">
          <!-- Dynamically populated tabs -->
        </div>

        <div class="catalog-grid" id="catalog-items-grid">
          <!-- Dynamically populated cards -->
        </div>

        <div style="text-align: center; margin-top: 30px;">
          <button class="review-submit-btn" style="width: auto; padding: 14px 32px;" onclick="openMegaModal()" data-i18n="viewFullCatalog">Смотреть весь каталог</button>
        </div>
      </div>
    </section>

    <!-- HOW WE WORK SECTION -->
    <section class="how-we-work-section" id="how-we-work" style="padding: 80px 0; border-top: 1px solid var(--border);">
      <div class="max-width-wrap">
        <div class="section-header">
          <span class="section-pretitle" data-i18n="howWeWorkTitle">Процесс</span>
          <h2 class="section-title-main" data-i18n="howWeWorkHeading">Как мы работаем</h2>
          <p class="section-subtitle-text" data-i18n="howWeWorkSub">Всего 4 простых шага до идеального результата</p>
        </div>
        <div class="showcase-steps" style="margin-top: 40px; display: flex; justify-content: space-between; align-items: center; gap: 20px; flex-wrap: wrap;">
          <div class="step-item">
            <div class="step-circle">1</div>
            <div class="step-text" data-i18n="step1">Заявка</div>
          </div>
          <div class="step-item">
            <div class="step-circle">2</div>
            <div class="step-text" data-i18n="step2">Подбор мастера</div>
          </div>
          <div class="step-item">
            <div class="step-circle">3</div>
            <div class="step-text" data-i18n="step3">Выполнение</div>
          </div>
          <div class="step-item">
            <div class="step-circle">4</div>
            <div class="step-text" data-i18n="step4">Готово!</div>
          </div>
        </div>
      </div>
    </section>

    <!-- MASTERS SECTION -->
    <section class="masters-section" id="masters" style="padding: 80px 0; border-top: 1px solid var(--border);">
      <div class="max-width-wrap">
        <div class="section-header">
          <span class="section-pretitle" data-i18n="ourMastersTitle">Команда</span>
          <h2 class="section-title-main" data-i18n="ourMastersHeading">Наши опытные мастера</h2>
          <p class="section-subtitle-text" data-i18n="ourMastersSub">Проверенные специалисты со стажем от 5 лет</p>
        </div>
        <div class="masters-carousel-wrap" style="margin-top: 40px;">
          <button class="carousel-btn-arrow prev-btn" onclick="moveCarousel(-1)">‹</button>
          <div class="masters-carousel-container">
            <div class="masters-carousel-track" id="masters-track">
              <!-- Dynamically populated masters -->
            </div>
          </div>
          <button class="carousel-btn-arrow next-btn" onclick="moveCarousel(1)">›</button>
        </div>
      </div>
    </section>

    <!-- WHY CHOOSE US SECTION -->
    <section class="why-choose-section" id="why-choose-us" style="padding: 80px 0; border-top: 1px solid var(--border);">
      <div class="max-width-wrap">
        <div class="section-header">
          <span class="section-pretitle" data-i18n="whyTitle">Преимущества</span>
          <h2 class="section-title-main" data-i18n="whyChooseTitle">Почему выбирают нас</h2>
          <p class="section-subtitle-text" data-i18n="whySub">Премиальный сервис для вашего дома и бизнеса</p>
        </div>
        <div class="why-grid-3x3" style="margin-top: 40px;">
          <div class="why-item-new">
            <div class="why-icon-new-box"><svg viewBox="0 0 24 24"><line x1="8" y1="6" x2="21" y2="6" /><line x1="8" y1="12" x2="21" y2="12" /><line x1="8" y1="18" x2="21" y2="18" /><line x1="3" y1="6" x2="3.01" y2="6" /><line x1="3" y1="12" x2="3.01" y2="12" /><line x1="3" y1="18" x2="3.01" y2="18" /></svg></div>
            <div class="why-text-new"><span class="why-title-new" data-i18n="whyTitle1">112 Услуг</span><span class="why-desc-new" data-i18n="whyDesc1">Широкий спектр работ</span></div>
          </div>
          <div class="why-item-new">
            <div class="why-icon-new-box"><svg viewBox="0 0 24 24"><path d="M3 18v-6a9 9 0 0 1 18 0v6" /><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z" /></svg></div>
            <div class="why-text-new"><span class="why-title-new" data-i18n="whyTitle2">24/7 Поддержка</span><span class="why-desc-new" data-i18n="whyDesc2">Круглосуточная помощь</span></div>
          </div>
          <div class="why-item-new">
            <div class="why-icon-new-box"><svg viewBox="0 0 24 24"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z" /><line x1="7" y1="7" x2="7.01" y2="7" /></svg></div>
            <div class="why-text-new"><span class="why-title-new" data-i18n="whyTitle3">Прозрачные цены</span><span class="why-desc-new" data-i18n="whyDesc3">Фиксированные прайсы</span></div>
          </div>
          <div class="why-item-new">
            <div class="why-icon-new-box"><svg viewBox="0 0 24 24"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z" /></svg></div>
            <div class="why-text-new"><span class="why-title-new" data-i18n="whyTitle4">Опытные мастера</span><span class="why-desc-new" data-i18n="whyDesc4">Только профессионалы</span></div>
          </div>
          <div class="why-item-new">
            <div class="why-icon-new-box"><svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="7" /><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88" /></svg></div>
            <div class="why-text-new"><span class="why-title-new" data-i18n="whyTitle5">Гарантия качества</span><span class="why-desc-new" data-i18n="whyDesc5">До 1 года на работы</span></div>
          </div>
          <div class="why-item-new">
            <div class="why-icon-new-box"><svg viewBox="0 0 24 24"><rect x="1" y="3" width="15" height="13" /><polygon points="16 8 20 8 23 11 23 16 16 16 16 8" /><circle cx="5.5" cy="18.5" r="2.5" /><circle cx="18.5" cy="18.5" r="2.5" /></svg></div>
            <div class="why-text-new"><span class="why-title-new" data-i18n="whyTitle6">Быстрый выезд</span><span class="why-desc-new" data-i18n="whyDesc6">В течение 1 часа</span></div>
          </div>
          <div class="why-item-new">
            <div class="why-icon-new-box"><svg viewBox="0 0 24 24"><rect x="1" y="4" width="22" height="16" rx="2" ry="2" /><line x1="1" y1="10" x2="23" y2="10" /></svg></div>
            <div class="why-text-new"><span class="why-title-new" data-i18n="whyTitle7">Безопасная оплата</span><span class="why-desc-new" data-i18n="whyDesc7">Картой или наличными</span></div>
          </div>
          <div class="why-item-new">
            <div class="why-icon-new-box"><svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" /></svg></div>
            <div class="why-text-new"><span class="why-title-new" data-i18n="whyTitle9">Контроль качества</span><span class="why-desc-new" data-i18n="whyDesc9">Постоянный мониторинг</span></div>
          </div>
        </div>
      </div>
    </section>

    <!-- REVIEWS SECTION -->
    <section class="reviews-section" id="reviews" style="padding: 80px 0; border-top: 1px solid var(--border);">
      <div class="max-width-wrap">
        <div class="section-header">
          <span class="section-pretitle" data-i18n="reviewsPreTitle">Отзывы</span>
          <h2 class="section-title-main" data-i18n="reviewsTitle">Отзывы клиентов</h2>
          <p class="section-subtitle-text" data-i18n="reviewsSub">Более 50 000 довольных клиентов — лучшее подтверждение нашей работы</p>
        </div>

        <div class="showcase-stats-row" style="margin-top: 30px; margin-bottom: 40px; background: var(--bg-card); padding: 30px; border-radius: 20px; border: 1px solid var(--border);">
          <!-- Rating Left -->
          <div class="stats-left">
            <div class="rating-big">4.9</div>
            <div class="rating-stars-col">
              <div class="star-row">
                <span>5 ★</span>
                <div class="star-bar"><div class="star-bar-fill" style="width: 95%;"></div></div>
              </div>
              <div class="star-row">
                <span>4 ★</span>
                <div class="star-bar"><div class="star-bar-fill" style="width: 25%;"></div></div>
              </div>
              <div class="star-row">
                <span>3 ★</span>
                <div class="star-bar"><div class="star-bar-fill" style="width: 5%;"></div></div>
              </div>
            </div>
            <div class="satisfied-badge">98%<span data-i18n="satisfied">довольных</span></div>
          </div>

          <!-- Reviews Grid -->
          <div class="reviews-scroll" style="display: flex; gap: 16px; overflow-x: auto; padding-bottom: 10px;">
            <div class="review-mini-card" style="flex: 0 0 300px;">
              <div class="review-mini-header">
                <div class="review-mini-avatar" style="background-image: url('https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=100&q=80');"></div>
                <div class="review-mini-name">Айжан К.</div>
              </div>
              <div class="review-mini-text">Очень быстро и качественно, спасибо мастеру...</div>
              <div class="review-mini-stars">★★★★★</div>
            </div>
            <div class="review-mini-card" style="flex: 0 0 300px;">
              <div class="review-mini-header">
                <div class="review-mini-avatar" style="background-image: url('https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=100&q=80');"></div>
                <div class="review-mini-name">Айдар В.</div>
              </div>
              <div class="review-mini-text">Оперативно приехали, починили диван. Сервис огонь.</div>
              <div class="review-mini-stars">★★★★★</div>
            </div>
            <div class="review-mini-card" style="flex: 0 0 300px;">
              <div class="review-mini-header">
                <div class="review-mini-avatar" style="background-image: url('https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&q=80');"></div>
                <div class="review-mini-name">Данияр Н.</div>
              </div>
              <div class="review-mini-text">Все отлично, мастер профи своего дела.</div>
              <div class="review-mini-stars">★★★★★</div>
            </div>
          </div>
        </div>

        <div class="reviews-grid" id="reviews-cards-grid">
          <!-- Dynamically populated reviews -->
        </div>

        <div style="text-align: center; margin-top: 30px;">
          <button class="review-submit-btn" style="width: auto; padding: 14px 32px;" onclick="openReviewModal()" data-i18n="writeReview">Оставить отзыв</button>
        </div>
      </div>
    </section>
"""
    
    content = content[:start_idx] + new_sections + content[end_idx:]
    
    # 2. Add final CTA before closing div of landing-page-content
    cta_landmark = "<!-- THEMATIC PAGE CONTAINER -->"
    if cta_landmark not in content:
        print("ERROR: THEMATIC PAGE CONTAINER landmark not found!")
        return
        
    cta_idx = content.find(cta_landmark)
    closing_div_idx = content.rfind("</div>", 0, cta_idx)
    
    final_cta = """    <!-- FINAL CTA SECTION -->
    <section class="lead-section" id="final-cta" style="padding: 80px 0; border-top: 1px solid var(--border);">
      <div class="max-width-wrap lead-inner-box">
        <div class="lead-text-box">
          <h3 data-i18n="leaveRequest">Оставьте заявку — перезвоним за 10 минут</h3>
          <p data-i18n="leaveRequestSub">Наши менеджеры ответят на любые ваши вопросы и оперативно подберут лучшего мастера</p>
          <div class="lead-features-small">
            <div class="lead-feat-item">
              <svg viewBox="0 0 24 24" stroke="currentColor" fill="none" strokeWidth="2.5"><polyline points="20 6 9 17 4 12" /></svg>
              <span data-i18n="feat1">Выезд бесплатно</span>
            </div>
            <div class="lead-feat-item">
              <svg viewBox="0 0 24 24" stroke="currentColor" fill="none" strokeWidth="2.5"><polyline points="20 6 9 17 4 12" /></svg>
              <span data-i18n="feat2">Гарантия качества</span>
            </div>
            <div class="lead-feat-item">
              <svg viewBox="0 0 24 24" stroke="currentColor" fill="none" strokeWidth="2.5"><polyline points="20 6 9 17 4 12" /></svg>
              <span data-i18n="feat3">Опытные специалисты</span>
            </div>
            <div class="lead-feat-item">
              <svg viewBox="0 0 24 24" stroke="currentColor" fill="none" strokeWidth="2.5"><polyline points="20 6 9 17 4 12" /></svg>
              <span data-i18n="feat4">Работаем 24/7</span>
            </div>
          </div>
        </div>

        <div class="lead-form-box" id="lead-form-container">
          <form onsubmit="handleLeadSubmit(event)">
            <div class="form-group" style="margin-bottom: 14px;">
              <label class="form-label" data-i18n="yourName">Ваше имя</label>
              <input type="text" id="lead-name" class="form-input" required placeholder="Ерлан">
            </div>
            <div class="form-group" style="margin-bottom: 14px;">
              <label class="form-label" data-i18n="yourPhone">Номер телефона</label>
              <input type="tel" id="lead-phone" class="form-input" required placeholder="+7 (705) 846-2749">
            </div>
            <div class="form-group" style="margin-bottom: 14px;">
              <label class="form-label" data-i18n="selectService">Выберите услугу</label>
              <select id="lead-service-select" class="form-select">
                <!-- Dynamically populated options -->
              </select>
            </div>
            <div class="form-group" style="margin-bottom: 14px;">
              <label class="form-label" data-i18n="selectCity">Выберите город</label>
              <select id="lead-city-select" class="form-select">
                <option value="almaty" data-i18n="selectCityAlmaty">Алматы</option>
                <option value="astana" data-i18n="selectCityAstana">Астана</option>
              </select>
            </div>
            <div class="form-group" style="margin-bottom: 14px;">
              <label class="form-label" data-i18n="yourAddress">Адрес (необязательно)</label>
              <input type="text" id="lead-address" class="form-input" placeholder="ул. Абая, д. 10, кв. 5">
            </div>
            <div class="form-group" style="margin-bottom: 20px;">
              <label class="form-label" data-i18n="problemDescription">Описание проблемы (необязательно)</label>
              <textarea id="lead-comment" class="form-input" style="height: 80px; resize: none;" placeholder="Опишите в двух словах вашу проблему..."></textarea>
            </div>
            <button type="submit" class="review-submit-btn" data-i18n="sendRequest">Отправить заявку</button>
          </form>
        </div>

        <div class="lead-form-box lead-form-success" id="lead-success-container" style="display: none;">
          <div class="success-icon-badge">
            <svg viewBox="0 0 24 24" stroke="#25d366" fill="none" strokeWidth="2.5">
              <polyline points="20 6 9 17 4 12" />
            </svg>
          </div>
          <h4 class="success-title" data-i18n="successTitle">Заявка успешно принята!</h4>
          <p class="success-message" data-i18n="successDesc">Мы свяжемся с вами в течение 10 минут. Спасибо!</p>
        </div>
      </div>
    </section>
"""
    
    content = content[:closing_div_idx] + final_cta + content[closing_div_idx:]
    
    # 3. Add review modal after language modal
    lang_modal_landmark = "lang-select-modal-overlay"
    if lang_modal_landmark not in content:
        print("ERROR: lang-select-modal-overlay not found!")
        return
        
    lang_idx = content.find(lang_modal_landmark)
    first_close = content.find("</div>", lang_idx)
    second_close = content.find("</div>", first_close + 6)
    insert_modal_idx = second_close + 6
    
    review_modal = """
  <!-- REVIEW MODAL -->
  <div class="modal-overlay" id="review-modal-overlay" onclick="handleOutsideReviewModalClick(event)">
    <div class="modal-box" style="max-width: 500px; width: 90%; text-align: left; padding: 30px;">
      <button class="modal-close-btn" onclick="closeReviewModal()" aria-label="Close modal">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <line x1="18" y1="6" x2="6" y2="18" />
          <line x1="6" y1="6" x2="18" y2="18" />
        </svg>
      </button>
      <div class="write-review-container" style="background: none; border: none; padding: 0;">
        <h3 class="review-form-title" data-i18n="writeReview" style="margin-top: 0;">Оставить отзыв</h3>
        <form onsubmit="handleReviewSubmit(event)">
          <div class="review-form-grid" style="display: flex; flex-direction: column; gap: 14px;">
            <div class="form-group">
              <label class="form-label" data-i18n="yourName">Ваше имя</label>
              <input type="text" id="rev-name" class="form-input" required placeholder="Алексей">
            </div>
            <div class="form-group">
              <label class="form-label" data-i18n="selectService">Выберите услугу</label>
              <select id="rev-service" class="form-select" required>
                <option value="" data-i18n="selectPrompt">-- Выберите --</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label" data-i18n="ratingLabel">Оценка</label>
              <div class="rating-stars-select" id="rev-rating-stars" style="display: flex; gap: 6px;">
                <button type="button" class="star-select-btn active" data-rating="1" onclick="setReviewRating(1)">★</button>
                <button type="button" class="star-select-btn active" data-rating="2" onclick="setReviewRating(2)">★</button>
                <button type="button" class="star-select-btn active" data-rating="3" onclick="setReviewRating(3)">★</button>
                <button type="button" class="star-select-btn active" data-rating="4" onclick="setReviewRating(4)">★</button>
                <button type="button" class="star-select-btn active" data-rating="5" onclick="setReviewRating(5)">★</button>
              </div>
            </div>
            <div class="form-group">
              <label class="form-label" data-i18n="reviewText">Текст отзыва</label>
              <textarea rows="3" id="rev-text" class="form-textarea" required placeholder="Напишите ваш отзыв здесь..."></textarea>
            </div>
          </div>
          <button type="submit" class="review-submit-btn" style="margin-top: 20px;" data-i18n="submitReview">Отправить отзыв</button>
        </form>
      </div>
    </div>
  </div>
"""
    content = content[:insert_modal_idx] + review_modal + content[insert_modal_idx:]
    
    # 4. Update handleReviewSubmit
    submit_landmark = "function handleReviewSubmit(e) {"
    if submit_landmark not in content:
        print("ERROR: handleReviewSubmit not found!")
        return
        
    submit_idx = content.find(submit_landmark)
    reset_text = "setReviewRating(5);"
    reset_idx = content.find(reset_text, submit_idx)
    next_brace_idx = content.find("}", reset_idx)
    
    content = content[:next_brace_idx] + "  closeReviewModal();\n    }" + content[next_brace_idx+1:]
    
    # 5. Add JavaScript helpers
    outside_landmark = "function handleOutsideModalClick(e) {"
    if outside_landmark not in content:
        print("ERROR: handleOutsideModalClick not found!")
        return
        
    outside_idx = content.find(outside_landmark)
    outside_end_idx = content.find("}", outside_idx) + 1
    
    helper_js = """

    window.openReviewModal = function() {
      const modal = document.getElementById('review-modal-overlay');
      if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
      }
    };

    window.closeReviewModal = function() {
      const modal = document.getElementById('review-modal-overlay');
      if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
      }
    };

    window.handleOutsideReviewModalClick = function(e) {
      if (e.target.id === 'review-modal-overlay') {
        closeReviewModal();
      }
    };
"""
    content = content[:outside_end_idx] + helper_js + content[outside_end_idx:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"SUCCESS processing {filepath}")

process_file("index.html")
process_file("hubmaster.html")
