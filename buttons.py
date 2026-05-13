# Buttons and keyboard layouts for the Telegram bot

from telebot import types
from config import NICKNAME_MIN_LENGTH, NICKNAME_MAX_LENGTH


# Main menu buttons
def get_main_menu():
    """Returns main menu keyboard"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
    	types.KeyboardButton("🏠 Главная"),
    	types.KeyboardButton("👤 Профил")
    )
    markup.add(types.KeyboardButton("📝 Добавить пост"),
    types.KeyboardButton("📖 Мои посты")
    )
    
    markup.add(types.KeyboardButton("🔍 Рандом пост"))
    return markup


# Other users' posts inline buttons
def get_post_buttons(post_id, is_owner=False):
    """
    Returns buttons for posts
    
    Args:
        post_id: ID of the post
        is_owner: True if user owns the post
    
    Returns:
        InlineKeyboardMarkup with appropriate buttons
    """
    markup = types.InlineKeyboardMarkup()
    
    if is_owner:
        # Owner buttons: Delete and Share
        markup.add(
            types.InlineKeyboardButton("🗑 Удалить", callback_data=f"delete_post_{post_id}"),
            types.InlineKeyboardButton("📤 Поделится", callback_data=f"share_post_{post_id}")
        )
    else:
        # Other users' posts: Like, Dislike, Report, Share
        markup.add(
            types.InlineKeyboardButton("👍 Like", callback_data=f"like_post_{post_id}"),
            types.InlineKeyboardButton("👎 Dislike", callback_data=f"dislike_post_{post_id}")
        )
        markup.add(
            types.InlineKeyboardButton("🚨 Spam", callback_data=f"report_post_{post_id}"),
            types.InlineKeyboardButton("📤 Поделится", callback_data=f"share_post_{post_id}")
        )
    
    # Next button for all posts
    markup.add(
        types.InlineKeyboardButton("➡️ Next", callback_data="next_post")
    )
    
    return markup


# Profile buttons
def get_profile_buttons():
    """Returns profile menu buttons"""
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("📖 Мои посты", callback_data="view_my_posts"),
        types.InlineKeyboardButton("❤️ Статистика", callback_data="view_stats")
    )
    markup.add(
        types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_home")
    )
    return markup


# Home buttons
def get_home_buttons():
    """Returns home menu buttons"""
    markup = types.InlineKeyboardMarkup()
    
    
    markup.add(
        types.InlineKeyboardButton("👤 Профил", callback_data="profile_button"),
        types.InlineKeyboardButton("📖 Мои посты", callback_data="my_posts_button")
        )
     
           
    markup.add(
        types.InlineKeyboardButton("🔍 Рандом пост", callback_data="view_random_post")
    )
    return markup


# Admin panel buttons
def get_admin_panel_buttons():
    """Returns admin panel buttons"""
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("📊 Statistiks", callback_data="admin_stats"),
        types.InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")
    )
    markup.add(
        types.InlineKeyboardButton("🗑 Reported Posts", callback_data="admin_reported"),
        types.InlineKeyboardButton("🔙 Back", callback_data="back_to_home")
    )
    return markup


# Reported posts admin view
def get_admin_reported_buttons(post_id):
    """Returns buttons for viewing reported posts in admin panel"""
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🗑 Delete", callback_data=f"admin_delete_{post_id}"),
        types.InlineKeyboardButton("✅ Keep", callback_data=f"admin_keep_{post_id}")
    )
    markup.add(
        types.InlineKeyboardButton("➡️ Next Report", callback_data="next_report")
    )
    return markup


# Confirmation buttons
def get_confirm_buttons(action_id):
    """Returns yes/no confirmation buttons"""
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ Yes", callback_data=f"confirm_{action_id}"),
        types.InlineKeyboardButton("❌ No", callback_data=f"cancel_{action_id}")
    )
    return markup


# Back button
def get_back_button():
    """Returns a simple back button"""
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_home")
    )
    return markup


# Registration keyboard
def get_registration_keyboard():
    """Returns keyboard for registration prompt"""
    markup = types.ReplyKeyboardRemove()
    return markup
