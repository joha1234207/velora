# Message handlers for text input

from telebot import types
import config
import user_state
import functions
from posts import add_post, get_random_post
from buttons import get_main_menu, get_back_button, get_home_buttons
from config import *


def register_message_handlers(bot):
    """Register all message handlers"""
    
    @bot.message_handler(commands=['cancel'])
    def handle_cancel(message):
        """Handle /cancel command"""
        user_id = message.from_user.id
        user_state.clear_all(user_id)
        
        bot.send_message(
            user_id,
            "❌ Действие отменено.",
            reply_markup=get_main_menu()
        )
    
    
    @bot.message_handler(content_types=['text'])
    def handle_text(message):
        """Handle all text messages"""
        user_id = message.from_user.id
        text = message.text.strip()
        state = user_state.get_state(user_id)
        
        # Handle registration state
        if state == user_state.States.ENTERING_NICKNAME:
            handle_nickname_input(bot, user_id, text)
        
        # Handle adding post state
        elif state == user_state.States.ADDING_POST:
            handle_post_input(bot, user_id, text)
        
        # Handle broadcasting state
        elif state == user_state.States.BROADCASTING:
            handle_broadcast_input(bot, user_id, text)
        
        # Handle menu button clicks
        elif text == "🏠 Главная":
            user_state.clear_all(user_id)
            handle_home(bot, user_id)
        
        elif text == "📝 Добавить пост":
            handle_add_post_command(bot, user_id)
        
        elif text == "👤 Профил":
            handle_profile_command(bot, user_id)
        
        elif text == "📖 Мои посты":
            handle_my_posts_command(bot, user_id)
        elif text == "🔍 Рандом пост":
            post = get_random_post(exclude_user_id=user_id)
        if not post:
            bot.send_message(user_id,
                text=NO_MORE_POSTS
            )
            return
                    # Save current post
            user_state.set_data(user_id, "current_post_id", post["post_id"])
            user_state.set_data(user_id, "viewing_posts", True)
        
        # Get reactions
            reactions = get_post_reactions(post["post_id"])
        
        # Format message
            text = format_post_text(post)
            text += f"\n\n👍 {reactions['likes']} | 👎 {reactions['dislikes']}"
        
            bot.send_message(
            text=text,
            parse_mode='HTML',
            reply_markup=get_post_buttons(post["post_id"], is_owner=False)
        )
        
        else:
            bot.send_message(
                user_id,
                "❓ Я не понимаю эту команду.\n\nПожалуйста, используй кнопки меню или введи /start 👇",
                reply_markup=get_main_menu()
            )


def handle_nickname_input(bot, user_id, nickname):
    """Handle nickname input during registration"""
    
    # Validate format
    if not functions.validate_nickname(nickname):
        bot.send_message(
            user_id,
            INVALID_NICKNAME
        )
        return
    
    # Check if taken
    if functions.is_nickname_taken(nickname):
        bot.send_message(
            user_id,
            NICKNAME_TAKEN
        )
        return
    
    # Register user
    if functions.register_user(user_id, nickname):
        user_state.clear_all(user_id)
        
        bot.send_message(
            user_id,
            REGISTRATION_SUCCESS.format(nickname),
            reply_markup=get_main_menu()
        )
    else:
        bot.send_message(
            user_id,
            ERROR_MESSAGE,
            reply_markup=get_back_button()
        )


def handle_post_input(bot, user_id, content):
    """Handle post content input"""
    
    # Validate length
    if not functions.validate_post_length(content):
        bot.send_message(
            user_id,
            POST_TOO_LONG.format(len(content))
        )
        return
        
    # Add post
    post_id = add_post(user_id, content)
    
    if post_id:
        user_state.clear_all(user_id)
        
        bot.send_message(
            user_id,
            POST_SUCCESS,
            reply_markup=get_main_menu()
        )
    else:
        bot.send_message(
            user_id,
            ERROR_MESSAGE,
            reply_markup=get_back_button()
        )


def handle_broadcast_input(bot, user_id, message_text):
    """Handle broadcast message input"""
    
    # Validate length
    if not functions.validate_post_length(message_text):
        bot.send_message(
            user_id,
            POST_TOO_LONG.format(len(message_text))
        )
        return
    
    # Get all users
    conn = __import__('sqlite3').connect(config.DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    # Send message to all users
    sent_count = 0
    for recipient_id in users:
        try:
            bot.send_message(
                recipient_id,
                f"📢 Анонимный пост от CosmOS\n\n<b>{message_text}</b>",
                parse_mode='HTML'
            )
            sent_count += 1
        except:
            pass
    
    user_state.clear_all(user_id)
    
    bot.send_message(
        user_id,
        BROADCAST_SUCCESS.format(sent_count),
        reply_markup=get_main_menu()
    )


def handle_home(bot, user_id):
    """Show home menu"""
    bot.send_message(
        user_id,
        "Добро пожаловать обратно 👋",
        reply_markup=get_home_buttons()
    )


def handle_add_post_command(bot, user_id):
    """Handle /addpost command"""
    
    # Check if registered
    if not functions.user_exists(user_id):
        bot.send_message(
            user_id,
            "❌ Сначала нужно зарегистрироваться. Используй команду /start 👇"
        )
        return
    
    user_state.set_state(user_id, user_state.States.ADDING_POST)
    bot.send_message(
        user_id,
        ADD_POST_MESSAGE,
        reply_markup=types.ReplyKeyboardRemove()
    )


def handle_profile_command(bot, user_id):
    """Handle profile command"""
    
    # Check if registered
    if not functions.user_exists(user_id):
        bot.send_message(
            user_id,
            "❌ Сначала нужно зарегистрироваться. Используй команду /start 👇"
        )
        return
    
    nickname = functions.get_user_nickname(user_id)
    posts_count = functions.get_user_posts_count(user_id)
    likes_count = functions.get_user_likes_count(user_id)
    
    from buttons import get_profile_buttons
    
    bot.send_message(
        user_id,
        PROFILE_MESSAGE.format(nickname, posts_count, likes_count),
        parse_mode='HTML'
    )


def handle_my_posts_command(bot, user_id):
    """Handle my posts command"""
    
    # Check if registered
    if not functions.user_exists(user_id):
        bot.send_message(
            user_id,
            "❌ You need to register first. Use /start"
        )
        return
    
    from posts import get_user_posts, format_post_text
    from buttons import get_post_buttons
    
    posts = get_user_posts(user_id)
    
    if not posts:
        bot.send_message(
            user_id,
            MY_POSTS_EMPTY,
            reply_markup=get_main_menu()
        )
        return
    
    # Show first post
    post = posts[0]
    user_state.set_data(user_id, "my_posts", posts)
    user_state.set_data(user_id, "my_posts_index", 0)
    
    text = format_post_text(post, show_nickname=False)
    
    bot.send_message(
        user_id,
        text,
        parse_mode='HTML',
        reply_markup=get_post_buttons(post["post_id"], is_owner=True)
    )
