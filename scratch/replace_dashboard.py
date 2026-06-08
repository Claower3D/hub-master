import os

files = [
    r"C:\Users\SystemX\Downloads\1\index.html",
    r"C:\Users\SystemX\Downloads\1\hubmaster.html"
]

for file_path in files:
    if not os.path.exists(file_path):
        print(f"Skipping {file_path} (does not exist)")
        continue
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. HTML Replacement
    target_html_start = "<!-- Step 2: Authenticated Cabinet Dashboard container -->"
    target_html_end = """          <!-- TAB: WARRANTIES -->
          <div id="cab-tab-content-warranties" style="display: none;">
            <h3 style="font-family: var(--font-heading); font-size: 20px; font-weight: 800; color: #fff; margin-bottom: 8px;">Гарантийные обязательства</h3>
            <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 20px;">Электронные гарантийные талоны по вашим завершенным заказам.</p>
            
            <div id="cab-warranties-list" style="display: flex; flex-direction: column; gap: 16px;">
              <!-- Warranty certificates dynamically built -->
            </div>
          </div>

        </div>
      </div>"""

    # Let's find the indexes
    start_idx = content.find(target_html_start)
    if start_idx == -1:
        print(f"Error: target_html_start not found in {file_path}")
        continue

    # Find the style block after target_html_start
    style_idx = content.find("<style>", start_idx)
    if style_idx == -1:
        print(f"Error: <style> not found after target_html_start in {file_path}")
        continue

    end_idx = content.find(target_html_end, style_idx)
    if end_idx == -1:
        print(f"Error: target_html_end not found in {file_path}")
        continue

    # We want to replace from style_idx to end_idx + len(target_html_end)
    replacement_html = """<style>
        .cab-nav-tab {
          width: 100%;
          background: none;
          border: none;
          text-align: left;
          padding: 12px 16px;
          border-radius: 10px;
          font-size: 14px;
          font-weight: 600;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 12px;
          transition: all 0.2s ease;
          outline: none;
          font-family: var(--font-sans);
          color: #a1a1aa !important;
        }
        .cab-nav-tab:hover {
          color: #fff !important;
          background: rgba(255, 255, 255, 0.03) !important;
        }
        .cab-nav-tab.active {
          color: #fff !important;
          background: #e63333 !important;
        }
        .cab-logout-btn:hover {
          background: rgba(239, 68, 68, 0.08) !important;
        }
        @keyframes float-sparkle {
          0%, 100% { transform: translateY(0) scale(1); }
          50% { transform: translateY(-4px) scale(1.1); }
        }
      </style>
      <div id="cab-dashboard-container" style="display: none; flex: 1; flex-direction: row; min-height: 580px; background: #121215;">

        <!-- LEFT SIDEBAR -->
        <div class="cab-sidebar" style="width: 280px; background: #0f1015; border-right: 1px solid #1f212a; display: flex; flex-direction: column; padding: 24px; flex-shrink: 0; box-sizing: border-box; justify-content: space-between;">
          <div style="display: flex; flex-direction: column; gap: 24px; width: 100%;">
            
            <!-- User Profile Header -->
            <div style="display: flex; align-items: center; gap: 14px;">
              <div id="cab-avatar" style="width: 48px; height: 48px; border-radius: 50%; background: linear-gradient(135deg, #e63333 0%, #991b1b 100%); display: flex; align-items: center; justify-content: center; font-weight: 700; color: #fff; font-size: 16px;">
                ГМ
              </div>
              <div style="display: flex; flex-direction: column;">
                <span id="cab-user-name" style="font-size: 15px; font-weight: 700; color: #fff; line-height: 1.2;">Галимов Максим</span>
                <span id="cab-user-phone" style="font-size: 12px; color: #71717a; margin-top: 4px;">+77000937002</span>
              </div>
            </div>
            
            <!-- Status Card -->
            <div style="background: rgba(230, 51, 51, 0.04); border: 1px solid rgba(230, 51, 51, 0.15); border-radius: 14px; padding: 16px; transition: all 0.3s ease;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <span style="font-size: 10px; font-weight: 700; color: #71717a; text-transform: uppercase; letter-spacing: 0.05em;">СТАТУС</span>
                <span style="background: #e63333; color: #fff; font-size: 9px; font-weight: 800; padding: 2px 8px; border-radius: 9999px; text-transform: uppercase; letter-spacing: 0.05em; transition: all 0.3s ease;">GOLD</span>
              </div>
              <div style="margin-bottom: 12px;">
                <div style="font-size: 14px; font-weight: 700; color: #fff;">Бонусы: <span id="cab-status-bonus-amount" style="color: #e63333; transition: all 0.3s ease;">2 500</span> ₸</div>
              </div>
              <div>
                <div style="display: flex; justify-content: space-between; font-size: 10px; color: #a1a1aa; margin-bottom: 6px;">
                  <span>До платинового уровня:</span>
                  <span id="cab-status-target" style="font-weight: 600;">7 500 ₸</span>
                </div>
                <div style="width: 100%; height: 5px; background: #27272a; border-radius: 9999px; overflow: hidden;">
                  <div id="cab-status-progress" style="width: 25%; height: 100%; background: #e63333; border-radius: 9999px; transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1), background-color 0.4s ease;"></div>
                </div>
              </div>
            </div>
            
            <!-- Menu Navigation -->
            <div style="display: flex; flex-direction: column; gap: 6px;">
              <button onclick="switchCabinetTab('main')" id="cab-tab-btn-main" class="cab-nav-tab active">
                <i class="ri-dashboard-line" style="font-size: 18px;"></i>
                Главная
              </button>
              <button onclick="switchCabinetTab('orders')" id="cab-tab-btn-orders" class="cab-nav-tab">
                <i class="ri-file-list-3-line" style="font-size: 18px;"></i>
                Мои заказы
              </button>
              <button onclick="switchCabinetTab('profile')" id="cab-tab-btn-profile" class="cab-nav-tab">
                <i class="ri-user-3-line" style="font-size: 18px;"></i>
                Профиль
              </button>
              <button onclick="switchCabinetTab('warranties')" id="cab-tab-btn-warranties" class="cab-nav-tab">
                <i class="ri-shield-check-line" style="font-size: 18px;"></i>
                Гарантии
              </button>
              <button onclick="switchCabinetTab('bonuses')" id="cab-tab-btn-bonuses" class="cab-nav-tab">
                <i class="ri-qr-scan-line" style="font-size: 18px;"></i>
                Бонусы & QR
              </button>
              <button onclick="switchCabinetTab('chat')" id="cab-tab-btn-chat" class="cab-nav-tab">
                <i class="ri-chat-3-line" style="font-size: 18px;"></i>
                Поддержка 24/7
              </button>
            </div>
            
          </div>
          
          <button onclick="logoutCabinet()" class="cab-logout-btn" style="background: none; border: none; width: 100%; text-align: left; padding: 12px 16px; border-radius: 10px; font-size: 14px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 12px; transition: all 0.2s; outline: none; font-family: var(--font-sans); color: #ef4444;">
            <i class="ri-logout-box-r-line" style="font-size: 18px;"></i>
            Выйти
          </button>
        </div>
        
        <!-- RIGHT CONTENT PANEL -->
        <div style="flex: 1; padding: 32px; overflow-y: auto; background: #121215; display: flex; flex-direction: column; box-sizing: border-box;">

          <!-- TAB: MAIN -->
          <div id="cab-tab-content-main">
            <h3 style="font-family: var(--font-heading); font-size: 24px; font-weight: 800; color: #fff; margin-bottom: 24px; display: flex; align-items: center; gap: 8px;">
              Панель управления
            </h3>
            
            <div style="display: grid; grid-template-columns: 1fr; gap: 24px;">
              <!-- Quick order card -->
              <div style="background: #18181c; border: 1px solid #222226; border-radius: 16px; padding: 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.15);">
                <h4 style="font-family: var(--font-sans); font-size: 16px; font-weight: 700; color: #fff; margin-bottom: 16px; display: flex; align-items: center; gap: 8px;">
                  <i class="ri-flashlight-line" style="color: #e63333;"></i>
                  Быстрый заказ
                </h4>
                <div style="display: flex; flex-direction: column; gap: 14px; margin-bottom: 16px;">
                  <select id="cab-quick-service" class="form-input" style="background: #121215; border-color: #222226; color: #fff; width: 100%; height: 46px; border-radius: 8px;">
                    <option value="furniture">Ремонт мебели</option>
                    <option value="windows">Ремонт окон</option>
                    <option value="appliances">Бытовая техника</option>
                    <option value="plumbing">Сантехника</option>
                    <option value="electric">Электрика</option>
                    <option value="cleaning">Клининг</option>
                  </select>
                  <input type="text" id="cab-quick-details" class="form-input" placeholder="Детали (например: сломалась петля)" style="background: #121215; border-color: #222226; color: #fff; width: 100%; height: 46px; border-radius: 8px;">
                </div>
                <button onclick="createQuickOrder()" class="review-submit-btn" style="padding: 12px 24px; border-radius: 10px; font-weight: 700; background: #e63333; color: white; border: none; cursor: pointer; transition: all 0.2s;">
                  Создать быстрый заказ
                </button>
                <div id="cab-quick-success" style="color: #25d366; font-size: 13px; margin-top: 8px; display: none;">Заказ успешно добавлен!</div>
              </div>

              <!-- Active Orders List -->
              <div>
                <h4 style="font-family: var(--font-sans); font-size: 16px; font-weight: 700; color: #fff; margin-bottom: 16px; display: flex; align-items: center; gap: 8px;">
                  <i class="ri-time-line" style="color: #e63333;"></i>
                  Активные заказы
                </h4>
                <div id="cab-active-orders" style="display: flex; flex-direction: column; gap: 12px;">
                  <!-- Dynamic orders inserted here -->
                </div>
              </div>
            </div>
          </div>

          <!-- TAB: ORDERS -->
          <div id="cab-tab-content-orders" style="display: none;">
            <h3 style="font-family: var(--font-heading); font-size: 20px; font-weight: 800; color: #fff; margin-bottom: 20px;">
              История заказов</h3>
            <div id="cab-all-orders" style="display: flex; flex-direction: column; gap: 12px;">
              <!-- All orders list -->
            </div>
          </div>

          <!-- TAB: PROFILE -->
          <div id="cab-tab-content-profile" style="display: none;">
            <h3 style="font-family: var(--font-heading); font-size: 20px; font-weight: 800; color: #fff; margin-bottom: 20px;">
              Личные данные</h3>

            <div style="background: #18181c; border: 1px solid #222226; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
              <div style="display: flex; flex-direction: column; gap: 12px; margin-bottom: 12px;">
                <div>
                  <label class="form-label" style="font-size: 11px; margin-bottom: 6px; color: var(--text);">Имя</label>
                  <input type="text" id="cab-profile-name" class="form-input" style="background: #121215; border-color: #222226; color: #fff;">
                </div>
                <div>
                  <label class="form-label" style="font-size: 11px; margin-bottom: 6px; color: var(--text);">Email</label>
                  <input type="email" id="cab-profile-email" class="form-input" style="background: #121215; border-color: #222226; color: #fff;">
                </div>
                <div>
                  <label class="form-label" style="font-size: 11px; margin-bottom: 6px; color: var(--text);">Город</label>
                  <select id="cab-profile-city" class="form-input" style="background: #121215; border-color: #222226; color: #fff; width: 100%;">
                    <option value="almaty">Алматы</option>
                    <option value="astana">Астана</option>
                    <option value="shymkent">Шымкент</option>
                    <option value="karaganda">Караганда</option>
                  </select>
                </div>
              </div>
              <button onclick="saveCabinetProfile()" class="review-submit-btn" style="padding: 10px 20px; border-radius: 8px;">Сохранить изменения</button>
              <div id="cab-profile-success" style="color: #25d366; font-size: 13px; margin-top: 8px; display: none;">
                Профиль обновлен!</div>
            </div>

            <!-- Saved Addresses -->
            <h4 style="font-family: var(--font-sans); font-size: 15px; font-weight: 700; color: #fff; margin-bottom: 12px;">
              Адреса доставки</h4>
            <div style="background: #18181c; border: 1px solid #222226; border-radius: 12px; padding: 20px;">
              <div id="cab-address-list" style="display: flex; flex-direction: column; gap: 8px; margin-bottom: 16px;">
                <!-- Address items -->
              </div>
              <div style="display: flex; gap: 12px;">
                <input type="text" id="cab-new-address" class="form-input" placeholder="Новый адрес" style="background: #121215; border-color: #222226; color: #fff; flex: 1;">
                <button onclick="addCabinetAddress()" class="review-submit-btn" style="padding: 10px 20px; white-space: nowrap; border-radius: 8px;">Добавить адрес</button>
              </div>
            </div>
          </div>

          <!-- TAB: CHAT -->
          <div id="cab-tab-content-chat" style="display: none; height: 100%; flex-direction: column; flex: 1;">
            <h3 style="font-family: var(--font-heading); font-size: 20px; font-weight: 800; color: #fff; margin-bottom: 12px;">
              Ассистент Иришка</h3>

            <div style="flex: 1; min-height: 300px; display: flex; flex-direction: column; background: #18181c; border: 1px solid #222226; border-radius: 12px; overflow: hidden;">
              <!-- Messages log -->
              <div id="cab-chat-messages" style="flex: 1; padding: 16px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; max-height: 280px;">
                <!-- Message items -->
              </div>

              <!-- Input area -->
              <div style="display: flex; border-top: 1px solid #222226; padding: 10px; gap: 8px; background: #0f0f12; margin-top: auto;">
                <input type="text" id="cab-chat-input" onkeydown="if(event.key === 'Enter') sendCabinetChatMessage()" placeholder="Напишите сообщение..." style="background: #18181c; border-color: #222226; color: #fff; flex: 1; border-radius: 8px; padding: 10px 14px; outline: none; border: 1px solid #222226;">
                <button onclick="sendCabinetChatMessage()" class="review-submit-btn" style="padding: 10px 20px; border-radius: 8px;">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width: 16px; height: 16px; transform: rotate(45deg);">
                    <line x1="22" y1="2" x2="11" y2="13" />
                    <polygon points="22 2 15 22 11 13 2 9 22 2" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- TAB: WARRANTIES -->
          <div id="cab-tab-content-warranties" style="display: none;">
            <h3 style="font-family: var(--font-heading); font-size: 20px; font-weight: 800; color: #fff; margin-bottom: 8px;">Гарантийные обязательства</h3>
            <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 20px;">Электронные гарантийные талоны по вашим завершенным заказам.</p>
            
            <div id="cab-warranties-list" style="display: flex; flex-direction: column; gap: 16px;">
              <!-- Warranty certificates dynamically built -->
            </div>
          </div>

          <!-- TAB: BONUSES -->
          <div id="cab-tab-content-bonuses" style="display: none;">
            <h3 style="font-family: var(--font-heading); font-size: 24px; font-weight: 800; color: #fff; margin-bottom: 8px;">Система лояльности</h3>
            <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 24px;">Получайте кэшбэк бонусами и сканируйте QR-коды для пополнения баланса.</p>
            
            <!-- Premium Emerald/Gold Loyalty Card -->
            <div class="cab-bonus-card" id="loyalty-card-visual" style="background: linear-gradient(135deg, #022c22 0%, #064e3b 50%, #022c22 100%); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 20px; padding: 30px; margin-bottom: 28px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 10px 30px rgba(0,0,0,0.3); position: relative; overflow: hidden; font-family: var(--font-sans); transition: all 0.5s ease;">
              
              <!-- Sparkle effects -->
              <div style="position: absolute; top: -20px; right: -20px; width: 150px; height: 150px; background: radial-gradient(circle, rgba(16, 185, 129, 0.15) 0%, transparent 70%); filter: blur(20px);"></div>
              
              <div style="display: flex; flex-direction: column; gap: 14px; z-index: 2;">
                <div style="font-size: 10px; text-transform: uppercase; font-weight: 800; color: rgba(255,255,255,0.5); letter-spacing: 1.5px;">БАЛАНС БОНУСОВ</div>
                <div style="display: flex; align-items: center; gap: 10px;">
                  <span id="cab-bonus-amount" style="font-size: 42px; font-weight: 800; color: #fff; font-family: var(--font-heading); text-shadow: 0 2px 10px rgba(0,0,0,0.3);">0</span>
                  <span style="font-size: 28px; animation: float-sparkle 3s ease-in-out infinite; display: inline-block;">✨</span>
                </div>
                <div style="font-size: 13px; color: rgba(255,255,255,0.7); line-height: 1.6; max-width: 420px;">
                  Накапливайте бонусы после каждого выполненного заказа. Сканируйте QR-коды с чеков для мгновенного начисления.
                </div>
                
                <button onclick="openQrScannerModal()" class="cab-bonus-scan-btn" style="background: #10b981; border: none; border-radius: 10px; padding: 12px 20px; color: #fff; font-size: 14px; font-weight: 700; cursor: pointer; display: flex; align-items: center; gap: 10px; transition: all 0.2s; outline: none; margin-top: 12px; font-family: var(--font-sans); box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);">
                  <i class="ri-qr-scan-2-line" style="font-size: 16px;"></i>
                  Сканировать QR-код с чека
                </button>
              </div>
              
              <!-- Double circular target style decoration on the right side -->
              <div style="width: 100px; height: 100px; border-radius: 50%; border: 2px solid rgba(16, 185, 129, 0.2); display: flex; align-items: center; justify-content: center; background: rgba(16, 185, 129, 0.05); flex-shrink: 0; z-index: 2; margin-right: 12px; position: relative;">
                <div style="width: 76px; height: 76px; border-radius: 50%; border: 1.5px dashed rgba(16, 185, 129, 0.4); display: flex; align-items: center; justify-content: center;">
                  <i class="ri-shield-user-line" style="font-size: 36px; color: #10b981;"></i>
                </div>
              </div>
            </div>
            
            <!-- Perks & Levels Info -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 28px;">
              <div style="background: #18181c; border: 1px solid #222226; border-radius: 14px; padding: 20px;">
                <h4 style="font-size: 15px; font-weight: 700; color: #fff; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                  <span style="display: inline-block; width: 8px; height: 8px; background: #e63333; border-radius: 50%;"></span>
                  Уровень GOLD
                </h4>
                <p style="font-size: 13px; color: var(--text-muted); line-height: 1.5;">Базовый уровень, активный при балансе до 10 000 бонусов. Кэшбэк 5% со всех заказов, стандартные условия гарантии.</p>
              </div>
              <div style="background: #18181c; border: 1px solid #222226; border-radius: 14px; padding: 20px;">
                <h4 style="font-size: 15px; font-weight: 700; color: #3b82f6; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                  <span style="display: inline-block; width: 8px; height: 8px; background: #3b82f6; border-radius: 50%;"></span>
                  Уровень PLATINUM
                </h4>
                <p style="font-size: 13px; color: var(--text-muted); line-height: 1.5;">Активируется автоматически при достижении 10 000 бонусов. Увеличивает кэшбэк до 10%, дает право на приоритетный выезд мастера за 30 минут.</p>
              </div>
            </div>
            
            <!-- Bonus Transactions History -->
            <h4 style="font-size: 16px; font-weight: 700; color: #fff; margin-bottom: 14px;">История начисления бонусов</h4>
            <div style="background: #18181c; border: 1px solid #222226; border-radius: 14px; overflow: hidden;">
              <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 13px;">
                <thead>
                  <tr style="border-bottom: 1px solid #222226; background: rgba(255,255,255,0.02);">
                    <th style="padding: 12px 16px; color: #71717a; font-weight: 600;">Дата</th>
                    <th style="padding: 12px 16px; color: #71717a; font-weight: 600;">Операция</th>
                    <th style="padding: 12px 16px; color: #71717a; font-weight: 600;">Статус</th>
                    <th style="padding: 12px 16px; color: #71717a; font-weight: 600; text-align: right;">Сумма</th>
                  </tr>
                </thead>
                <tbody id="cab-bonus-history-rows">
                  <!-- Dynamic rows -->
                </tbody>
              </table>
            </div>
          </div>

        </div>
      </div>"""

    # Replace content from style_idx to end_idx + len(target_html_end)
    new_content = content[:style_idx] + replacement_html + content[end_idx + len(target_html_end):]

    # 2. Javascript Replacements
    # We will define updateLoyaltyStatusUI, renderBonusesTab and update switchCabinetTab
    js_target = """    window.switchCabinetTab = function (tab) {
      ['main', 'orders', 'profile', 'chat', 'warranties'].forEach(t => {
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
      }
    };"""

    js_replacement = """    window.updateLoyaltyStatusUI = function(bonuses) {
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
    };"""

    # Replace js_target
    new_content = new_content.replace(js_target, js_replacement)

    # Update showDashboard
    show_dashboard_target = """    function showDashboard(user, token) {
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

      const bonusEl = document.getElementById('cab-bonus-amount');
      if (bonusEl) bonusEl.innerText = user.bonuses || '0';

      if (window.pendingCabinetTab) {
        switchCabinetTab(window.pendingCabinetTab);
        window.pendingCabinetTab = null;
      } else {
        switchCabinetTab('main');
      }
      loadUserOrders(token);
    }"""

    show_dashboard_replacement = """    function showDashboard(user, token) {
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
    }"""

    new_content = new_content.replace(show_dashboard_target, show_dashboard_replacement)

    # Update simulateQrScanSuccess
    simulate_target = """            // Update local user object
            let localUser = JSON.parse(localStorage.getItem('cab_user') || '{}');
            localUser.bonuses = data.user.bonuses;
            localStorage.setItem('cab_user', JSON.stringify(localUser));

            // Update UI elements
            const bonusEl = document.getElementById('cab-bonus-amount');
            if (bonusEl) bonusEl.innerText = data.user.bonuses;"""

    simulate_replacement = """            // Update local user object
            let localUser = JSON.parse(localStorage.getItem('cab_user') || '{}');
            localUser.bonuses = data.user.bonuses;
            localStorage.setItem('cab_user', JSON.stringify(localUser));

            // Update UI elements
            updateLoyaltyStatusUI(data.user.bonuses);
            renderBonusesTab();"""

    new_content = new_content.replace(simulate_target, simulate_replacement)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Successfully updated {file_path}")
