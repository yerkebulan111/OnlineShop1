# Online Shop - Telegram Bot

Интернет-магазин носков с Telegram ботом для управления товарами и заказами.

## Telegram Bot
   Найдите бота в Telegram: @OnlineShoppp1_bot (https://t.me/OnlineShoppp1_bot)

## Технологии
- **Backend:** Django 5.2.8, Django REST Framework
- **Database:** PostgreSQL
- **Telegram Bot:** aiogram 3.22.0
- **Authentication:** Basic Auth

## Функционал

### Роли пользователей:
1. **SuperAdmin** - управление администраторами и всеми пользователями
2. **Admin (Продавец)** - управление товарами (CRUD)
3. **User** - просмотр товаров, добавление в корзину, покупка

### Возможности:
-  Регистрация и авторизация через Telegram
-  Просмотр товаров по категориям (Спортивные, Классические, Теплые, Детские носки)
-  Поиск товаров
-  Корзина покупок
-  CRUD операции через Telegram Bot API
-  Django Admin панель для управления

## Установка и запуск

### 1. Клонировать репозиторий
```bash
git clone https://github.com/yerkebulan111/OnlineShop1.git
cd OnlineShop1
```

### 2. Создать виртуальное окружение
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

### 3. Установить зависимости
```bash
pip install -r requirements.txt
```

### 4. Настроить PostgreSQL
Создайте базу данных `online_shop1_db` в PostgreSQL

### 5. Создать .env файл
```env
DB_NAME=online_shop1_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your-secret-key
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
```

### 6. Применить миграции
```bash
python manage.py migrate
```

### 7. Создать начальные данные
```bash
python create_initial_data.py
```

### 8. Запустить Django сервер (Terminal 1)
```bash
python manage.py runserver
```

### 9. Запустить Telegram бота (Terminal 2)
```bash
python run_bot.py
```

## Тестовые аккаунты

- **SuperAdmin:** `super_admin` / `123`
- **Admin:** `admin_seller` / `123`
- **User:** `GalymBartay` / `12345678`

## Структура проекта
```
OnlineShop1/
├── OnlineShop1/          # Основные настройки Django
├── shop/                 # Приложение магазина
│   ├── models.py        # Модели (User, Item, Category, Cart)
│   ├── views.py         # API ViewSets
│   ├── serializers.py   # DRF Serializers
│   └── admin.py         # Django Admin
├── bot/                  # Telegram Bot
│   ├── main.py          # Основной файл бота
│   ├── handlers.py      # Обработчики команд
│   ├── keyboards.py     # Клавиатуры бота
│   └── config.py        # Конфигурация
├── manage.py
└── run_bot.py
```

## API Endpoints

- `GET/POST /api/users/` - Управление пользователями
- `GET /api/users/me/` - Информация о текущем пользователе
- `GET/POST /api/items/` - Управление товарами
- `GET /api/categories/` - Категории товаров
- `GET/POST/DELETE /api/cart/` - Корзина

## Telegram Bot команды

- `/start` - Начать работу с ботом
- `/register` - Регистрация
- `/login` - Вход в систему
- `/logout` - Выход
- `/categories` - Просмотр категорий
- `/all` - Все товары
- `/search` - Поиск товаров
- `/cart` - Корзина
- `/help` - Помощь
