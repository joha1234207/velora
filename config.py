# Configuration file for the Telegram bot

# Bot token - replace with your actual token
BOT_TOKEN = "8611090952:AAGNRKzckFF_kTVaignhYfcZpBVuz7lBlLQ"

# Admin user ID - replace with your Telegram ID
ADMIN_ID = 7789281265
SUPABASE_URL = "https://ffqjfkqohhwouahxhxtp.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZmcWpma3FvaGh3b3VhaHhoeHRwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzg2ODg5ODgsImV4cCI6MjA5NDI2NDk4OH0.J7q1Owtin84SM3NuzaeuZfGy_oblQfAMStn74o2-uno"

# Pagination settings
POSTS_PER_PAGE = 1

# Text limits
NICKNAME_MIN_LENGTH = 2
NICKNAME_MAX_LENGTH = 16
POST_MAX_LENGTH = 300

# Messages
START_MESSAGE = """
👋 Добро пожаловать в Velora!

Это пространство, где ты можешь: 📝 Публиковать анонимные посты
❤️ Реагировать на посты других людей
🔍 Открывать случайные публикации
📊 Смотреть свой профиль и статистику

Нажми кнопку ниже, чтобы начать ✨
"""

REGISTERED_MESSAGE = """
✅ Ты уже зарегистрирован как: @{}

Выбери действие из меню ниже ✨
"""

REGISTRATION_MESSAGE = """
📝 Добро пожаловать! Давай создадим твой профиль ✨

Твой ник будет отображаться в постах. Он должен: • Быть уникальным
• Содержать от 2 до 16 символов
• Может включать буквы, цифры и нижнее подчёркивание

Отправь свой никнейм 👇
"""

INVALID_NICKNAME = """
❌ Неверный никнейм!

Правила:
 ✓ От 2 до 16 символов
✓ Только буквы, цифры и подчёркивания
✓ Ник должен быть уникальным

Попробуй ещё раз 👇
"""

NICKNAME_TAKEN = """
❌ Этот никнейм уже занят!

Попробуй другой 
"""

REGISTRATION_SUCCESS = """
✅ Регистрация успешно завершена!

Твой никнейм: @{}

Теперь ты можешь: 📝 Публиковать посты
❤️ Реагировать на посты
🔍 Просматривать публикации

Начнём 🚀
"""

ADD_POST_MESSAGE = """
📝 Напиши свой пост (максимум 300 символов)

Отменить можно в любой момент командой /cancel
"""

POST_TOO_LONG = """
❌ Пост слишком длинный!

Максимум: 300 символов
Твой пост: {} символов

Пожалуйста, сократи его ✂️
"""

POST_SUCCESS = """
✅ Твой пост успешно опубликован!

Теперь он виден всем 🌍
Готов добавить ещё один? 🚀
"""

NO_MORE_POSTS = """
😔 Больше постов пока нет.

Попробуй позже или добавь свой собственный пост ✨
"""

PROFILE_MESSAGE = """
👤 Твой профиль

Никнейм: @{}
📝 Всего постов: {}
❤️ Получено лайков: {}
"""

MY_POSTS_EMPTY = """
📭 У тебя пока нет ни одного поста.

Создай свой первый пост с помощью /addpost ✨
"""

ADMIN_PANEL = """
👨‍💼 Панель администратора

Пользователи: {}
Посты: {}
Жалобы на посты: {}

Выбери действие 👇
"""

BROADCAST_MESSAGE = """
📢 Отправь сообщение для рассылки

Оно будет отправлено всем {} пользователям.
Максимум: 300 символов.

Отмена: /cancel
"""

BROADCAST_SUCCESS = """
✅ Сообщение отправлено {} пользователям!
"""

POST_REPORTED = """
✅ Пост отправлен администратору на рассмотрение.

Спасибо, что помогаешь поддерживать платформу безопасной 🤝✨
"""

POST_DELETED_USER = """
✅ Твой пост удалён.
"""

POST_DELETED_ADMIN = """
✅ Пост успешно удалён.
"""

SHARED_POST_MESSAGE = """
🔗 Кто-то поделился с тобой этим постом!

Хочешь его посмотреть? 👀
"""

ERROR_MESSAGE = """
❌ Что-то пошло не так!

Попробуй ещё раз или свяжись с администратором ⚙️
"""
