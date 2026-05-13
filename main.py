from flask import Flask, request
import telebot
import os

from config import BOT_TOKEN, WEBHOOK_URL

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Handlers
from commands_handler import register_command_handlers
register_command_handlers(bot)

from message_handler import register_message_handlers
register_message_handlers(bot)

from callback_handler import register_callback_handlers
register_callback_handlers(bot)


# Webhook
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])

    return "ok", 200


# Home page
@app.route("/")
def home():
    return "Bot is running"


# Start server
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")

    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 10000))
    )
