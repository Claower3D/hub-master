import os

filepath = "hubmaster.html"
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Verify that the slice starts with `<div class="hero-bottom-form-card">` and ends with `</div>` of form-card-left
start_line = 5350 # 0-indexed index 5349
end_line = 5408   # 0-indexed index 5407

print("Start line is:", repr(lines[5350]))
print("End line is:", repr(lines[5407]))

new_content = """        <div class="hero-bottom-form-card">
          <div class="form-card-left" style="display: flex; flex-direction: column; justify-content: center; gap: 12px;">
            <h3 class="form-card-title" data-i18n="heroFormTitle">Быстрый заказ услуг</h3>
            <p style="font-size: 14px; color: var(--text); line-height: 1.6; margin: 0 0 8px 0;" data-i18n="heroFormDesc">
              Оставьте заявку на ремонт или сборку мебели, и наши специалисты свяжутся с вами в течение 10 минут, либо напишите нам в WhatsApp.
            </p>
            <div style="display: flex; gap: 14px; flex-wrap: wrap;">
              <button onclick="document.getElementById('lead-form-container').scrollIntoView({ behavior: 'smooth' })" class="form-submit-red-btn" style="display: inline-flex; align-items: center; justify-content: center; height: 46px; font-size: 14px; border-radius: 8px; padding: 0 24px; cursor: pointer;" data-i18n="btnLeaveAnketa">
                Оставить анкету
              </button>
              <a href="https://wa.me/77058462749" target="_blank" rel="noopener noreferrer" class="form-whatsapp-green-btn" style="display: inline-flex; align-items: center; justify-content: center; height: 46px; font-size: 14px; text-decoration: none; border-radius: 8px; padding: 0 24px;">
                <svg viewBox="0 0 24 24" width="18" height="18">
                  <path fill="currentColor"
                    d="M12.012 2c-5.506 0-9.989 4.478-9.99 9.984a9.96 9.96 0 001.37 5.016L2 22l5.13-1.346a9.92 9.92 0 004.882 1.28h.005c5.507 0 9.99-4.478 9.99-9.986 0-2.67-1.037-5.178-2.923-7.065A9.925 9.925 0 0012.012 2zm5.72 14.103c-.235.662-1.362 1.224-1.879 1.285-.466.056-.918.23-2.986-.583-2.645-1.04-4.327-3.738-4.46-3.914-.131-.176-1.077-1.433-1.077-2.731a2.8 2.8 0 01.854-2.074c.264-.265.578-.332.772-.332.193 0 .386.002.553.01.173.008.406-.065.636.488.235.568.805 1.961.875 2.1.07.142.118.307.022.493-.095.187-.142.307-.283.473-.142.167-.29.351-.414.47-.142.138-.29.288-.125.572.167.283.74 1.22 1.585 1.97.1.09.286.257.48.337.195.08.388.082.533-.082.146-.166.627-.728.794-.977.167-.249.333-.207.562-.123.23.084 1.455.686 1.705.811.25.124.417.187.478.293.063.107.063.621-.172 1.283z" />
                </svg>
                WhatsApp
              </a>
            </div>
          </div>
"""

# Replace lines from index 5350 to 5408
lines[5350:5408] = [new_content]

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("SUCCESS")
