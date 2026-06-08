import styles from './Modal.module.css';
import { servicesData } from '../../data/services';

export default function Modal({ open, service, onClose, t, lang }) {
  if (!open) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    onClose();
  };

  return (
    <div className={`${styles.overlay} ${open ? styles.active : ''}`} onClick={e => e.target === e.currentTarget && onClose()}>
      <div className={styles.box}>
        <button className={styles.closeBtn} onClick={onClose}>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>

        <h2 className={styles.title}>{t.modalTitle}</h2>
        <p className={styles.desc}>{t.modalDesc}</p>

        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.grid}>
            <div className={styles.field}>
              <label>{t.name}</label>
              <input type="text" placeholder={t.name} className={styles.input} required />
            </div>
            <div className={styles.field}>
              <label>{t.phone}</label>
              <input type="tel" placeholder="+7 (___) ___-__-__" className={styles.input} required />
            </div>
          </div>
          <div className={styles.field}>
            <label>{t.service}</label>
            <select className={styles.input} defaultValue={service || ''}>
              <option value="">{t.service}</option>
              {servicesData.map(s => (
                <option key={s.id} value={s.id}>
                  {lang === 'KZ' ? s.nameKZ : lang === 'EN' ? s.nameEN : s.nameRU}
                </option>
              ))}
            </select>
          </div>
          <button type="submit" className={styles.submitBtn}>{t.send}</button>
        </form>
      </div>
    </div>
  );
}
