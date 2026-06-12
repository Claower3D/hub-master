import os
import re

files_to_update = [
    'public/index.html',
    'public/template1.html',
    'public/template2.html',
    'public/hubmaster.html',
    'hub-master/hubmaster.html'
]

replacement_css = """        <style>
          .hero-bottom-grid {
            grid-column: span 2;
            display: grid;
            grid-template-columns: 1.3fr 0.7fr;
            gap: 32px;
            margin-top: 16px;
            background: rgba(20, 20, 24, 0.55);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 24px 32px;
            align-items: start;
          }
          @media (max-width: 992px) {
            .hero-bottom-grid {
              grid-template-columns: 1fr;
              padding: 24px 20px;
            }
          }
          
          /* Light Theme Adaptations */
          [data-theme="light"] .hero-bottom-grid {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
          }
          [data-theme="light"] .partners-dev-card,
          [data-theme="light"] .partners-tag {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            color: #1a202c;
          }
          [data-theme="light"] .partners-main-title,
          [data-theme="light"] .partners-dev-title,
          [data-theme="light"] .why-us-title,
          [data-theme="light"] .why-us-list li span.chk-text {
            color: #1a202c;
          }
          [data-theme="light"] .partners-label,
          [data-theme="light"] .partners-dev-text,
          [data-theme="light"] .why-us-list li span.chk-subtext {
            color: #64748b;
          }

          .partners-block {
            display: flex;
            flex-direction: column;
          }
          .partners-main-title {
            font-size: 24px;
            font-weight: 700;
            color: var(--text-white);
            margin-bottom: 24px;
            font-family: var(--font-heading);
          }
          .partners-category {
            margin-bottom: 30px;
          }
          .partners-category:last-child {
            margin-bottom: 0;
          }
          .partners-label {
            display: block;
            font-size: 12px;
            color: var(--text-muted);
            text-transform: uppercase;
            margin-bottom: 12px;
            letter-spacing: 0.5px;
          }
          .partners-dev-card {
            background: rgba(20, 20, 24, 0.55);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 20px;
            max-width: 100%;
          }
          .partners-dev-title {
            font-size: 18px;
            font-weight: 600;
            color: var(--text-white);
            margin-bottom: 8px;
          }
          .partners-dev-text {
            font-size: 14px;
            color: var(--text-muted);
            line-height: 1.5;
          }
          .partners-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
          }
          .partners-tag {
            background: rgba(20, 20, 24, 0.55);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 12px 20px;
            font-size: 14px;
            font-weight: 600;
            color: var(--text-white);
            display: flex;
            align-items: center;
            justify-content: center;
          }
          
          .why-us-block {
            display: flex;
            flex-direction: column;
          }
          .why-us-title {
            font-size: 24px;
            font-weight: 700;
            color: var(--text-white);
            margin-bottom: 24px;
            font-family: var(--font-heading);
          }
          .why-us-list {
            list-style: none;
            padding: 0;
            margin: 0;
            display: flex;
            flex-direction: column;
            gap: 16px;
          }
          .why-us-list li {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            font-size: 15px;
            color: var(--text-white);
          }
          .why-us-list li span.chk-icon {
            color: var(--primary);
            font-weight: bold;
            font-size: 16px;
            flex-shrink: 0;
          }
          .why-us-list li span.chk-subtext {
            color: var(--text-muted);
            font-size: 14px;
          }
        </style>
        
        <div class="hero-bottom-grid">
          <div class="partners-block">
          <h2 class="partners-main-title">Нам доверяют</h2>
          
          <div class="partners-category">
            <span class="partners-label">ЗАСТРОЙЩИК</span>
            <div class="partners-dev-card">
              <div class="partners-dev-title">Everest Development</div>
              <div class="partners-dev-text">Выполняем работы на объектах застройщика: остекление и москитные сетки, электромонтажные работы, сварка и металлоконструкции.</div>
            </div>
          </div>
          
          <div class="partners-category">
            <span class="partners-label">ПРОФИЛЬ ДЛЯ ОКОН И СЕТОК</span>
            <div class="partners-tags">
              <div class="partners-tag">WUKO</div>
              <div class="partners-tag">KAVI</div>
              <div class="partners-tag">VEKA</div>
              <div class="partners-tag">REHAU</div>
              <div class="partners-tag">Euro Super Plast</div>
            </div>
          </div>
          
          <div class="partners-category">
            <span class="partners-label">МАТЕРИАЛЫ И ФУРНИТУРА ДЛЯ МЕБЕЛИ</span>
            <div class="partners-tags">
              <div class="partners-tag">Blum</div>
              <div class="partners-tag">Hettich</div>
              <div class="partners-tag">Häfele</div>
              <div class="partners-tag">Egger</div>
              <div class="partners-tag">Kronospan</div>
            </div>
          </div>
        </div>

        <div class="why-us-block">
          <h2 class="why-us-title">Почему мы</h2>
          <ul class="why-us-list">
            <li><span class="chk-icon">✓</span><span class="chk-text">Гарантия от 12 месяцев на работы</span></li>
            <li><span class="chk-icon">✓</span><span class="chk-text">Сертифицированные мастера</span></li>
            <li><span class="chk-icon">✓</span><span class="chk-text">Бесплатный замер и выезд <span class="chk-subtext">— по окнам и сеткам</span></span></li>
            <li><span class="chk-icon">✓</span><span class="chk-text">Договор на все работы</span></li>
            <li><span class="chk-icon">✓</span><span class="chk-text">Выезд в день обращения</span></li>
            <li><span class="chk-icon">✓</span><span class="chk-text">Работаем по всему Казахстану <span class="chk-subtext">— окна и сетки</span></span></li>
            <li><span class="chk-icon">✓</span><span class="chk-text">Гарантия лучшей цены</span></li>
          </ul>
        </div>
      </div>"""

for filepath in files_to_update:
    if not os.path.exists(filepath):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # If the file already has the <style>...hero-bottom-grid...</div></div></div></div>... it means it was updated.
    # Otherwise, it might have <div class="hero-bottom-form-card">...</div>
    
    # We'll use regex to find either the old hero-bottom-form-card OR the new hero-bottom-grid block
    # and replace it.
    
    # Match from <div class="hero-bottom-form-card"> to the corresponding </div> 
    # Or match from <style> to the end of <div class="hero-bottom-grid">...</div>
    # Actually, a simpler way is to find a unique comment or structure.
    
    # Let's replace by string replacement for the parts we know.
    # We know public/index.html was already updated, so we need to replace the <style>...hero-bottom-grid...</div></div></div></div>...
    
    pattern1 = re.compile(r'<style>\s*\.hero-bottom-grid \{.*?</style>\s*<div class="hero-bottom-grid">.*?</div>\s*</div>\s*</div>\s*</div>', re.DOTALL)
    
    pattern2 = re.compile(r'<div class="hero-bottom-form-card">.*?</ul>\s*</div>\s*</div>', re.DOTALL)
    
    # Also I made a mistake in previous replacement in hub-master.html where I replaced with .partners-block instead of hero-bottom-grid.
    pattern3 = re.compile(r'<style>\s*\.partners-block \{.*?</style>\s*<div class="partners-block">.*?</div>\s*</div>\s*</div>\s*</div>', re.DOTALL)
    
    new_content = content
    if pattern1.search(new_content):
        new_content = pattern1.sub(replacement_css, new_content)
    elif pattern3.search(new_content):
        new_content = pattern3.sub(replacement_css, new_content)
    elif pattern2.search(new_content):
        new_content = pattern2.sub(replacement_css, new_content)
    else:
        print(f"Could not find matching block in {filepath}")
        continue
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Updated {filepath}")
