import { useState, useEffect, useCallback } from 'react';

export function useTheme() {
  const [theme, setTheme] = useState(() => localStorage.getItem('hm-theme') || 'dark');

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('hm-theme', theme);
  }, [theme]);

  const toggleTheme = useCallback(() => {
    setTheme(t => (t === 'dark' ? 'light' : 'dark'));
  }, []);

  return { theme, toggleTheme };
}
