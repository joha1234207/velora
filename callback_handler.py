# Callback query handlers for inline button clicks

from telebot import types
import config
import user_state
import functions
from posts import (
    get_random_post, format_post_text, get_post_by_id, get_post_reactions,
    get_user_reaction, toggle_reaction, delete_post, report_post,
    get_user_posts, get_reported_posts
)
from buttons import (
    get_post_buttons, get_main_menu, get_profile_buttons,
    get_admin_panel_buttons, get_admin_reported_buttons
)
from config import *


def register_callback_handlers(bot):
    """Register all callback query handlers"""
    
    # ===== HOME AND NAVIGATION =====
    @bot.callback_query_handler(func=lambda call: call.data == "back_to_home")
    def callback_back_to_home(call):
        """Go back to home"""
        user_id = call.from_user.id
        user_state.clear_all(user_id)
        
        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text="🏠 Добро пожаловать в Velora",
            reply_markup=get_main_menu()
        )
    
    
    # ===== RANDOM POSTS =====
    
    @bot.callback_query_handler(func=lambda call: call.data == "view_random_post")
    def callback_view_random_post(call):
        """Show random post"""
        user_id = call.from_user.id
        
        # Get random post
        post = get_random_post(exclude_user_id=user_id)
        bot.answer_callback_query(call.id)
        if not post:
            bot.edit_message_text(
                chat_id=user_id,
                message_id=call.message.message_id,
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
        
        bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=text,
            parse_mode='HTML',
            reply_markup=get_post_buttons(post["post_id"], is_owner=False)
        )
    
    
    @bot.callback_query_handler(func=lambda call: call.data == "next_post")
    def callback_next_post(call):
        """Show next post"""
        user_id = call.from_user.id
        
        # Check if viewing my posts or random posts
        my_posts = user_state.get_data(user_id, "my_posts")
        
        if my_posts:
            # Viewing own posts
            current_index = user_state.get_data(user_id, "my_posts_index") or 0
            next_index = current_index + 1
            
            if next_index >= len(my_posts):
                bot.answer_callback_query(
                    call.id,
                    "No more posts",
                    show_alert=False
                )
                return
            
            post = my_posts[next_index]
            user_state.set_data(user_id, "my_posts_index", next_index)
            
            text = format_post_text(post, show_nickname=False)
            
            bot.edit_message_text(
                chat_id=user_id,
                message_id=call.message.message_id,
                text=text,
                parse_mode='HTML',
                reply_markup=get_post_buttons(post["post_id"], is_owner=True)
            )
        else:
            # Viewing random posts - just get another random
            callback_view_random_post(call)
    
    
    # ===== REACTIONS (LIKE/DISLIKE) =====
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("like_post_"))
    def callback_like_post(call):
        """Like a post"""
        user_id = call.from_user.id
        post_id = int(call.data.split("_")[2])
        
        bot.answer_callback_query(call.id)
        # Toggle like
        result = toggle_reaction(user_id, post_id, "like")
        
        # Get updated reactions
        reactions = get_post_reactions(post_id)
        
        # Get current message text
        post = get_post_by_id(post_id)
        text = format_post_text(post)
        text += f"\n\n👍 {reactions['likes']} | 👎 {reactions['dislikes']}"
        
        bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=text,
            parse_mode='HTML',
            reply_markup=get_post_buttons(post_id, is_owner=False)
        )
        
        # Show feedback
        if result == "added":
            bot.answer_callback_query(call.id, "👍 Liked!", show_alert=False)
        elif result == "removed":
            bot.answer_callback_query(call.id, "👍 Like removed", show_alert=False)
        else:
            bot.answer_callback_query(call.id, "Changed to like", show_alert=False)
    
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("dislike_post_"))
    def callback_dislike_post(call):
        """Dislike a post"""
        user_id = call.from_user.id
        post_id = int(call.data.split("_")[2])
        bot.answer_callback_query(call.id)
        
        # Toggle dislike
        result = toggle_reaction(user_id, post_id, "dislike")
        
        # Get updated reactions
        reactions = get_post_reactions(post_id)
        
        # Get current message text
        post = get_post_by_id(post_id)
        text = format_post_text(post)
        text += f"\n\n👍 {reactions['likes']} | 👎 {reactions['dislikes']}"
        
        bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=text,
            parse_mode='HTML',
            reply_markup=get_post_buttons(post_id, is_owner=False)
        )
        
        # Show feedback
        if result == "added":
            bot.answer_callback_query(call.id, "👎 Disliked", show_alert=False)
        elif result == "removed":
            bot.answer_callback_query(call.id, "👎 Dislike removed", show_alert=False)
        else:
            bot.answer_callback_query(call.id, "Changed to dislike", show_alert=False)
    
    
    # ===== SHARING POSTS =====
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("share_post_"))
    def callback_share_post(call):
        """Share post with deep link"""
        user_id = call.from_user.id
        post_id = int(call.data.split("_")[2])
        
        # Create deep link
        bot_username = bot.get_me().username
        deep_link = f"https://t.me/{bot_username}?start=post_{post_id}"
        
        share_text = f"""
🔗 <b>Поделиться этим постом</b>

{deep_link}

Нажмите, чтобы посмотреть этот пост!
"""
        
        bot.send_message(
            user_id,
            share_text,
            parse_mode='HTML'
        )
        
        bot.answer_callback_query(call.id, "Link copied!", show_alert=False)
    
    
    # ===== DELETING POSTS =====
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("delete_post_"))
    def callback_delete_post(call):
        """Delete user's own post"""
        user_id = call.from_user.id
        post_id = int(call.data.split("_")[2])
        
        # Verify ownership
        post = get_post_by_id(post_id)
        if not post or post["user_id"] != user_id:
            bot.answer_callback_query(call.id, "❌ This is not your post", show_alert=True)
            return
        
        # Delete
        if delete_post(post_id):
            bot.edit_message_text(
                chat_id=user_id,
                message_id=call.message.message_id,
                text=POST_DELETED_USER
            )
        else:
            bot.answer_callback_query(call.id, "Error deleting post", show_alert=True)
    
    
    # ===== REPORTING POSTS =====
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("report_post_"))
    def callback_report_post(call):
        """Report a post as spam"""
        user_id = call.from_user.id
        post_id = int(call.data.split("_")[2])
        
        # Report
        if report_post(post_id):
            bot.edit_message_text(
                chat_id=user_id,
                message_id=call.message.message_id,
                text=POST_REPORTED
            )
            
            # Notify admin
            admin_text = f"⚠️ <b>Post Reported</b>\n\nPost ID: {post_id}"
            try:
                bot.send_message(config.ADMIN_ID, admin_text, parse_mode='HTML')
            except:
                pass
        else:
            bot.answer_callback_query(call.id, "Error reporting post", show_alert=True)
    
    
    # ===== PROFILE =====
    
    @bot.callback_query_handler(func=lambda call: call.data == "profile_button")
    def callback_profile_button(call):
        """Show profile button"""
        from message_handler import handle_profile_command
        handle_profile_command(bot, call.from_user.id)
        bot.answer_callback_query(call.id)
    
    
    @bot.callback_query_handler(func=lambda call: call.data == "view_my_posts")
    def callback_view_my_posts(call):
        """View user's own posts"""
        user_id = call.from_user.id
        bot.answer_callback_query(call.id)
        posts = get_user_posts(user_id)
        
        if not posts:
            bot.edit_message_text(
                chat_id=user_id,
                message_id=call.message.message_id,
                text=MY_POSTS_EMPTY
            )
            return
        
        # Show first post
        post = posts[0]
        user_state.set_data(user_id, "my_posts", posts)
        user_state.set_data(user_id, "my_posts_index", 0)
        
        text = format_post_text(post, show_nickname=False)
        
        bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=text,
            parse_mode='HTML',
            reply_markup=get_post_buttons(post["post_id"], is_owner=True)
        )
    
    
    @bot.callback_query_handler(func=lambda call: call.data == "view_stats")
    def callback_view_stats(call):
        """View user stats"""
        user_id = call.from_user.id
        bot.answer_callback_query(call.id)
        nickname = functions.get_user_nickname(user_id)
        posts_count = functions.get_user_posts_count(user_id)
        likes_count = functions.get_user_likes_count(user_id)
        
        text = PROFILE_MESSAGE.format(nickname, posts_count, likes_count)
        
        bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=text,
            parse_mode='HTML'
        )
    
    
    # ===== ADD POST BUTTONS =====
    
    @bot.callback_query_handler(func=lambda call: call.data == "add_post_button")
    def callback_add_post_button(call):
        """Add post button"""
        from message_handler import handle_add_post_command
        handle_add_post_command(bot, call.from_user.id)
        bot.answer_callback_query(call.id)
    
    
    @bot.callback_query_handler(func=lambda call: call.data == "my_posts_button")
    def callback_my_posts_button(call):
        """My posts button"""
        from message_handler import handle_my_posts_command
        handle_my_posts_command(bot, call.from_user.id)
        bot.answer_callback_query(call.id)
    
    
    # ===== ADMIN PANEL =====
    
    @bot.callback_query_handler(func=lambda call: call.data == "admin_stats")
    def callback_admin_stats(call):
        """Show admin statistics"""
        user_id = call.from_user.id
        
        if user_id != config.ADMIN_ID:
            bot.answer_callback_query(call.id, "❌ Permission denied", show_alert=True)
            return
        
        total_users = functions.get_total_users()
        total_posts = functions.get_total_posts()
        total_reported = functions.get_total_reported_posts()
        
        text = f"""
<b>📊 Bot Statistics</b>

👥 Total Users: {total_users}
📝 Total Posts: {total_posts}
🚨 Reported Posts: {total_reported}
"""
        
        bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=text,
            parse_mode='HTML',
            reply_markup=get_admin_panel_buttons()
        )
    
    
    @bot.callback_query_handler(func=lambda call: call.data == "admin_broadcast")
    def callback_admin_broadcast(call):
        """Start broadcast"""
        user_id = call.from_user.id
        
        if user_id != config.ADMIN_ID:
            bot.answer_callback_query(call.id, "❌ Permission denied", show_alert=True)
            return
        
        total_users = functions.get_total_users()
        
        user_state.set_state(user_id, user_state.States.BROADCASTING)
        
        bot.send_message(
            user_id,
            BROADCAST_MESSAGE.format(total_users),
            parse_mode='HTML'
        )
    
    
    @bot.callback_query_handler(func=lambda call: call.data == "admin_reported")
    def callback_admin_reported(call):
        """View reported posts"""
        user_id = call.from_user.id
        
        if user_id != config.ADMIN_ID:
            bot.answer_callback_query(call.id, "❌ Permission denied", show_alert=True)
            return
        
        reported = get_reported_posts()
        
        if not reported:
            bot.edit_message_text(
                chat_id=user_id,
                message_id=call.message.message_id,
                text="✅ No reported posts!"
            )
            return
        
        # Show first reported post
        post = reported[0]
        user_state.set_data(user_id, "reported_posts", reported)
        user_state.set_data(user_id, "reported_index", 0)
        
        text = f"""
<b>🚨 Reported Post</b>

{post['content']}

👤 By: @{post['nickname']}
"""
        
        bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=text,
            parse_mode='HTML',
            reply_markup=get_admin_reported_buttons(post["post_id"])
        )
    
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("admin_delete_"))
    def callback_admin_delete(call):
        """Admin delete post"""
        user_id = call.from_user.id
        post_id = int(call.data.split("_")[2])
        
        if user_id != config.ADMIN_ID:
            bot.answer_callback_query(call.id, "❌ Permission denied", show_alert=True)
            return
        
        if delete_post(post_id):
            # Get next reported post
            reported = user_state.get_data(user_id, "reported_posts")
            current_index = user_state.get_data(user_id, "reported_index") or 0
            next_index = current_index + 1
            
            if reported and next_index < len(reported):
                post = reported[next_index]
                user_state.set_data(user_id, "reported_index", next_index)
                
                text = f"""
<b>🚨 Reported Post</b>

{post['content']}

👤 By: @{post['nickname']}
"""
                
                bot.edit_message_text(
                    chat_id=user_id,
                    message_id=call.message.message_id,
                    text=text,
                    parse_mode='HTML',
                    reply_markup=get_admin_reported_buttons(post["post_id"])
                )
            else:
                bot.edit_message_text(
                    chat_id=user_id,
                    message_id=call.message.message_id,
                    text=POST_DELETED_ADMIN
                )
    
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("admin_keep_"))
    def callback_admin_keep(call):
        """Admin keep post (mark as not reported)"""
        user_id = call.from_user.id
        post_id = int(call.data.split("_")[2])
        
        if user_id != config.ADMIN_ID:
            bot.answer_callback_query(call.id, "❌ Permission denied", show_alert=True)
            return
        
        # Un-report the post
        import sqlite3
        conn = sqlite3.connect(config.DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("UPDATE posts SET is_reported = 0 WHERE post_id = ?", (post_id,))
        conn.commit()
        conn.close()
        
        # Get next reported post
        reported = user_state.get_data(user_id, "reported_posts")
        current_index = user_state.get_data(user_id, "reported_index") or 0
        next_index = current_index + 1
        
        if reported and next_index < len(reported):
            post = reported[next_index]
            user_state.set_data(user_id, "reported_index", next_index)
            
            text = f"""
<b>🚨 Reported Post</b>

{post['content']}

👤 By: @{post['nickname']}
"""
            
            bot.edit_message_text(
                chat_id=user_id,
                message_id=call.message.message_id,
                text=text,
                parse_mode='HTML',
                reply_markup=get_admin_reported_buttons(post["post_id"])
            )
        else:
            bot.edit_message_text(
                chat_id=user_id,
                message_id=call.message.message_id,
                text="✅ Post kept. No more reports!"
            )
    
    
    @bot.callback_query_handler(func=lambda call: call.data == "next_report")
    def callback_next_report(call):
        """Show next reported post"""
        user_id = call.from_user.id
        
        reported = user_state.get_data(user_id, "reported_posts")
        current_index = user_state.get_data(user_id, "reported_index") or 0
        next_index = current_index + 1
        
        if not reported or next_index >= len(reported):
            bot.answer_callback_query(call.id, "No more reports", show_alert=False)
            return
        
        post = reported[next_index]
        user_state.set_data(user_id, "reported_index", next_index)
        
        text = f"""
<b>🚨 Reported Post</b>

{post['content']}

👤 By: @{post['nickname']}
"""
        
        bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=text,
            parse_mode='HTML',
            reply_markup=get_admin_reported_buttons(post["post_id"])
        )
    @bot.callback_query_handler(func=lambda call: True)
    def stop_effekt(call):
        bot.answer_callback_query(call.id)