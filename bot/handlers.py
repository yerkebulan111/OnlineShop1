from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import aiohttp
from .config import API_URL
from .keyboards import main_menu, categories_keyboard, item_actions_keyboard, admin_menu, superadmin_menu, guest_menu

router = Router()

# Store user sessions (username, password, and role for authentication)
user_sessions = {}


class Registration(StatesGroup):
    username = State()
    password = State()
    email = State()


class Login(StatesGroup):
    username = State()
    password = State()


class Search(StatesGroup):
    query = State()


# ============ START & HELP ============
@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    if user_id in user_sessions:
        role = user_sessions[user_id].get('role', 'user')
        keyboard = get_menu_by_role(role)
        await message.answer(
            f"👋 С возвращением, {user_sessions[user_id]['username']}!",
            reply_markup=keyboard
        )
    else:
        await message.answer(
            f"👋 Добро пожаловать в магазин носков!\n\n"
            f"🔹 /register - Регистрация\n"
            f"🔹 /login - Войти\n"
            f"🔹 /help - Помощь",
            reply_markup=guest_menu()
        )


@router.message(Command("help"))
async def cmd_help(message: Message):
    help_text = """
📋 Доступные команды:

🔹 /start - Начать
🔹 /register - Регистрация
🔹 /login - Войти
🔹 /logout - Выйти
🔹 /categories - Категории носков
🔹 /all - Все товары
🔹 /search - Поиск товаров
🔹 /cart - Корзина
🔹 /help - Помощь
    """
    await message.answer(help_text)


def get_menu_by_role(role):
    if role == 'superadmin':
        return superadmin_menu()
    elif role == 'admin':
        return admin_menu()
    else:
        return main_menu()


# ============ REGISTRATION ============
@router.message(Command("register"))
async def cmd_register(message: Message, state: FSMContext):
    await message.answer("Давайте создадим аккаунт!\n\nВведите имя пользователя:")
    await state.set_state(Registration.username)


@router.message(Registration.username)
async def process_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("Отлично! Теперь введите пароль:")
    await state.set_state(Registration.password)


@router.message(Registration.password)
async def process_password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await message.answer("Введите email (или нажмите /skip):")
    await state.set_state(Registration.email)


@router.message(Registration.email)
async def process_email(message: Message, state: FSMContext):
    data = await state.get_data()

    user_data = {
        'username': data['username'],
        'password': data['password'],
        'email': message.text if message.text != '/skip' else '',
        'role': 'user'  # YES! Always registers as 'user'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_URL}/users/", json=user_data) as response:
            if response.status == 201:
                await message.answer(
                    "✅ Регистрация успешна! Вы зарегистрированы как обычный пользователь.\nИспользуйте /login для входа.")
            else:
                error = await response.json()
                await message.answer(f"❌ Ошибка регистрации: {error}")

    await state.clear()


# ============ LOGIN WITH VALIDATION ============
@router.message(Command("login"))
async def cmd_login(message: Message, state: FSMContext):
    await message.answer("Введите имя пользователя:")
    await state.set_state(Login.username)


@router.message(Login.username)
async def login_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("Введите пароль:")
    await state.set_state(Login.password)


@router.message(Login.password)
async def login_password(message: Message, state: FSMContext):
    data = await state.get_data()
    username = data['username']
    password = message.text
    user_id = message.from_user.id

    # Validate credentials by getting user info
    auth = aiohttp.BasicAuth(username, password)

    async with aiohttp.ClientSession() as session:
        # Use the /me endpoint to get current user info
        async with session.get(f"{API_URL}/users/me/", auth=auth) as response:
            if response.status == 200:
                user_data = await response.json()
                role = user_data.get('role', 'user')

                # Store credentials with role
                user_sessions[user_id] = {
                    'username': username,
                    'password': password,
                    'role': role,
                    'user_id': user_data['id']
                }

                keyboard = get_menu_by_role(role)
                role_text = {
                    'superadmin': 'Суперадминистратор',
                    'admin': 'Администратор (Продавец)',
                    'user': 'Пользователь'
                }

                await message.answer(
                    f"✅ Вы вошли как {username}!\n"
                    f"Роль: {role_text.get(role, 'Пользователь')}",
                    reply_markup=keyboard
                )
            elif response.status == 401 or response.status == 403:
                await message.answer("❌ Неверное имя пользователя или пароль!")
            else:
                await message.answer("❌ Ошибка входа. Попробуйте снова.")

    await state.clear()


# ============ LOGOUT ============
@router.message(Command("logout"))
@router.message(F.text == "🚪 Выйти")
async def cmd_logout(message: Message):
    user_id = message.from_user.id
    if user_id in user_sessions:
        del user_sessions[user_id]
        await message.answer("👋 Вы вышли из аккаунта.", reply_markup=guest_menu())
    else:
        await message.answer("Вы не были авторизованы.")


# ============ CHECK AUTH ============
def check_auth(user_id):
    return user_id in user_sessions


# ============ CATEGORIES ============
@router.message(Command("categories"))
@router.message(F.text == "📂 Категории")
async def cmd_categories(message: Message):
    user_id = message.from_user.id
    if not check_auth(user_id):
        await message.answer("❌ Сначала войдите в систему: /login")
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/categories/") as response:
            if response.status == 200:
                categories = await response.json()
                keyboard = categories_keyboard(categories)
                await message.answer("📂 Выберите категорию:", reply_markup=keyboard)
            else:
                await message.answer("❌ Не удалось загрузить категории.")


@router.callback_query(F.data.startswith("category_"))
async def show_category_items(callback: CallbackQuery):
    category_id = callback.data.split("_")[1]

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/items/?category={category_id}") as response:
            if response.status == 200:
                items = await response.json()
                if not items:
                    await callback.message.answer("📦 В этой категории пока нет товаров.")
                else:
                    for item in items:
                        text = f"🧦 **{item['name']}**\n\n"
                        text += f"📁 Категория: {item['category_name']}\n"
                        text += f"💰 Цена: {item['price']} тг\n"
                        text += f"📦 В наличии: {item['stock']} шт\n"
                        text += f"📝 {item['description']}\n"

                        keyboard = item_actions_keyboard(item['id'])
                        await callback.message.answer(text, parse_mode="Markdown", reply_markup=keyboard)
            else:
                await callback.message.answer("❌ Ошибка загрузки товаров.")

    await callback.answer()


# ============ ALL ITEMS ============
@router.message(Command("all"))
@router.message(F.text == "📦 Все товары")
async def cmd_all_items(message: Message):
    user_id = message.from_user.id
    if not check_auth(user_id):
        await message.answer("❌ Сначала войдите в систему: /login")
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/items/") as response:
            if response.status == 200:
                items = await response.json()
                if not items:
                    await message.answer("📦 Товаров пока нет.")
                else:
                    await message.answer(f"📦 Всего товаров: {len(items)}\n")
                    for item in items:
                        text = f"🧦 **{item['name']}**\n\n"
                        text += f"📁 Категория: {item['category_name']}\n"
                        text += f"💰 Цена: {item['price']} тг\n"
                        text += f"📦 В наличии: {item['stock']} шт\n"
                        text += f"📝 {item['description']}\n"

                        keyboard = item_actions_keyboard(item['id'])
                        await message.answer(text, parse_mode="Markdown", reply_markup=keyboard)
            else:
                await message.answer("❌ Ошибка загрузки товаров.")


# ============ SEARCH ============
@router.message(Command("search"))
@router.message(F.text == "🔍 Поиск")
async def cmd_search(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if not check_auth(user_id):
        await message.answer("❌ Сначала войдите в систему: /login")
        return

    await message.answer("🔍 Введите название товара для поиска:")
    await state.set_state(Search.query)


@router.message(Search.query)
async def process_search(message: Message, state: FSMContext):
    query = message.text

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/items/?search={query}") as response:
            if response.status == 200:
                items = await response.json()
                if not items:
                    await message.answer(f"❌ Товары по запросу '{query}' не найдены.")
                else:
                    await message.answer(f"🔍 Найдено: {len(items)} товар(ов)\n")
                    for item in items:
                        text = f"🧦 **{item['name']}**\n\n"
                        text += f"📁 Категория: {item['category_name']}\n"
                        text += f"💰 Цена: {item['price']} тг\n"
                        text += f"📦 В наличии: {item['stock']} шт\n"
                        text += f"📝 {item['description']}\n"

                        keyboard = item_actions_keyboard(item['id'])
                        await message.answer(text, parse_mode="Markdown", reply_markup=keyboard)
            else:
                await message.answer("❌ Ошибка поиска.")

    await state.clear()


# ============ ADD TO CART ============
@router.callback_query(F.data.startswith("addcart_"))
async def add_to_cart(callback: CallbackQuery):
    user_id = callback.from_user.id

    if not check_auth(user_id):
        await callback.message.answer("❌ Сначала войдите в систему: /login")
        await callback.answer()
        return

    item_id = callback.data.split("_")[1]
    auth = aiohttp.BasicAuth(
        user_sessions[user_id]['username'],
        user_sessions[user_id]['password']
    )

    cart_data = {
        'item': int(item_id),
        'quantity': 1
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_URL}/cart/", json=cart_data, auth=auth) as response:
            if response.status == 201:
                await callback.message.answer("✅ Товар добавлен в корзину!")
            else:
                await callback.message.answer("❌ Ошибка добавления в корзину.")

    await callback.answer()


# ============ CART ============
@router.message(Command("cart"))
@router.message(F.text == "🛒 Корзина")
async def cmd_cart(message: Message):
    user_id = message.from_user.id

    if not check_auth(user_id):
        await message.answer("❌ Сначала войдите в систему: /login")
        return

    auth = aiohttp.BasicAuth(
        user_sessions[user_id]['username'],
        user_sessions[user_id]['password']
    )

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/cart/", auth=auth) as response:
            if response.status == 200:
                cart_items = await response.json()
                if not cart_items:
                    await message.answer("🛒 Ваша корзина пуста.")
                else:
                    total = 0
                    text = "🛒 **Ваша корзина:**\n\n"
                    for cart_item in cart_items:
                        item_total = float(cart_item['total_price'])
                        total += item_total
                        text += f"🧦 {cart_item['item_name']}\n"
                        text += f"   Цена: {cart_item['item_price']} тг x {cart_item['quantity']} = {item_total} тг\n\n"

                    text += f"💰 **Итого: {total} тг**"
                    await message.answer(text, parse_mode="Markdown")
            else:
                await message.answer("❌ Ошибка загрузки корзины.")


# ============ TEXT BUTTON HANDLERS ============
@router.message(F.text == "🔐 Войти")
async def text_login(message: Message, state: FSMContext):
    await cmd_login(message, state)


@router.message(F.text == "📝 Регистрация")
async def text_register(message: Message, state: FSMContext):
    await cmd_register(message, state)

@router.message(F.text == "ℹ️ Помощь")
async def text_help(message: Message):
    await cmd_help(message)