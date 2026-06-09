import { useState } from 'react';
import Navbar from './components/Navbar/Navbar';
import Catalog from './components/Catalog/Catalog';
import Coverage from './components/Coverage/Coverage';
import Reviews from './components/Reviews/Reviews';
import Modal from './components/Modal/Modal';
import { useLang } from './hooks/useLang';
import { useTheme } from './hooks/useTheme';
import { useModal } from './hooks/useModal';
import { i18n } from './data/i18n';
import './App.css';

function App() {
  const { lang, switchLang } = useLang();
  const { theme, toggleTheme } = useTheme();
  const { modal, openModal, closeModal } = useModal();
  const [city, setCity] = useState('Алматы');

  const t = i18n[lang] || i18n['RU'];

  const handleCityToggle = () => {
    setCity(prev => prev === 'Алматы' ? 'Астана' : 'Алматы');
  };

  return (
    <div className="app-container">
      <Navbar 
        lang={lang} 
        switchLang={switchLang} 
        theme={theme} 
        toggleTheme={toggleTheme} 
        city={city} 
        onCityToggle={handleCityToggle} 
        onOpenModal={openModal} 
        t={t} 
      />
      
      <main>
        {/* Placeholder for Hero Section */}
        <section style={{ padding: '80px 0', textAlign: 'center' }}>
          <div className="max-width-wrap">
            <h1 style={{ fontSize: '48px', marginBottom: '20px', fontFamily: 'var(--font-heading)' }}>
              {t.heroTitle1} <span style={{ color: 'var(--primary)' }}>{t.heroTitle2}</span> {t.heroTitle3}
            </h1>
            <p style={{ fontSize: '18px', color: 'var(--text-muted)', marginBottom: '40px' }}>
              {t.heroSub}
            </p>
            <button 
              onClick={() => openModal()}
              style={{ padding: '15px 30px', fontSize: '18px', background: 'var(--primary)', color: '#fff', border: 'none', borderRadius: '12px', cursor: 'pointer', fontWeight: 'bold' }}
            >
              {t.heroCta}
            </button>
          </div>
        </section>

        <Catalog lang={lang} t={t} onOpenModal={openModal} />
        <Coverage city={city} t={t} />
        <Reviews lang={lang} t={t} />
      </main>

      {/* Basic Footer Placeholder */}
      <footer style={{ background: 'var(--bg-nav)', padding: '40px 0', borderTop: '1px solid var(--border)', marginTop: '60px' }}>
        <div className="max-width-wrap">
          <p style={{ color: 'var(--text-muted)', fontSize: '14px', textAlign: 'center' }}>{t.copyRight}</p>
        </div>
      </footer>

      <Modal 
        open={modal.open} 
        service={modal.service} 
        onClose={closeModal} 
        t={t} 
        lang={lang} 
      />
    </div>
  );
}

export default App;
