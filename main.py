# Main bot file - Telegram Anonymous Posts Platform
# Using pyTelegramBotAPI (telebot) - NO aiogram, NO asyncio, NO FSM

import telebot
from config import BOT_TOKEN

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

# Register all handlers
print("📝 Registering handlers...")

# Import and register command handlers
from commands_handler import register_command_handlers
register_command_handlers(bot)

# Import and register message handlers
from message_handler import register_message_handlers
register_message_handlers(bot)

# Import and register callback handlers
from callback_handler import register_callback_handlers
register_callback_handlers(bot)

print("✅ All handlers registered!")

# Display bot information
try:
    me = bot.get_me()
    print("\n🤖 Bot Information:")
    print(f"   Name: {me.first_name}")
    print(f"   Username: @{me.username}")
    print(f"   ID: {me.id}")
except Exception as e:
    print(f"⚠️  Warning: Could not fetch bot info: {e}")

print("🚀 Bot is starting polling...\n")

# Start polling
if __name__ == "__main__":
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        print("\n⛔ Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Restarting in 5 seconds...")
        import time
        time.sleep(5)
