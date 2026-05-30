import styles from './Navbar.module.css';

const SunIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <circle cx="12" cy="12" r="5"/>
    <line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/>
    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
    <line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/>
    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
  </svg>
);
const MoonIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/>
  </svg>
);

export default function Navbar({ lang, switchLang, theme, toggleTheme, city, onCityToggle, onOpenModal, t }) {
  return (
    <nav className={styles.navbar}>
      <div className={`max-width-wrap ${styles.inner}`}>
        {/* Logo */}
        <div className={styles.logoSection}>
          <a href="/" className={styles.logoLink}>
            <div className={styles.logoBox}>
              <span className={styles.logoHm}>HM</span>
              <div className={styles.logoTextWrap}>
                <span className={styles.logoTextHub}>HUB MASTER</span>
                <span className={styles.logoSubtitle}>Алматы — с 2018</span>
              </div>
            </div>
          </a>
          <button className={styles.cityBtn} onClick={onCityToggle}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
              <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/>
              <circle cx="12" cy="9" r="2.5"/>
            </svg>
            {city} ▾
          </button>
        </div>

        {/* Right */}
        <div className={styles.right}>
          {/* Lang */}
          <div className={styles.langSelector}>
            {['RU','KZ','EN'].map((l, i) => (
              <span key={l}>
                <button className={`${styles.langBtn} ${lang === l ? styles.langActive : ''}`} onClick={() => switchLang(l)}>{l}</button>
                {i < 2 && <span className={styles.langDivider}>/</span>}
              </span>
            ))}
          </div>

          {/* Theme toggle */}
          <button className={styles.themeBtn} onClick={toggleTheme} aria-label="Toggle theme">
            {theme === 'dark' ? <SunIcon /> : <MoonIcon />}
          </button>

          {/* WhatsApp phone */}
          <a href="https://wa.me/77058462749" target="_blank" rel="noopener noreferrer" className={styles.phoneBtn}>
            <span className={styles.waBadge}>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81a19.79 19.79 0 01-3.07-8.68A2 2 0 012 1h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 8.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/>
              </svg>
            </span>
            +7 705 846 2749
          </a>

          <button className={styles.cabinetBtn} onClick={() => onOpenModal('cabinet')}>
            {t.cabinet}
          </button>

          <button className={styles.ctaBtn} onClick={() => onOpenModal('general')}>
            {t.leaveRequest}
          </button>
        </div>
      </div>
    </nav>
  );
}
