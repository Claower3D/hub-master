
    // Coverage zone data per city
    const coverageData = {
      'Алматы': {
        address: 'Алматы, ул. Байзакова, 280',
        districts: ['Алмалинский р-н', 'Бостандыкский р-н', 'Ауэзовский р-н', 'Медеуский р-н', 'Наурызбайский р-н', 'Жетысуский р-н', 'Турксибский р-н', 'Алатауский р-н']
      },
      'Астана': {
        address: 'Астана, пр. Республики, 15',
        districts: ['р-н Есиль', 'р-н Алматы', 'р-н Байконур', 'р-н Сарыарка', 'Левый берег', 'Правый берег']
      }
    };

    function updateCoverageBlock(city) {
      const data = coverageData[city] || coverageData['Алматы'];
      const cityEl = document.getElementById('coverage-city-name');
      const addrEl = document.getElementById('coverage-address');
      const countEl = document.getElementById('coverage-district-count');
      const labelEl = document.getElementById('coverage-right-label');
      const gridEl = document.getElementById('coverage-districts-grid');
      if (cityEl) cityEl.textContent = city;
      if (addrEl) addrEl.textContent = data.address;
      if (countEl) countEl.textContent = data.districts.length + ' районов охвата';
      if (labelEl) labelEl.textContent = 'Районы обслуживания — ' + city;
      if (gridEl) {
        gridEl.innerHTML = data.districts.map(d => `
          <div class="district-chip">
            <svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
            ${d}
          </div>
        `).join('');
      }
    }

    // Init on page load
    document.addEventListener('DOMContentLoaded', function () {
      const city = document.getElementById('current-city-label')?.textContent?.trim() || 'Алматы';
      updateCoverageBlock(city);
    });

    // Hook into existing toggleCity if present
    const _origToggleCity = window.toggleCity;
    window.toggleCity = function () {
      if (_origToggleCity) _origToggleCity();
      setTimeout(function () {
        const city = document.getElementById('current-city-label')?.textContent?.trim() || 'Алматы';
        updateCoverageBlock(city);
      }, 100);
    };
  