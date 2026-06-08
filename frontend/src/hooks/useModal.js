import { useState, useCallback } from 'react';

export function useModal() {
  const [modal, setModal] = useState({ open: false, service: '' });

  const openModal  = useCallback((service = '') => setModal({ open: true,  service }), []);
  const closeModal = useCallback(() =>            setModal({ open: false, service: '' }), []);

  return { modal, openModal, closeModal };
}
