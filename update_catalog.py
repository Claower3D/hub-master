import json
import re

filepath = 'public/admin.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Find defaultCatalogFallback
match = re.search(r'const defaultCatalogFallback = (\{[\s\S]*?\n    \});', content)
if not match:
    print("Could not find defaultCatalogFallback")
    exit(1)

catalog_json_str = match.group(1)
# Some keys might not be quoted perfectly if it's raw JS, but it looks like standard JSON from the code snippet!
# Let's try parsing it
try:
    catalog = json.loads(catalog_json_str)
except Exception as e:
    print("Failed to parse JSON:", e)
    # If it fails, we will just use string replacement
    
# Let's replace the categories for tab 'okna'
categories = catalog['categories']
categories = [c for c in categories if c.get('tab') != 'okna']

new_okna_categories = [
    { "id": "cat-okna-1", "tab": "okna", "title": "Защита от выпадения детей", "icon": "ri-shield-check-line" },
    { "id": "cat-okna-2", "tab": "okna", "title": "Изготовление окон", "icon": "ri-building-line" },
    { "id": "cat-okna-3", "tab": "okna", "title": "Кованые решётки", "icon": "ri-grid-line" },
    { "id": "cat-okna-4", "tab": "okna", "title": "Москитные сетки", "icon": "ri-window-line" },
    { "id": "cat-okna-5", "tab": "okna", "title": "Плиссе", "icon": "ri-layout-top-line" },
    { "id": "cat-okna-6", "tab": "okna", "title": "Ремонт окон", "icon": "ri-tools-line" }
]
catalog['categories'] = new_okna_categories + categories

# Replace subcategories
subcategories = catalog['subcategories']
keys_to_delete = [k for k in subcategories.keys() if k.startswith('cat-okna-')]
for k in keys_to_delete:
    del subcategories[k]

subcategories["cat-okna-4"] = [
    { "id": "sub-okna-4-1", "title": "Сетка Антикошка" },
    { "id": "sub-okna-4-2", "title": "Сетка Антимошка" },
    { "id": "sub-okna-4-3", "title": "Сетка Антипыль (Polly tex)" },
    { "id": "sub-okna-4-4", "title": "Сетка дверная" },
    { "id": "sub-okna-4-5", "title": "Сетка раздвижная" },
    { "id": "sub-okna-4-6", "title": "Сетка рулонная москитная" },
    { "id": "sub-okna-4-7", "title": "Сетка стандартная" }
]

# Update details
details = catalog['details']
details["sub-okna-4-7"] = {
    "title": "Сетка стандартная",
    "desc": "Тип: рамочная москитная сетка. Профиль рамки — алюминиевый окрашенный (белый/коричневый, цвет по RAL под заказ). Полотно — фибергласс (стекловолокно) с ПВХ-покрытием, ячейка 1,2×1,2 мм, цвет серый/чёрный. Уплотнительный шнур (кедер) Ø 4 мм. Крепление — наружные Z-образные кронштейны (плунжерные). В комплекте 2 пластиковые ручки. Изготовление по индивидуальным размерам проёма, макс. размер до 1,5×1,8 м. Защита от комаров, мошки, мух и тополиного пуха.",
    "price": "от 7 000 ₸",
    "time": "Срок: 1-3 дня",
    "warr": "Гарантия: 12 мес",
    "image": "https://images.unsplash.com/photo-1581092921461-eab62e97a780?q=80&w=600"
}
# Also add mock details for others just so they have something
details["sub-okna-4-1"] = { "title": "Сетка Антикошка", "desc": "Усиленное полотно из нержавеющей стали или прочного полиэстера. Выдерживает когти домашних животных и прыжки.", "price": "от 12 000 ₸", "time": "Срок: 1-3 дня", "warr": "Гарантия: 12 мес" }
details["sub-okna-4-2"] = { "title": "Сетка Антимошка", "desc": "Сетка с очень мелкими ячейками, защищающая от самой мелкой мошкары.", "price": "от 9 000 ₸", "time": "Срок: 1-3 дня", "warr": "Гарантия: 12 мес" }
details["sub-okna-4-3"] = { "title": "Сетка Антипыль (Polly tex)", "desc": "Инновационное полотно Polly tex, задерживающее пыль и пыльцу. Идеально для аллергиков.", "price": "от 15 000 ₸", "time": "Срок: 1-3 дня", "warr": "Гарантия: 12 мес" }
details["sub-okna-4-4"] = { "title": "Сетка дверная", "desc": "Усиленная москитная сетка на петлях для балконных и входных дверей.", "price": "от 18 000 ₸", "time": "Срок: 1-3 дня", "warr": "Гарантия: 12 мес" }
details["sub-okna-4-5"] = { "title": "Сетка раздвижная", "desc": "Раздвижные москитные сетки для лоджий и балконов с алюминиевым остеклением.", "price": "от 14 000 ₸", "time": "Срок: 1-3 дня", "warr": "Гарантия: 12 мес" }
details["sub-okna-4-6"] = { "title": "Сетка рулонная москитная", "desc": "Рулонная москитная сетка, которую можно легко скрутить в короб, когда она не нужна.", "price": "от 20 000 ₸", "time": "Срок: 1-3 дня", "warr": "Гарантия: 12 мес" }


new_json_str = json.dumps(catalog, ensure_ascii=False, indent=2)

new_content = content[:match.start()] + 'const defaultCatalogFallback = ' + new_json_str + ';' + content[match.end():]

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated admin.html successfully!")

# Now, we also need to update backend/catalog_data.json if it exists, or push to API
import urllib.request
import urllib.parse
# Save it as catalog_data.json just in case
with open('catalog_data.json', 'w', encoding='utf-8') as f:
    f.write(new_json_str)
print("Saved to catalog_data.json")

