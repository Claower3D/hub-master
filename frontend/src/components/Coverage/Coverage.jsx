import { coverageData } from '../../data/i18n';
import styles from './Coverage.module.css';

const CheckIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
    <polyline points="20 6 9 17 4 12"/>
  </svg>
);
const PinIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/>
    <circle cx="12" cy="9" r="2.5"/>
  </svg>
);
const ClockIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
  </svg>
);
const TeamIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/>
    <circle cx="9" cy="7" r="4"/>
  </svg>
);

export default function Coverage({ city, t }) {
  const data = coverageData[city] || coverageData['Алматы'];

  return (
    <section className={styles.section}>
      <div className="max-width-wrap">
        <div className={styles.inner}>

          {/* LEFT */}
          <div className={styles.left}>
            <div className={styles.badge}>
              <PinIcon />
              Районы выезда
            </div>

            <h2 className={styles.heading}>
              {t.coverageTitle}<br />
              <span className={styles.cityAccent}>{city}</span>
            </h2>
            <p className={styles.desc}>{t.coverageSub}</p>

            <div className={styles.addressCard}>
              <div className={styles.addressIcon}>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="3" y="3" width="18" height="18" rx="2"/>
                  <path d="M3 9h18M9 21V9"/>
                </svg>
              </div>
              <div>
                <div className={styles.addressMain}>{data.address}</div>
                <div className={styles.addressSub}>{t.serviceCenter}</div>
              </div>
            </div>

            <div className={styles.statsRow}>
              <div className={styles.stat}><PinIcon />{data.districts.length} районов охвата</div>
              <div className={styles.stat}><ClockIcon />45 {t.deliveryTime}</div>
              <div className={styles.stat}><TeamIcon />{t.allDay}</div>
            </div>
          </div>

          {/* RIGHT */}
          <div className={styles.right}>
            <div className={styles.rightBadge}>
              <PinIcon />
              {t.zonesLabel} — {city}
            </div>
            <div className={styles.districtsGrid}>
              {data.districts.map((d, i) => (
                <div key={i} className={styles.chip}>
                  <CheckIcon />
                  {d}
                </div>
              ))}
            </div>
          </div>

        </div>
      </div>
    </section>
  );
}
