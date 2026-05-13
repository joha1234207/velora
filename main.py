import telebot
from flask import Flask, request

from config import BOT_TOKEN, WEBHOOK_URL

# Bot
bot = telebot.TeleBot(BOT_TOKEN)

# Flask
app = Flask(__name__)

# Handlers
from commands_handler import register_command_handlers
register_command_handlers(bot)

from message_handler import register_message_handlers
register_message_handlers(bot)

from callback_handler import register_callback_handlers
register_callback_handlers(bot)


# Home
@app.route("/", methods=["GET"])
def home():
    return "Bot ishlayapti"


# Webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)

    bot.process_new_updates([update])

    return "ok", 200


# Start
if __name__ == "__main__":
    bot.remove_webhook()

    bot.set_webhook(
        url=f"{WEBHOOK_URL}/webhook"
    )

    app.run(
        host="0.0.0.0",
        port=10000
    )
