import { reviewsData } from '../../data/reviews';
import styles from './Reviews.module.css';

const Stars = ({ n = 5 }) => '★'.repeat(n);

export default function Reviews({ lang, t }) {
  const getName = r => lang === 'KZ' ? r.nameKZ : lang === 'EN' ? r.nameEN : r.nameRU;
  const getText = r => lang === 'KZ' ? r.textKZ : lang === 'EN' ? r.textEN : r.textRU;

  return (
    <section className={styles.section} id="reviews">
      <div className="max-width-wrap">
        <div className={styles.header}>
          <h2 className={styles.title}>{t.reviewsTitle}</h2>
          <p className={styles.subtitle}>{t.reviewsSub}</p>
        </div>
        <div className={styles.grid}>
          {reviewsData.map(r => (
            <div key={r.id} className={styles.card}>
              <div className={styles.cardHeader}>
                <div className={styles.avatar} style={{ background: r.color }}>{r.avatar}</div>
                <div>
                  <div className={styles.name}>{getName(r)}</div>
                  <div className={styles.service}>{r.service}</div>
                </div>
              </div>
              <div className={styles.stars}><Stars n={r.rating} /></div>
              <p className={styles.text}>{getText(r)}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
