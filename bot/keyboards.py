from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def guest_menu():
    """Menu for users who are not logged in"""
    keyboard = [
        [KeyboardButton(text="🔐 Войти"), KeyboardButton(text="📝 Регистрация")],
        [KeyboardButton(text="ℹ️ Помощь")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def main_menu():
    """Menu for regular users"""
    keyboard = [
        [KeyboardButton(text="📦 Все товары"), KeyboardButton(text="📂 Категории")],
        [KeyboardButton(text="🔍 Поиск"), KeyboardButton(text="🛒 Корзина")],
        [KeyboardButton(text="ℹ️ Помощь"), KeyboardButton(text="🚪 Выйти")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def admin_menu():
    """Menu for admin (seller) users"""
    keyboard = [
        [KeyboardButton(text="📦 Все товары"), KeyboardButton(text="📂 Категории")],
        [KeyboardButton(text="🔍 Поиск"), KeyboardButton(text="🛒 Корзина")],
        [KeyboardButton(text="➕ Добавить товар"), KeyboardButton(text="✏️ Управление товарами")],
        [KeyboardButton(text="ℹ️ Помощь"), KeyboardButton(text="🚪 Выйти")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def superadmin_menu():
    """Menu for superadmin users"""
    keyboard = [
        [KeyboardButton(text="👥 Управление пользователями")],
        [KeyboardButton(text="📦 Управление товарами"), KeyboardButton(text="📂 Категории")],
        [KeyboardButton(text="➕ Добавить админа"), KeyboardButton(text="🗑 Удалить админа")],
        [KeyboardButton(text="ℹ️ Помощь"), KeyboardButton(text="🚪 Выйти")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def categories_keyboard(categories):
    buttons = []
    for category in categories:
        buttons.append([InlineKeyboardButton(
            text=category['name'],
            callback_data=f"category_{category['id']}"
        )])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def item_actions_keyboard(item_id):
    buttons = [
        [InlineKeyboardButton(text="➕ Добавить в корзину", callback_data=f"addcart_{item_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)