import os
from datetime import datetime
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
    CommandHandler,
)
import threading

# --- Настройки ---
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID", "0"))

# --- Flask app для Render healthcheck ---
flask_app = Flask(__name__)

@flask_app.route("/healthz")
def health():
    return "OK", 200

# --- Telegram бот ---
message_count = 0
lock = threading.Lock()  # защита от многопоточности

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот активен. Я считаю сообщения 🧮")

async def count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global message_count
    with lock:
        message_count += 1

async def report(context: ContextTypes.DEFAULT_TYPE):
    global message_count
    with lock:
        count = message_count
        message_count = 0
    date = datetime.now().strftime("%Y-%m-%d")
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text=f"📊 {date}: получено {count} сообщений за день.",
    )

# --- Основной запуск ---
async def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, count))

    # Планировщик отчётов — каждые сутки в 21:00 (по UTC)
    application.job_queue.run_daily(report, time=datetime.utcnow().replace(hour=21, minute=0, second=0))

    await application.run_polling()

# --- Запуск Flask и Telegram параллельно ---
if __name__ == "__main__":
    import asyncio
    import threading

    telegram_thread = threading.Thread(target=lambda: asyncio.run(main()))
    telegram_thread.start()

    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
