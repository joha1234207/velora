from flask import Flask, request
import telebot
import os

from config import BOT_TOKEN, WEBHOOK_URL

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Handlers
from commands_handler import register_command_handlers
from message_handler import register_message_handlers
from callback_handler import register_callback_handlers

register_command_handlers(bot)
register_message_handlers(bot)
register_callback_handlers(bot)


# ========================
# WEBHOOK ROUTE
# ========================
@app.route("/webhook", methods=["POST"])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_str = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
    return "OK", 200


# ========================
# HOME ROUTE (optional)
# ========================
@app.route("/")
def home():
    return "Bot is running 🚀"


# ========================
# START SERVER
# ========================
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")

    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8080))
    )
