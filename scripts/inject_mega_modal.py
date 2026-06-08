import re

with open('hubmaster.html', 'r', encoding='utf-8') as f:
    html = f.read()

css_inject = '''
    /* Mega Catalog Modal */
    .mega-catalog-modal {
      width: 960px;
      max-width: 95%;
      height: 640px;
      max-height: 90vh;
      background: var(--bg-card);
      border-radius: 16px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      position: relative;
    }
    .mega-catalog-header {
      padding: 16px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--border);
    }
    .mega-catalog-title {
      font-family: var(--font-heading);
      font-size: 20px;
      font-weight: 800;
      color: var(--text-white);
    }
    .mega-catalog-close {
      background: rgba(255,255,255,0.05);
      border: none;
      border-radius: 50%;
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      color: var(--text);
      transition: background 0.2s;
    }
    .mega-catalog-close:hover {
      background: rgba(255,255,255,0.1);
      color: var(--text-white);
    }
    [data-theme="light"] .mega-catalog-close {
      background: rgba(0,0,0,0.05);
    }
    [data-theme="light"] .mega-catalog-close:hover {
      background: rgba(0,0,0,0.1);
    }
    .mega-catalog-body {
      display: grid;
      grid-template-columns: 240px 280px 1fr;
      flex: 1;
      overflow: hidden;
    }
    .mega-col {
      overflow-y: auto;
      padding: 20px;
      border-right: 1px solid var(--border);
    }
    .mega-col:last-child {
      border-right: none;
      background: rgba(0,0,0,0.2);
    }
    [data-theme="light"] .mega-col:last-child {
      background: #f9f9fb;
    }
    .mega-cat-btn {
      display: flex;
      align-items: center;
      gap: 12px;
      width: 100%;
      padding: 12px 16px;
      background: none;
      border: none;
      text-align: left;
      color: var(--text);
      font-size: 14px;
      font-weight: 500;
      border-radius: 8px;
      cursor: pointer;
      margin-bottom: 4px;
      transition: 0.2s;
      position: relative;
    }
    .mega-cat-btn:hover {
      background: rgba(255,255,255,0.05);
    }
    [data-theme="light"] .mega-cat-btn:hover {
      background: rgba(0,0,0,0.05);
    }
    .mega-cat-btn.active {
      color: var(--primary);
      background: rgba(230, 51, 51, 0.05);
      font-weight: 600;
    }
    .mega-cat-btn.active::before {
      content: '';
      position: absolute;
      left: 0;
      top: 10px;
      bottom: 10px;
      width: 3px;
      background: var(--primary);
      border-radius: 0 4px 4px 0;
    }
    .mega-item-btn {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
      padding: 12px 16px;
      background: none;
      border: none;
      text-align: left;
      color: var(--text);
      font-size: 13px;
      border-radius: 8px;
      cursor: pointer;
      margin-bottom: 4px;
      transition: 0.2s;
      position: relative;
    }
    .mega-item-btn:hover {
      background: rgba(255,255,255,0.05);
    }
    [data-theme="light"] .mega-item-btn:hover {
      background: rgba(0,0,0,0.05);
    }
    .mega-item-btn.active {
      color: var(--primary);
      background: rgba(230, 51, 51, 0.05);
      font-weight: 600;
    }
    .mega-item-btn.active::before {
      content: '';
      position: absolute;
      left: 0;
      top: 10px;
      bottom: 10px;
      width: 3px;
      background: var(--primary);
      border-radius: 0 4px 4px 0;
    }
    .mega-detail-card {
      background: var(--bg-card);
      border-radius: 12px;
      border: 1px solid var(--border);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    [data-theme="light"] .mega-detail-card {
      box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    .mega-detail-img {
      height: 180px;
      background-size: cover;
      background-position: center;
    }
    .mega-detail-content {
      padding: 20px;
    }
    .mega-detail-title {
      font-size: 18px;
      font-weight: 800;
      color: var(--text-white);
      margin-bottom: 8px;
    }
    .mega-detail-desc {
      font-size: 13px;
      color: var(--text);
      margin-bottom: 16px;
      line-height: 1.5;
    }
    .mega-info-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-bottom: 16px;
    }
    .mega-info-box {
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 10px 12px;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .mega-info-box svg {
      width: 16px;
      height: 16px;
      stroke: var(--primary);
    }
    .mega-info-text {
      display: flex;
      flex-direction: column;
    }
    .mega-info-label {
      font-size: 10px;
      color: var(--text-muted);
      text-transform: uppercase;
    }
    .mega-info-val {
      font-size: 12px;
      font-weight: 600;
      color: var(--text-white);
    }
    .mega-price-box {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 14px;
      background: rgba(230,51,51,0.05);
      border-radius: 8px;
      margin-bottom: 16px;
    }
    .mega-price-label {
      font-size: 13px;
      color: var(--text);
    }
    .mega-price-val {
      font-size: 20px;
      font-weight: 800;
      color: var(--primary);
    }
    .mega-actions {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
'''

html_inject = '''
  <!-- MEGA CATALOG MODAL -->
  <div class="modal-overlay" id="mega-modal-overlay" onclick="handleOutsideMegaClick(event)">
    <div class="mega-catalog-modal" id="mega-catalog-modal" onclick="event.stopPropagation()">
      <div class="mega-catalog-header">
        <div class="mega-catalog-title">Каталог услуг</div>
        <button class="mega-catalog-close" onclick="closeMegaModal()">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>
      <div class="mega-catalog-body">
        <!-- Col 1: Categories -->
        <div class="mega-col" id="mega-col-1"></div>
        <!-- Col 2: Services -->
        <div class="mega-col" id="mega-col-2"></div>
        <!-- Col 3: Detail -->
        <div class="mega-col" id="mega-col-3" style="display:flex; align-items:center; justify-content:center;">
          <!-- Detail content goes here -->
        </div>
      </div>
    </div>
  </div>
'''

js_inject = '''
    // MEGA MODAL LOGIC
    let megaActiveCat = null;
    let megaActiveItem = null;

    window.openMegaModal = function() {
      document.getElementById('mega-modal-overlay').classList.add('active');
      megaActiveCat = servicesData[0];
      megaActiveItem = megaActiveCat.items[0];
      renderMegaCols();
    };
    
    window.closeMegaModal = function() {
      document.getElementById('mega-modal-overlay').classList.remove('active');
    };
    
    window.handleOutsideMegaClick = function(e) {
      if (e.target.id === 'mega-modal-overlay') closeMegaModal();
    };

    function renderMegaCols() {
      const col1 = document.getElementById('mega-col-1');
      const col2 = document.getElementById('mega-col-2');
      const col3 = document.getElementById('mega-col-3');
      
      if (!megaActiveCat) return;

      // Col 1
      col1.innerHTML = '';
      servicesData.forEach(cat => {
        const btn = document.createElement('button');
        btn.className = 'mega-cat-btn' + (megaActiveCat.id === cat.id ? ' active' : '');
        btn.innerHTML = `
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            ${getIconPath(cat.iconName)}
          </svg>
          ${currentLang==='RU' ? cat.title : (currentLang==='KZ' ? cat.titleKz : cat.titleEn)}
        `;
        btn.onclick = () => {
          megaActiveCat = cat;
          megaActiveItem = cat.items[0];
          renderMegaCols();
        };
        col1.appendChild(btn);
      });

      // Col 2
      col2.innerHTML = `
        <div style="font-size: 12px; font-weight: 700; color: var(--primary); text-transform: uppercase; margin-bottom: 12px; padding: 0 8px;">
          ⚡ Все услуги: ${currentLang==='RU' ? megaActiveCat.title : (currentLang==='KZ' ? megaActiveCat.titleKz : megaActiveCat.titleEn)}
        </div>
      `;
      megaActiveCat.items.forEach(item => {
        const name = currentLang==='RU' ? item.name : (currentLang==='KZ' ? item.nameKz : item.name);
        const btn = document.createElement('button');
        btn.className = 'mega-item-btn' + (megaActiveItem && megaActiveItem.name === item.name ? ' active' : '');
        btn.innerHTML = `
          <span>${name}</span>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>
        `;
        btn.onclick = () => {
          megaActiveItem = item;
          renderMegaCols();
        };
        col2.appendChild(btn);
      });

      // Col 3
      if (megaActiveItem) {
        const name = currentLang==='RU' ? megaActiveItem.name : (currentLang==='KZ' ? megaActiveItem.nameKz : megaActiveItem.name);
        
        // select random image based on string length to be deterministic
        const imgs = [
            "https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=600&q=80",
            "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=600&q=80",
            "https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=600&q=80",
            "https://images.unsplash.com/photo-1621905252507-b35492cc74b4?w=600&q=80",
            "https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=600&q=80"
        ];
        const img = imgs[megaActiveItem.name.length % imgs.length];

        col3.style.display = 'block';
        col3.innerHTML = `
          <div class="mega-detail-card">
            <div class="mega-detail-img" style="background-image: url('${img}')"></div>
            <div class="mega-detail-content">
              <div class="mega-detail-title">${name}</div>
              <div class="mega-detail-desc">Профессиональная услуга от сертифицированных мастеров. Быстро, качественно и с гарантией.</div>
              
              <div class="mega-info-grid">
                <div class="mega-info-box">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                  <div class="mega-info-text">
                    <span class="mega-info-label">Время работы</span>
                    <span class="mega-info-val">1-3 дня</span>
                  </div>
                </div>
                <div class="mega-info-box">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                  <div class="mega-info-text">
                    <span class="mega-info-label">Гарантия</span>
                    <span class="mega-info-val">12 мес</span>
                  </div>
                </div>
              </div>

              <div class="mega-price-box">
                <span class="mega-price-label">Стоимость работы</span>
                <span class="mega-price-val">${megaActiveItem.price}</span>
              </div>

              <div class="mega-actions">
                <button class="review-submit-btn" style="padding: 14px; cursor: pointer;" onclick="closeMegaModal(); switchCategory('${megaActiveCat.id}'); setTimeout(() => { document.getElementById('catalog').scrollIntoView({behavior:'smooth', block:'start'}); }, 100);">
                  Заказать
                </button>
                <a href="https://wa.me/77058462749?text=${encodeURIComponent('Здравствуйте! Хочу заказать услугу: ' + megaActiveItem.name)}" target="_blank" class="review-submit-btn" style="padding: 14px; background: #25D366; color: #fff; border: none; text-align: center; text-decoration: none; display: block;">
                  Заказать по WhatsApp
                </a>
              </div>
            </div>
          </div>
        `;
      }
    }

    // helper for mega modal icons
    function getIconPath(name) {
      if(name==='hammer') return '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>';
      if(name==='wrench') return '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>';
      if(name==='laptop') return '<rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/>';
      if(name==='droplet') return '<path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/>';
      if(name==='bolt') return '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>';
      if(name==='sparkles') return '<path d="M12 3l2 5h5l-4 3 1.5 5-4.5-3.5-4.5 3.5 1.5-5-4-3h5l2-5z"/>';
      if(name==='car') return '<rect x="3" y="10" width="18" height="10" rx="2"/><path d="M5 10l2-6h10l2 6"/>';
      if(name==='users') return '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>';
      if(name==='truck') return '<rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/>';
      return '<circle cx="12" cy="12" r="10"/>';
    }
'''

# 1. Insert CSS
if '/* Mega Catalog Modal */' not in html:
    idx = html.find('/* Dropdowns */')
    html = html[:idx] + css_inject + '\n' + html[idx:]

# 2. Insert HTML
if 'MEGA CATALOG MODAL' not in html:
    idx = html.find('<div class="modal-overlay" id="cabinet-modal-overlay"')
    html = html[:idx] + html_inject + '\n' + html[idx:]

# 3. Insert JS
if 'MEGA MODAL LOGIC' not in html:
    idx = html.find('// ── Modal open / close')
    html = html[:idx] + js_inject + '\n' + html[idx:]

# 4. Modify Catalog Header Button
# We need to change the header Catalog button to openMegaModal() instead of the dropdown
if 'id="cat-dropdown"' in html:
    # Replace the dropdown block
    old_block = re.search(r'<div class="dropdown" style="margin-left: 12px;">\s*<button class="nav-menu-btn" onclick="toggleDropdown\(event, \'cat-dropdown\'\)">[\s\S]*?</div>\s*</div>', html)
    if old_block:
        new_btn = '''
        <button class="nav-menu-btn" style="margin-left: 12px;" onclick="openMegaModal()">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
          <span data-i18n="catalogTitle">Каталог</span>
        </button>
        '''
        html = html[:old_block.start()] + new_btn + html[old_block.end():]

with open('hubmaster.html', 'w', encoding='utf-8') as f:
    f.write(html)
