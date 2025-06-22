import nest_asyncio
nest_asyncio.apply()

import asyncio
from datetime import datetime, time
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import threading
import os

# --- Настройки ---
TOKEN = "7979735611:AAEaLiilXvzzKucfxEghYAf_VNZNvmAJzdI"
CHAT_ID = 1154455614  # <-- Твой chat_id


flask_app = Flask(__name__)

@flask_app.route("/")
def health():
    return "OK", 200

def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5050)))

# --- Telegram логика ---
message_count = 0
lock = threading.Lock()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот активен. Я считаю сообщения 🧮")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global message_count
    with lock:
        message_count += 1

async def report(context: ContextTypes.DEFAULT_TYPE):
    global message_count
    now = datetime.utcnow().strftime("%Y-%m-%d")
    report_text = f"📊 {now}: получено {message_count} сообщений за день."
    await context.bot.send_message(chat_id=CHAT_ID, text=report_text)
    message_count = 0  # reset for next day

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.job_queue.run_daily(
        report,
        time=time(hour=21, minute=0)  # 21:00 UTC
    )

    await app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    asyncio.run(main())
