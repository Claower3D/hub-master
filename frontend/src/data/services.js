// ============================================================
// HubMaster — Service catalog data
// ============================================================

export const servicesData = [
  // Сборка мебели
  {
    id: 1, category: 'furniture',
    nameRU: 'Сборка кухни',        nameKZ: 'Асүй жинау',         nameEN: 'Kitchen Assembly',
    price: 15000, priceType: 'от',
    image: 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&q=80',
  },
  {
    id: 2, category: 'furniture',
    nameRU: 'Сборка шкафа-купе',   nameKZ: 'Шкаф-купе жинау',    nameEN: 'Wardrobe Assembly',
    price: 8000,  priceType: 'от',
    image: 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400&q=80',
  },
  {
    id: 3, category: 'furniture',
    nameRU: 'Перетяжка дивана',    nameKZ: 'Диванды қайта тігу', nameEN: 'Sofa Re-upholstery',
    price: 12000, priceType: 'от',
    image: 'https://images.unsplash.com/photo-1567016432779-094069958ea5?w=400&q=80',
  },
  // Ремонт техники
  {
    id: 4, category: 'appliances',
    nameRU: 'Ремонт стиральной машины', nameKZ: 'Кір жуғыш машинаны жөндеу', nameEN: 'Washing Machine Repair',
    price: 5000, priceType: 'от',
    image: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&q=80',
  },
  {
    id: 5, category: 'appliances',
    nameRU: 'Ремонт холодильника', nameKZ: 'Тоңазытқышты жөндеу', nameEN: 'Fridge Repair',
    price: 6000, priceType: 'от',
    image: 'https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?w=400&q=80',
  },
  // Сантехника
  {
    id: 6, category: 'plumbing',
    nameRU: 'Замена труб',          nameKZ: 'Құбырларды ауыстыру', nameEN: 'Pipe Replacement',
    price: 4000, priceType: 'от',
    image: 'https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=400&q=80',
  },
  // HVAC
  {
    id: 7, category: 'hvac',
    nameRU: 'Установка кондиционера', nameKZ: 'Кондиционер орнату', nameEN: 'AC Installation',
    price: 10000, priceType: 'от',
    image: 'https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=400&q=80',
  },
  // Электрика
  {
    id: 8, category: 'electrical',
    nameRU: 'Замена розеток',       nameKZ: 'Розеткаларды ауыстыру', nameEN: 'Outlet Replacement',
    price: 1500, priceType: 'от',
    image: 'https://images.unsplash.com/photo-1621905251918-48416bd8575a?w=400&q=80',
  },
];

export const categoryTabs = [
  { id: 'all',        labelRU: 'Все',          labelKZ: 'Барлығы',    labelEN: 'All' },
  { id: 'furniture',  labelRU: 'Мебель',       labelKZ: 'Жиһаз',     labelEN: 'Furniture' },
  { id: 'appliances', labelRU: 'Техника',      labelKZ: 'Техника',    labelEN: 'Appliances' },
  { id: 'plumbing',   labelRU: 'Сантехника',   labelKZ: 'Сантехника', labelEN: 'Plumbing' },
  { id: 'hvac',       labelRU: 'HVAC',         labelKZ: 'HVAC',       labelEN: 'HVAC' },
  { id: 'electrical', labelRU: 'Электрика',    labelKZ: 'Электрика',  labelEN: 'Electrical' },
];
