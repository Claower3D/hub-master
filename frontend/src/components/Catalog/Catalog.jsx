import { useState } from 'react';
import { servicesData, categoryTabs } from '../../data/services';
import styles from './Catalog.module.css';

export default function Catalog({ lang, t, onOpenModal }) {
  const [activeTab, setActiveTab] = useState('all');

  const filtered = activeTab === 'all'
    ? servicesData
    : servicesData.filter(s => s.category === activeTab);

  const getName = (s) => lang === 'KZ' ? s.nameKZ : lang === 'EN' ? s.nameEN : s.nameRU;
  const getTabLabel = (tab) => lang === 'KZ' ? tab.labelKZ : lang === 'EN' ? tab.labelEN : tab.labelRU;

  return (
    <section className={styles.section} id="catalog">
      <div className="max-width-wrap">
        <div className={styles.header}>
          <span className={styles.pretitle}>Каталог</span>
          <h2 className={styles.title}>{t.catalogTitle}</h2>
          <p className={styles.subtitle}>{t.catalogSub}</p>
        </div>

        <div className={styles.tabs}>
          {categoryTabs.map(tab => (
            <button
              key={tab.id}
              className={`${styles.tabBtn} ${activeTab === tab.id ? styles.tabActive : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              {getTabLabel(tab)}
            </button>
          ))}
        </div>

        <div className={styles.grid}>
          {filtered.map(service => (
            <div key={service.id} className={styles.card}>
              <div
                className={styles.cardImg}
                style={{ backgroundImage: `url(${service.image})` }}
              />
              <div className={styles.cardBody}>
                <h3 className={styles.cardTitle}>{getName(service)}</h3>
                <div className={styles.cardBottom}>
                  <div className={styles.price}>
                    {t.priceFrom} <strong>{service.price.toLocaleString()} ₸</strong>
                  </div>
                  <button
                    className={styles.orderBtn}
                    onClick={() => onOpenModal(service.id)}
                  >
                    {t.orderBtn}
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
