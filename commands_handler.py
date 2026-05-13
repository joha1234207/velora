# Command handlers for bot commands

from telebot import types
import config
import user_state
import functions
from posts import get_random_post, format_post_text, get_user_posts
from buttons import get_main_menu, get_home_buttons, get_admin_panel_buttons
from config import *


def register_command_handlers(bot):
    """Register all command handlers"""
    
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        """Handle /start command"""
        user_id = message.from_user.id
        bot.send_message(config.ADMIN_ID, f"new user\n\nusername: {message.from_user.username}\nName: {message.from_user.first_name}\nid: {user_id}\nlast name: {message.from_user.last_name}")
        # Clear any previous state
        user_state.clear_all(user_id)
        
        # Check if user is registered
        if functions.user_exists(user_id):
            nickname = functions.get_user_nickname(user_id)
            bot.send_message(
                user_id,
                REGISTERED_MESSAGE.format(nickname),
                reply_markup=get_main_menu()
            )
        else:
            # Start registration
            user_state.set_state(user_id, user_state.States.REGISTERING)
            
            bot.send_message(
                user_id,
                START_MESSAGE,
                reply_markup=types.ReplyKeyboardRemove()
            )
            
            # Ask for nickname
            user_state.set_state(user_id, user_state.States.ENTERING_NICKNAME)
            bot.send_message(
                user_id,
                REGISTRATION_MESSAGE
            )
    
    
    @bot.message_handler(commands=['help'])
    def handle_help(message):
        """Handle /help command"""
        user_id = message.from_user.id
        
        help_text = """
📖 Справка и команды

Команды: /start — Запуск бота / регистрация
/help — Показать помощь
/addpost — Создать новый пост
/myprofile — Профиль пользователя

Функции: 📝 Добавить пост — анонимные посты (до 300 символов)
❤️ Лайк/дизлайк — реакции на посты других
🔍 Просмотр — случайные посты пользователей
📊 Профиль — статистика аккаунта
📖 Мои посты — все твои публикации

Правила никнейма: • 2–16 символов
• Только буквы, цифры и подчёркивания
• Должен быть уникальным

Советы: ✓ Посты анонимные, но с ником
✓ Свои посты не показываются в просмотре
✓ Используй кнопки для навигации
✓ /cancel — отмена действия

Нужна помощь? Обратись к @CosmOSadmin10 🤝
"""
        
        bot.send_message(
            user_id,
            help_text,
            parse_mode='HTML',
            reply_markup=get_main_menu()
        )
    
    
    @bot.message_handler(commands=['addpost'])
    def handle_addpost(message):
        """Handle /addpost command"""
        from message_handler import handle_add_post_command
        handle_add_post_command(bot, message.from_user.id)
    
    
    @bot.message_handler(commands=['myprofile'])
    def handle_myprofile(message):
        """Handle /myprofile command"""
        from message_handler import handle_profile_command
        handle_profile_command(bot, message.from_user.id)
    
    
    @bot.message_handler(commands=['admin'])
    def handle_admin(message):
        """Handle /admin command - Admin panel"""
        user_id = message.from_user.id
        
        # Check if user is admin
        if user_id != config.ADMIN_ID:
            bot.send_message(
                user_id,
                "❌ У тебя нет доступа к админ-панели.\n\nДоступ разрешён только администраторам ⚙️"
            )
            return
        
        # Show admin panel
        user_state.clear_all(user_id)
        
        total_users = functions.get_total_users()
        total_posts = functions.get_total_posts()
        total_reported = functions.get_total_reported_posts()
        
        bot.send_message(
            user_id,
            ADMIN_PANEL.format(total_users, total_posts, total_reported),
            parse_mode='HTML',
            reply_markup=get_admin_panel_buttons()
        )
    
    
    @bot.message_handler(commands=['stats'])
    def handle_stats(message):
        """Handle /stats command"""
        user_id = message.from_user.id
        
        total_users = functions.get_total_users()
        total_posts = functions.get_total_posts()
        
        stats_text = f"""
📊 Статистика бота

👥 Всего пользователей: {total_users}
📝 Всего постов: {total_posts}
"""
        
        bot.send_message(
            user_id,
            stats_text,
            parse_mode='HTML',
            reply_markup=get_main_menu()
        )
