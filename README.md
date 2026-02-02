# 🎮 ПАРТМАРТ Cards Generator

Профессиональный генератор карточек для объявлений на Авито с 5 стилями дизайна.

![Python 3.14+](https://img.shields.io/badge/python-3.14%2B-blue)
![Django 6.0](https://img.shields.io/badge/django-6.0-green)
![Pillow 12.1](https://img.shields.io/badge/pillow-12.1-orange)
![License MIT](https://img.shields.io/badge/license-MIT-purple)

## ✨ Фичи

### 🎨 5 Профессиональных Стилей

1. **🔴 MSI Gaming** - Агрессивный игровой стиль с красными акцентами
2. **🎮 Steam Library** - Стиль платформы Steam с тёмным фоном
3. **🍎 Apple Premium** - Минималистичный премиум дизайн
4. **🎵 Spotify Minimal** - Чистый стиль с зелёными акцентами
5. **💜 MIXPC Series** - Серия из 6 карточек в стиле MIXPC для Авито

### 🚀 Основные возможности

- ⚡ **Быстрая генерация** - Готовая карточка за 1-2 минуты
- 🎨 **Glass Morphism** - Современные эффекты стекла
- 🖼️ **Автоматическая обработка фото** - Коррекция и оптимизация
- 📊 **Таблицы характеристик** - Красивое отображение комплектующих
- 🎮 **FPS показатели** - Тесты в 8 популярных играх
- 📦 **ZIP архивы** - Скачивание серий карточек

## 🛠️ Требования

- **Python 3.14+** (тестировано на 3.14 и 3.15)
- Django 6.0+
- Pillow 12.1+
- Git

## 🚀 Быстрый старт

### 1. Клонирование

```bash
git clone https://github.com/vitorpixel-6436/partmart-cards.git
cd partmart-cards
```

### 2. Виртуальное окружение

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
# Обновление pip
python -m pip install --upgrade pip

# Установка зависимостей
pip install -r requirements.txt
```

**Что установится:**
- Django 6.0.1
- Pillow 12.1.0
- Steam UI Framework (из music-stream-app)
- Django Crispy Forms
- Crispy Bootstrap5

### 4. Миграции базы данных

```bash
# Применить миграции
python manage.py migrate

# Создать суперпользователя (опционально)
python manage.py createsuperuser
```

### 5. Запуск

```bash
python manage.py runserver
```

🎉 **Готово!** Откройте http://127.0.0.1:8000

## 📚 Использование

### Генерация одной карточки

1. Перейдите на страницу «Создать»
2. Загрузите фото ПК
3. Укажите характеристики:
   - Процессор (CPU)
   - Видеокарта (GPU)
   - Оперативная память (RAM)
   - Накопитель (SSD)
   - Материнская плата
   - Блок питания (PSU)
4. Выберите стиль
5. Нажмите «Генерировать»

### Генерация MIXPC Series (6 карточек)

1. Перейдите в «MIXPC Gallery»
2. Нажмите «Создать серию»
3. Заполните форму
4. Получите 6 карточек:
   - 🎮 Игровой компьютер
   - ⚙️ Конфигурация
   - 🎮 Тесты в играх
   - 🧪 Тестирование
   - 🚚 Доставка
   - 💰 Трейд-ин
5. Скачайте все карточки в ZIP

## 🎯 Примеры использования

### Бюджетный ПК
```
CPU: AMD Ryzen 5 7500F
GPU: RTX 4060 8GB GDDR6
RAM: DDR5 16GB (2x8GB)
SSD: M.2 512GB NVMe
Price: 45,000 ₽
```

### Средний ПК
```
CPU: AMD Ryzen 7 7700X
GPU: RTX 4070 Super 12GB
RAM: DDR5 32GB (2x16GB)
SSD: M.2 1TB NVMe
Price: 85,000 ₽
```

### Топовый ПК
```
CPU: AMD Ryzen 9 7950X
GPU: RTX 4090 24GB GDDR6X
RAM: DDR5 64GB (2x32GB)
SSD: M.2 2TB NVMe
Price: 250,000 ₽
```

## 🎨 Стили

### MSI Gaming
- 🔴 Красные акценты
- ⚫ Тёмный фон
- 🔥 Агрессивный дизайн

### Steam Library
- 🔵 Синие акценты
- 🖤 Тёмно-серый фон
- 🎮 Стиль платформы

### Apple Premium
- ⚪ Белые акценты
- 🌑 Светлый фон
- 🍎 Минимализм

### Spotify Minimal
- 🟢 Зелёные акценты
- ⚫ Чёрный фон
- 🎵 Чистый дизайн

### MIXPC Series
- 💜 Фиолетово-розовый
- ✨ Glass morphism
- 📊 6 карточек в серии

## 🛠️ Структура проекта

```
partmart-cards/
├── cards/                   # Основное приложение
│   ├── generators/        # Генераторы карточек
│   │   ├── base_generator.py
│   │   ├── msi_style.py
│   │   ├── steam_style.py
│   │   ├── apple_style.py
│   │   ├── spotify_style.py
│   │   └── mixpc_series.py
│   ├── templates/         # Шаблоны
│   ├── models.py          # Модели
│   ├── views.py           # Представления
│   └── urls.py            # Маршруты
├── media/                 # Медиа-файлы
│   ├── uploads/           # Загруженные фото
│   └── generated/         # Генерированные карточки
├── partmart_cards/       # Настройки проекта
├── requirements.txt       # Зависимости
└── manage.py              # Django команды
```

## 🔧 Troubleshooting

### Ошибка миграций

```bash
python manage.py makemigrations
python manage.py migrate --run-syncdb
```

### Проблемы с фото

```bash
# Создайте необходимые папки
mkdir -p media/uploads media/generated

# Linux/Mac: установите права
chmod -R 755 media/
```

### Ошибка Steam UI

```bash
# Переустановите библиотеку
pip uninstall music-stream-app -y
pip install git+https://github.com/vitorpixel-6436/music-stream-app.git
```

## 📝 Технологии

- **Backend**: Django 6.0.1
- **Изображения**: Pillow 12.1.0
- **UI Framework**: Steam UI (glass morphism)
- **Frontend**: Tailwind CSS + Custom CSS
- **БД**: SQLite (default), PostgreSQL (production)

## 🚀 Production развертывание

### Docker

```dockerfile
FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "partmart_cards.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Настройка безопасности

```python
# settings.py (production)
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECRET_KEY = os.environ.get('SECRET_KEY')

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## 🤝 Вклад

Contributions welcome! Откройте issue или pull request.

## 📜 Лицензия

MIT License - используйте свободно!

## 🔗 Ссылки

- [GitHub Repository](https://github.com/vitorpixel-6436/partmart-cards)
- [Steam UI Framework](https://github.com/vitorpixel-6436/music-stream-app)
- [Issue Tracker](https://github.com/vitorpixel-6436/partmart-cards/issues)

---

💜 Made with love by **vitorpixel-6436** | Powered by Django + Pillow + Steam UI
