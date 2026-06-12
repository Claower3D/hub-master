import styles from './Partners.module.css';

export default function Partners({ t }) {
  return (
    <section className={styles.section} id="partners">
      <div className="max-width-wrap">
        <h2 className={styles.title}>{t.partnersTitle}</h2>

        <div className={styles.category}>
          <span className={styles.categoryLabel}>{t.partnersDeveloper}</span>
          <div className={styles.developerCard}>
            <h3 className={styles.developerTitle}>Everest Development</h3>
            <p className={styles.developerText}>{t.partnersDeveloperText}</p>
          </div>
        </div>

        <div className={styles.category}>
          <span className={styles.categoryLabel}>{t.partnersWindows}</span>
          <div className={styles.tagsContainer}>
            <div className={styles.tag}>WUKO</div>
            <div className={styles.tag}>KAVI</div>
            <div className={styles.tag}>VEKA</div>
            <div className={styles.tag}>REHAU</div>
            <div className={styles.tag}>Euro Super Plast</div>
          </div>
        </div>

        <div className={styles.category}>
          <span className={styles.categoryLabel}>{t.partnersFurniture}</span>
          <div className={styles.tagsContainer}>
            <div className={styles.tag}>Blum</div>
            <div className={styles.tag}>Hettich</div>
            <div className={styles.tag}>Häfele</div>
            <div className={styles.tag}>Egger</div>
            <div className={styles.tag}>Kronospan</div>
          </div>
        </div>

      </div>
    </section>
  );
}
