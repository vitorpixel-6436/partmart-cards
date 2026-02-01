# 🛠 Установка ПАРТМАРТ Cards Generator

## Требования

- **Python 3.14+** (тестировано на 3.14 и 3.15)
- pip (latest)
- Virtualenv (рекомендуется)

## Быстрая установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/vitorpixel-6436/partmart-cards.git
cd partmart-cards
```

### 2. Проверка версии Python

```bash
python --version  # Должно быть Python 3.14.0 или выше
```

### 3. Создание виртуального окружения

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### 4. Обновление pip

```bash
python -m pip install --upgrade pip
```

### 5. Установка зависимостей

```bash
pip install -r requirements.txt
```

**Что установится:**
- Django 5.1+ (с поддержкой Python 3.14+)
- Pillow 11.0+ (последняя версия)
- Django Crispy Forms 2.3+
- Crispy Bootstrap5 2.0+

### 6. Миграции базы данных

```bash
python manage.py migrate
```

### 7. Создание суперпользователя (опционально)

```bash
python manage.py createsuperuser
```

### 8. Сбор статических файлов (для production)

```bash
python manage.py collectstatic --noinput
```

### 9. Запуск сервера

```bash
python manage.py runserver
```

Откройте браузер: **http://127.0.0.1:8000**

## Настройка шрифтов

Для корректной генерации карточек убедитесь, что установлены необходимые шрифты:

**Linux:**
```bash
sudo apt-get install fonts-dejavu fonts-liberation
```

**Mac:**
Шрифты уже установлены в системе

**Windows:**
Шрифты Arial установлены по умолчанию

## Структура директорий

После запуска автоматически создадутся:

```
media/
├── uploads/          # Загруженные фото ПК
└── generated/        # Сгенерированные карточки
```

## Troubleshooting

### Ошибка версии Python

Если у вас Python < 3.14:

```bash
# Скачайте Python 3.14+ с официального сайта
www.python.org/downloads/
```

### Ошибка импорта PIL/Pillow

```bash
pip uninstall Pillow
pip install Pillow --upgrade
```

### Ошибка миграций

```bash
python manage.py makemigrations
python manage.py migrate --run-syncdb
```

### Проблемы с правами на media/ (Linux/Mac)

```bash
chmod -R 755 media/
```

### Ошибка "ModuleNotFoundError"

```bash
# Убедитесь, что виртуальное окружение активировано
pip list  # Проверьте установленные пакеты
```

## Production настройка

### Безопасность

1. **Измените SECRET_KEY** в `settings.py`:
```python
import secrets
SECRET_KEY = secrets.token_urlsafe(50)
```

2. **Отключите DEBUG**:
```python
DEBUG = False
```

3. **Настройте ALLOWED_HOSTS**:
```python
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

### Развертывание с Gunicorn + Nginx

```bash
# Установка Gunicorn
pip install gunicorn

# Запуск
gunicorn partmart_cards.wsgi:application --bind 0.0.0.0:8000
```

### Докер (Docker)

Создайте `Dockerfile`:
```dockerfile
FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

```bash
docker build -t partmart-cards .
docker run -p 8000:8000 partmart-cards
```

## Оптимизация для Python 3.14/3.15

Проект оптимизирован для новых возможностей Python 3.14+:
- Поддержка JIT-компилятора (PEP 744)
- Улучшенная производительность Pillow 11.0+
- Новые возможности Django 5.1+

## Готово! 🎉

Теперь вы можете создавать профессиональные карточки ПАРТМАРТ на Python 3.14/3.15!

👉 См. [USAGE.md](USAGE.md) для полного руководства пользователя
