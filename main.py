from flask import Flask, request
import telebot
from config import BOT_TOKEN, WEBHOOK_URL

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

from commands_handler import register_command_handlers
register_command_handlers(bot)

from message_handler import register_message_handlers
register_message_handlers(bot)

from callback_handler import register_callback_handlers
register_callback_handlers(bot)

bot.remove_webhook()
bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")


@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "ok", 200


@app.route("/")
def home():
    return "Bot is running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
