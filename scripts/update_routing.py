import os

def update_routing(filepath):
    print(f"Updating routing in {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update categoriesToRender mapping to store cat.tabId in renderCatalogItems
    old_mapping_block = """      let categoriesToRender = [];
      if (selectedCategory === 'all') {
        servicesData.forEach(svc => {
          if (svc.categories && svc.categories.length > 0) {
            svc.categories.forEach(cat => {
              if (!categoriesToRender.some(c => c.id === cat.id)) {
                categoriesToRender.push(cat);
              }
            });
          } else {
            categoriesToRender.push(svc);
          }
        });
      } else {
        let found = false;
        servicesData.forEach(svc => {
          if (svc.categories && svc.categories.length > 0) {
            const cat = svc.categories.find(c => c.id === selectedCategory);
            if (cat) {
              categoriesToRender.push(cat);
              found = true;
            }
          }
        });
        if (!found) {
          const cat = servicesData.find(svc => svc.id === selectedCategory);
          if (cat) {
            categoriesToRender.push(cat);
          }
        }
      }"""

    new_mapping_block = """      let categoriesToRender = [];
      if (selectedCategory === 'all') {
        servicesData.forEach(svc => {
          if (svc.categories && svc.categories.length > 0) {
            svc.categories.forEach(cat => {
              if (!categoriesToRender.some(c => c.id === cat.id)) {
                cat.tabId = svc.id;
                categoriesToRender.push(cat);
              }
            });
          } else {
            svc.tabId = svc.id;
            categoriesToRender.push(svc);
          }
        });
      } else {
        let found = false;
        servicesData.forEach(svc => {
          if (svc.categories && svc.categories.length > 0) {
            const cat = svc.categories.find(c => c.id === selectedCategory);
            if (cat) {
              cat.tabId = svc.id;
              categoriesToRender.push(cat);
              found = true;
            }
          }
        });
        if (!found) {
          const cat = servicesData.find(svc => svc.id === selectedCategory);
          if (cat) {
            cat.tabId = cat.id;
            categoriesToRender.push(cat);
          }
        }
      }"""

    if old_mapping_block in content:
        content = content.replace(old_mapping_block, new_mapping_block)
    else:
        print("Warning: old_mapping_block not found precisely.")

    # 2. Update navigateThematic clickAction in renderCatalogItems
    old_click_action = """          const clickAction = (item.catId && item.id)
            ? `navigateThematic('${cat.id}', '${item.catId}', '${item.id}')`
            : `openModal('${item.name}')`;"""
            
    new_click_action = """          const clickAction = (item.catId && item.id)
            ? `navigateThematic('${cat.tabId || cat.id}', '${cat.id}', '${item.id}')`
            : `openModal('${item.name}')`;"""

    if old_click_action in content:
        content = content.replace(old_click_action, new_click_action)
    else:
        print("Warning: old_click_action not found precisely.")

    # 3. Replace getThematicImage, renderThematicPage, initRouter block
    start_str = "    function getThematicImage(catId, subcatId, itemId) {"
    end_str = """    function initRouter() {
      const path = window.location.pathname;
      if (path === '/' || path === '/index.html' || path === '/admin.html') {
        renderThematicPage(null);
        return;
      }

      const parts = path.split('/').filter(Boolean);
      if (parts.length > 0) {
        const catId = parts[0];
        const subcatId = parts.length > 1 ? parts[1] : null;
        const itemId = parts.length > 2 ? parts[2] : null;

        const categoryExists = servicesData.some(s => s.id === catId);
        if (categoryExists) {
          renderThematicPage(catId, subcatId, itemId);
        } else {
          renderThematicPage(null);
        }
      }
    }"""

    if start_str not in content or end_str not in content:
        print("Error: Routing functions block not found!")
        return

    # Find boundaries
    start_idx = content.find(start_str)
    end_idx = content.find(end_str) + len(end_str)

    new_routing_block = """    function resolveCatalogRoute(parts) {
      if (!parts || parts.length === 0) return null;
      
      let resolvedTab = null;
      let resolvedCat = null;
      let resolvedItem = null;

      // 1. Search for item first (e.g. "sub-okna-1-1") in all parts
      for (const part of parts) {
        for (const tab of servicesData) {
          if (tab.items) {
            const foundItem = tab.items.find(i => i.id === part);
            if (foundItem) {
              resolvedItem = foundItem;
              resolvedCat = (tab.categories || []).find(c => c.id === foundItem.catId);
              resolvedTab = tab;
              break;
            }
          }
        }
        if (resolvedItem) break;
      }

      // 2. Search for category (e.g. "cat-okna-1")
      if (!resolvedItem) {
        for (const part of parts) {
          for (const tab of servicesData) {
            if (tab.categories) {
              const foundCat = tab.categories.find(c => c.id === part);
              if (foundCat) {
                resolvedCat = foundCat;
                resolvedTab = tab;
                break;
              }
            }
            if (tab.id === part && (!tab.categories || tab.categories.length === 0)) {
              resolvedCat = tab;
              resolvedTab = tab;
              break;
            }
          }
          if (resolvedCat) break;
        }
      }

      // 3. Search for tab (e.g. "okna")
      if (!resolvedCat && !resolvedItem) {
        for (const part of parts) {
          const foundTab = servicesData.find(t => t.id === part);
          if (foundTab) {
            resolvedTab = foundTab;
            break;
          }
        }
      }

      if (resolvedTab || resolvedCat || resolvedItem) {
        return {
          tabId: resolvedTab ? resolvedTab.id : (resolvedCat ? resolvedCat.tabId : null),
          catId: resolvedCat ? resolvedCat.id : null,
          itemId: resolvedItem ? resolvedItem.id : null
        };
      }
      return null;
    }

    function getThematicImage(catId, subcatId, itemId) {
      const images = {
        'sub-tech-1-1': 'https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?q=80&w=600&auto=format&fit=crop',
        'sub-tech-1-2': 'https://images.unsplash.com/photo-1584622650111-993a426fbf0a?q=80&w=600&auto=format&fit=crop',
        'sub-tech-1-3': 'https://images.unsplash.com/photo-1585338107529-13afc5f02586?q=80&w=600&auto=format&fit=crop',
        'cat-tech-1': 'https://images.unsplash.com/photo-1581092921461-eab62e97a780?q=80&w=600&auto=format&fit=crop',
        'cat-tech-2': 'https://images.unsplash.com/photo-1574269909862-7e1d70bb8078?q=80&w=600&auto=format&fit=crop',
        'cat-tech-3': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?q=80&w=600&auto=format&fit=crop',
        'cat-tech-4': 'https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?q=80&w=600&auto=format&fit=crop',
        'tech': 'https://images.unsplash.com/photo-1581092921461-eab62e97a780?q=80&w=600&auto=format&fit=crop',
        'cat-auto-1': 'https://images.unsplash.com/photo-1486006920555-c77dce18193b?q=80&w=600&auto=format&fit=crop',
        'cat-auto-2': 'https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?q=80&w=600&auto=format&fit=crop',
        'auto': 'https://images.unsplash.com/photo-1486006920555-c77dce18193b?q=80&w=600&auto=format&fit=crop',
        'cat-house-1': 'https://images.unsplash.com/photo-1581578731548-c64695cc6952?q=80&w=600&auto=format&fit=crop',
        'cat-house-2': 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?q=80&w=600&auto=format&fit=crop',
        'cat-house-3': 'https://images.unsplash.com/photo-1528224202796-f3e49e29a997?q=80&w=600&auto=format&fit=crop',
        'cat-house-4': 'https://images.unsplash.com/photo-1504307651254-35680f356dfd?q=80&w=600&auto=format&fit=crop',
        'household': 'https://images.unsplash.com/photo-1581578731548-c64695cc6952?q=80&w=600&auto=format&fit=crop',
        'cat-spec-1': 'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?q=80&w=600&auto=format&fit=crop',
        'cat-spec-2': 'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?q=80&w=600&auto=format&fit=crop',
        'specialists': 'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?q=80&w=600&auto=format&fit=crop',
        'cat-const-1': 'https://images.unsplash.com/photo-1503387762-592deb58ef4e?q=80&w=600&auto=format&fit=crop',
        'cat-const-2': 'https://images.unsplash.com/photo-1621905251189-08b45d6a269e?q=80&w=600&auto=format&fit=crop',
        'cat-const-3': 'https://images.unsplash.com/photo-1540518614846-7eded433c457?q=80&w=600&auto=format&fit=crop',
        'construction': 'https://images.unsplash.com/photo-1503387762-592deb58ef4e?q=80&w=600&auto=format&fit=crop',
        'cat-furn-1': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?q=80&w=600&auto=format&fit=crop',
        'cat-furn-2': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?q=80&w=600&auto=format&fit=crop',
        'furniture': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?q=80&w=600&auto=format&fit=crop',
        'cat-other-1': 'https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?q=80&w=600&auto=format&fit=crop',
        'cat-other-2': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=600&auto=format&fit=crop',
        'cat-other-3': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=600&auto=format&fit=crop',
        'other': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=600&auto=format&fit=crop'
      };

      if (itemId && images[itemId]) return images[itemId];
      if (subcatId && images[subcatId]) return images[subcatId];
      if (catId && images[catId]) return images[catId];

      let searchTitle = '';
      let cat = servicesData.find(c => c.id === catId);
      if (!cat) {
        for (const tab of servicesData) {
          if (tab.categories) {
            const found = tab.categories.find(c => c.id === catId);
            if (found) {
              cat = found;
              break;
            }
          }
        }
      }

      if (cat) {
        searchTitle = cat.title;
        if (itemId && cat.items) {
          const item = cat.items.find(i => i.id === itemId);
          if (item) searchTitle = item.name;
        } else if (subcatId && cat.items) {
          const subItem = cat.items.find(i => i.catId === subcatId);
          if (subItem) searchTitle = subItem.catTitle || subItem.name;
        }
      }

      const t = (searchTitle || '').toLowerCase();
      if (t.includes('крупн') || t.includes('стирал') || t.includes('холод')) {
        return 'https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?w=800&q=80';
      }
      if (t.includes('мелк') || t.includes('пылесос') || t.includes('микроволн') || t.includes('кофема')) {
        return 'https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=800&q=80';
      }
      if (t.includes('цифр') || t.includes('телевиз') || t.includes('телефо') || t.includes('планшет')) {
        return 'https://images.unsplash.com/photo-1461151304267-38535e780c79?w=800&q=80';
      }
      if (t.includes('компь') || t.includes('ноутбук') || t.includes('macbook')) {
        return 'https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=800&q=80';
      }
      if (t.includes('авто') || t.includes('сто') || t.includes('эвакуа')) {
        return 'https://images.unsplash.com/photo-1617788138017-80ad40651399?w=800&q=80';
      }
      if (t.includes('клини') || t.includes('уборк')) {
        return 'https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=800&q=80';
      }
      if (t.includes('санитар') || t.includes('дезинф') || t.includes('тарака') || t.includes('клоп')) {
        return 'https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800&q=80';
      }
      if (t.includes('химчист') || t.includes('стирк') || t.includes('ковр')) {
        return 'https://images.unsplash.com/photo-1545189656-786ac2d77ef7?w=800&q=80';
      }
      if (t.includes('сантех') || t.includes('электри') || t.includes('проводк')) {
        return 'https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?w=800&q=80';
      }
      if (t.includes('юрист') || t.includes('адвокат') || t.includes('закон')) {
        return 'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=800&q=80';
      }
      if (t.includes('жиһаз') || t.includes('мебе')) {
        return 'https://images.unsplash.com/photo-1592078615290-033ee584e267?w=800&q=80';
      }
      if (t.includes('окн') || t.includes('витраж')) {
        return 'https://images.unsplash.com/photo-1509644851169-2aba0855683d?w=800&q=80';
      }
      if (t.includes('здоров') || t.includes('врач') || t.includes('фитнес')) {
        return 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=800&q=80';
      }
      if (t.includes('ремонт кварт') || t.includes('строител')) {
        return 'https://images.unsplash.com/photo-1581094794329-c8112a89af12?w=800&q=80';
      }
      if (t.includes('монтаж') || t.includes('установк')) {
        return 'https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800&q=80';
      }
      return 'https://images.unsplash.com/photo-1581092921461-eab62e97a780?q=80&w=600&auto=format&fit=crop';
    }

    function renderThematicPage(catId, subcatId = null, itemId = null) {
      const landing = document.getElementById('landing-page-content');
      const thematic = document.getElementById('thematic-page-content');

      if (!catId) {
        landing.style.display = 'block';
        thematic.style.display = 'none';
        thematic.innerHTML = '';
        return;
      }

      let resolved = resolveCatalogRoute([catId, subcatId, itemId].filter(Boolean));
      if (!resolved) {
        let fallbackCat = servicesData.find(c => c.id === catId);
        if (!fallbackCat) {
          for (const tab of servicesData) {
            if (tab.categories) {
              const found = tab.categories.find(c => c.id === catId);
              if (found) {
                fallbackCat = found;
                break;
              }
            }
          }
        }
        if (!fallbackCat) {
          landing.style.display = 'block';
          thematic.style.display = 'none';
          return;
        }
        resolved = {
          tabId: catId,
          catId: fallbackCat.id,
          itemId: itemId
        };
      }

      const tab = servicesData.find(t => t.id === resolved.tabId);
      let cat = null;
      if (resolved.catId) {
        cat = tab ? (tab.categories || []).find(c => c.id === resolved.catId) : null;
        if (!cat) {
          cat = servicesData.find(c => c.id === resolved.catId);
        }
      }
      if (!cat) {
        cat = tab || servicesData.find(c => c.id === resolved.tabId);
      }

      if (!cat) {
        landing.style.display = 'block';
        thematic.style.display = 'none';
        return;
      }

      landing.style.display = 'none';
      thematic.style.display = 'block';

      let breadcrumbsHTML = `
        <div class="breadcrumbs">
          <a href="#" onclick="navigateThematic(''); return false;">Главная</a>
          <span class="separator">/</span>
          <a href="#" onclick="navigateThematic('${resolved.tabId}'); return false;">${currentLang === 'RU' ? (tab ? tab.title : cat.title) : (currentLang === 'KZ' ? (tab ? tab.titleKz || tab.title : cat.titleKz || cat.title) : (tab ? tab.titleEn || tab.title : cat.titleEn || cat.title))}</a>
      `;

      let title = currentLang === 'RU' ? cat.title : (currentLang === 'KZ' ? cat.titleKz || cat.title : cat.titleEn || cat.title);
      let subtitle = currentLang === 'RU' ? `Профессиональный сервис услуг и товаров в категории "${cat.title}" в Алматы и Астане.` : `Сапалы қызмет көрсету "${cat.titleKz || cat.title}" санаты бойынша.`;
      let itemsList = [];

      if (resolved.itemId) {
        const item = cat.items.find(i => i.id === resolved.itemId);
        if (item) {
          breadcrumbsHTML += `
            <span class="separator">/</span>
            <a href="#" onclick="navigateThematic('${resolved.tabId}', '${cat.id}'); return false;">${currentLang === 'RU' ? item.catTitle : (currentLang === 'KZ' ? item.catTitleKz || item.catTitle : item.catTitleEn || item.catTitle)}</a>
            <span class="separator">/</span>
            <span>${currentLang === 'RU' ? item.name : item.nameKz || item.name}</span>
          `;
          title = currentLang === 'RU' ? item.name : item.nameKz || item.name;
          subtitle = item.desc || '';
          itemsList = [item];
        }
      } else if (resolved.catId && resolved.catId !== resolved.tabId) {
        breadcrumbsHTML += `
          <span class="separator">/</span>
          <span>${title}</span>
        `;
        subtitle = currentLang === 'RU' ? `Полный спектр услуг по направлению "${title}". Выгодные цены и официальная гарантия.` : `"${title}" бағыты бойынша барлық қызметтер тізімі.`;
        itemsList = cat.items || [];
      } else {
        itemsList = cat.items || [];
      }

      breadcrumbsHTML += `</div>`;

      let servicesHTML = '';
      if (!resolved.itemId && (!resolved.catId || resolved.catId === resolved.tabId)) {
        servicesHTML += `<div class="thematic-categories-grid">`;
        if (cat.categories && cat.categories.length > 0) {
          cat.categories.forEach(category => {
            const subItems = category.items || [];
            const blockIcon = category.icon || 'ri-tools-line';
            servicesHTML += `
              <div class="category-block-card animate-fade-in">
                <div class="category-block-header">
                  <div class="category-block-icon">
                    <i class="${blockIcon}"></i>
                  </div>
                  <h3 class="category-block-title">${currentLang === 'RU' ? category.title : (currentLang === 'KZ' ? category.titleKz || category.title : category.titleEn || category.title)}</h3>
                </div>
                <ul class="category-sublist">
            `;
            subItems.forEach(sub => {
              servicesHTML += `
                <li>
                  <a href="#" onclick="navigateThematic('${resolved.tabId}', '${category.id}', '${sub.id}'); return false;">
                    <i class="ri-arrow-right-s-line"></i>
                    <span>${currentLang === 'RU' ? sub.name : sub.nameKz || sub.name}</span>
                  </a>
                </li>
              `;
            });
            if (subItems.length === 0) {
              servicesHTML += `<li class="no-items-placeholder">Услуги скоро появятся</li>`;
            }
            servicesHTML += `
                </ul>
              </div>
            `;
          });
        } else {
          const grouped = {};
          (itemsList || []).forEach(item => {
            if (!grouped[item.catId]) {
              grouped[item.catId] = {
                title: currentLang === 'RU' ? item.catTitle : (currentLang === 'KZ' ? item.catTitleKz || item.catTitle : item.catTitleEn || item.catTitle),
                items: []
              };
            }
            grouped[item.catId].items.push(item);
          });
          for (const subId in grouped) {
            servicesHTML += `
              <div class="category-block-card animate-fade-in">
                <div class="category-block-header">
                  <div class="category-block-icon">
                    <i class="ri-tools-line"></i>
                  </div>
                  <h3 class="category-block-title">${grouped[subId].title}</h3>
                </div>
                <ul class="category-sublist">
            `;
            grouped[subId].items.forEach(item => {
              servicesHTML += `
                <li>
                  <a href="#" onclick="navigateThematic('${resolved.tabId}', '${item.catId}', '${item.id}'); return false;">
                    <i class="ri-arrow-right-s-line"></i>
                    <span>${currentLang === 'RU' ? item.name : item.nameKz || item.name}</span>
                  </a>
                </li>
              `;
            });
            servicesHTML += `
                </ul>
              </div>
            `;
          }
        }
        servicesHTML += `</div>`;
      } else {
        servicesHTML += `<div class="services-list-grid">`;
        (itemsList || []).forEach(item => {
          servicesHTML += renderItemCardHTML(item, resolved.tabId);
        });
        servicesHTML += `</div>`;
      }

      let pricesTableHTML = '';
      if ((resolved.catId && resolved.catId !== resolved.tabId) || resolved.itemId) {
        const currentCategory = resolved.catId || (itemsList[0] && itemsList[0].catId);
        const pricingItems = (cat.items || []).filter(i => i.catId === currentCategory);
        if (pricingItems.length > 0) {
          pricesTableHTML = `
            <div class="prices-section animate-fade-in">
              <h2 class="prices-title">${currentLang === 'RU' ? 'Цены на популярные услуги' : 'Танымал қызметтердің бағалары'}</h2>
              <div class="prices-table-wrapper">
                <table class="prices-table">
                  <thead>
                    <tr>
                      <th>${currentLang === 'RU' ? 'Услуга' : 'Қызмет'}</th>
                      <th>${currentLang === 'RU' ? 'Стоимость (KZT)' : 'Құны (KZT)'}</th>
                      <th>${currentLang === 'RU' ? 'Срок выполнения' : 'Орындау мерзімі'}</th>
                    </tr>
                  </thead>
                  <tbody>
          `;
          pricingItems.forEach(item => {
            const name = currentLang === 'RU' ? item.name : item.nameKz || item.name;
            pricesTableHTML += `
              <tr>
                <td>${name}</td>
                <td class="price-cell">${item.price}</td>
                <td class="time-cell">${item.time}</td>
              </tr>
            `;
          });
          pricesTableHTML += `
                  </tbody>
                </table>
              </div>
              <p style="font-size: 12px; color: var(--text-muted); margin-top: 15px; font-style: italic;">
                * ${currentLang === 'RU' ? 'Точная стоимость определяется мастером после диагностики.' : 'Нақты құны диагностикадан кейін шебермен анықталады.'}
              </p>
            </div>
          `;
        }
      }

      const heroImageSrc = getThematicImage(resolved.tabId, resolved.catId, resolved.itemId);
      const isQuickRepairBadge = resolved.itemId && (resolved.itemId.includes('tech-1-2') || resolved.itemId.includes('fridge'));
      const badgeText = isQuickRepairBadge ? (currentLang === 'RU' ? 'Быстрый выезд мастера' : 'Шебердің жедел келуі') : 'Premium Service';

      let heroHTML = `
        <div class="thematic-hero animate-fade-in">
          <div class="thematic-hero-text">
            <div class="thematic-badge">
              <span class="badge-dot">●</span>
              <span>${badgeText}</span>
            </div>
            <h1 class="thematic-title">${title}</h1>
            <p class="thematic-subtitle">${subtitle}</p>
            
            <div class="thematic-hero-buttons">
              <button class="thematic-btn-primary" onclick="document.getElementById('them-name').focus(); return false;">
                ${currentLang === 'RU' ? 'Вызвать мастера' : 'Шеберді шақыру'}
              </button>
              <button class="thematic-btn-secondary" onclick="window.scrollTo({ top: document.querySelector('.section-headline').offsetTop - 100, behavior: 'smooth' }); return false;">
                ${currentLang === 'RU' ? 'Узнать цены' : 'Бағасын білу'}
              </button>
            </div>

            <div class="thematic-hero-badges">
              <div class="thematic-hero-badge-item">
                <i class="ri-checkbox-circle-fill"></i>
                <span>${currentLang === 'RU' ? 'Гарантия качества' : 'Сапа кепілдігі'}</span>
              </div>
              <div class="thematic-hero-badge-item">
                <i class="ri-time-fill"></i>
                <span>${currentLang === 'RU' ? 'Выезд за 45 мин' : '45 минутта келу'}</span>
              </div>
            </div>
          </div>
          <div class="thematic-hero-image-wrapper">
            <img class="thematic-hero-image" src="${heroImageSrc}" alt="${title}">
          </div>
        </div>
      `;

      thematic.innerHTML = `
        <div class="thematic-container">
          ${breadcrumbsHTML}
          ${heroHTML}
          
          <div class="thematic-grid">
            <div class="thematic-left-section">
              <div class="section-headline">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
                <span>${resolved.itemId ? (currentLang === 'RU' ? 'Детали услуги' : 'Қызмет мәліметтері') : (currentLang === 'RU' ? 'Наши услуги и цены' : 'Қызметтеріміз бен бағаларымыз')}</span>
              </div>
              ${servicesHTML}
              ${pricesTableHTML}
            </div>
            
            <div class="thematic-form-card">
              <div class="section-headline" style="font-size: 18px; margin-bottom: 12px;">
                <span>${currentLang === 'RU' ? 'Быстрый заказ' : 'Жедел тапсырыс'}</span>
              </div>
              <p style="font-size: 14px; color: var(--text); margin-bottom: 20px; line-height: 1.4;">
                ${currentLang === 'RU' ? 'Оставьте заявку, наш специалист свяжется с вами в течение 10 минут для консультации.' : 'Өтінім қалдырыңыз, біздің маман сізбен кеңесу үшін 10 минут ішінде хабарласады.'}
              </p>
              
              <form onsubmit="handleThematicSubmit(event, '${title}')">
                <div class="input-group-v2" style="margin-bottom: 15px;">
                  <label style="font-size: 12px; color: var(--text); display: block; margin-bottom: 6px; font-weight: 600;">${currentLang === 'RU' ? 'Ваше имя' : 'Сіздің есіміңіз'}</label>
                  <input type="text" required placeholder="${currentLang === 'RU' ? 'Введите имя' : 'Есіміңізді енгізіңіз'}" id="them-name" style="width: 100%; padding: 12px; background: rgba(255,255,255,0.03); border: 1px solid var(--border); border-radius: 8px; color: white;">
                </div>
                <div class="input-group-v2" style="margin-bottom: 15px;">
                  <label style="font-size: 12px; color: var(--text); display: block; margin-bottom: 6px; font-weight: 600;">${currentLang === 'RU' ? 'Номер телефона' : 'Телефон нөмірі'}</label>
                  <input type="tel" required placeholder="+7 (777) 777-77-77" id="them-phone" style="width: 100%; padding: 12px; background: rgba(255,255,255,0.03); border: 1px solid var(--border); border-radius: 8px; color: white;">
                </div>
                <button type="submit" class="cta-button-v2" style="width: 100%; padding: 14px; background: var(--primary); border: none; border-radius: 8px; color: white; font-weight: 700; cursor: pointer; transition: background 0.2s;">
                  ${currentLang === 'RU' ? 'Отправить заявку' : 'Өтінімді жіберу'}
                </button>
              </form>
              
              <div class="form-badge-grid">
                <div class="form-badge-item">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                  <span>${currentLang === 'RU' ? 'Выезд за 45 мин' : '45 минутта келу'}</span>
                </div>
                <div class="form-badge-item">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                  <span>${currentLang === 'RU' ? 'Гарантия до 3 лет' : '3 жылға дейін кепілдік'}</span>
                </div>
                <div class="form-badge-item">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
                  <span>${currentLang === 'RU' ? 'Любая оплата' : 'Кез келген төлем'}</span>
                </div>
                <div class="form-badge-item">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
                  <span>${currentLang === 'RU' ? 'Честная цена' : 'Әділ баға'}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      `;

      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function renderItemCardHTML(item, catId) {
      const name = currentLang === 'RU' ? item.name : item.nameKz || item.name;
      return `
        <div class="thematic-item-card">
          <div class="item-card-left">
            <div class="item-card-title">${name}</div>
            <div class="item-card-desc">${item.desc}</div>
            <div style="display: flex; gap: 15px; margin-top: 10px; font-size: 12px; color: var(--text-muted);">
              <span>⏱ ${item.time}</span>
              <span>🛡 ${item.warr}</span>
            </div>
          </div>
          <div class="item-card-right">
            <div class="item-card-price">${item.price}</div>
            <button class="item-card-action" onclick="openModal('${name}')">Заказать</button>
            <button class="item-card-action" style="background: transparent; border: 1px solid var(--border); margin-top: 4px; padding: 6px 12px; font-size: 12px;" onclick="navigateThematic('${catId}', '${item.catId}', '${item.id}')">Подробнее</button>
          </div>
        </div>
      `;
    }

    async function handleThematicSubmit(e, serviceName) {
      e.preventDefault();
      const name = document.getElementById('them-name').value.trim();
      const phone = document.getElementById('them-phone').value.trim();
      const city = currentCity;

      if (!name || !phone) return;

      try {
        const res = await fetch(API_BASE + '/api/callback', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name, phone, service: serviceName, city })
        });
        if (res.ok) {
          alert('Заявка успешно принята! Мы свяжемся с вами в течение 10 минут.');
          document.getElementById('them-name').value = '';
          document.getElementById('them-phone').value = '';
        } else {
          alert('Произошла ошибка при отправке заявки. Попробуйте еще раз.');
        }
      } catch (err) {
        console.error(err);
        alert('Произошла ошибка сети. Попробуйте еще раз.');
      }
    }

    window.navigateThematic = function (catId, subcatId = '', itemId = '') {
      let path = '/';
      if (catId) {
        path += catId;
        if (subcatId) {
          path += '/' + subcatId;
          if (itemId) {
            path += '/' + itemId;
          }
        }
      }
      
      const isMobile = window.innerWidth < 768;
      if (isMobile && catId) {
        window.open(path, '_blank');
        closeMegaModal();
        return;
      }

      if (window.location.pathname !== path) {
        history.pushState({ catId, subcatId, itemId }, '', path);
      }
      renderThematicPage(catId, subcatId, itemId);
      closeMegaModal();
    };

    function initRouter() {
      const path = window.location.pathname;
      if (path === '/' || path === '/index.html' || path === '/admin.html') {
        renderThematicPage(null);
        return;
      }

      const parts = path.split('/').filter(Boolean);
      if (parts.length > 0) {
        const resolved = resolveCatalogRoute(parts);
        if (resolved) {
          renderThematicPage(resolved.tabId, resolved.catId, resolved.itemId);
        } else {
          renderThematicPage(parts[0], parts.length > 1 ? parts[1] : null, parts.length > 2 ? parts[2] : null);
        }
      }
    }"""

    # Replace content between start_idx and end_idx
    content = content[:start_idx] + new_routing_block + content[end_idx:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully updated routing in {filepath}!")

update_routing("index.html")
update_routing("hubmaster.html")
