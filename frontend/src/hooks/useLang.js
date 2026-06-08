import { useState, useCallback } from 'react';

export function useLang() {
  const [lang, setLang] = useState(() => localStorage.getItem('hm-lang') || 'RU');

  const switchLang = useCallback((l) => {
    setLang(l);
    localStorage.setItem('hm-lang', l);
  }, []);

  return { lang, switchLang };
}
