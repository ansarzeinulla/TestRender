import asyncio
import threading
from datetime import datetime
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# === Настройки ===
TOKEN = "7979735611:AAEaLiilXvzzKucfxEghYAf_VNZNvmAJzdI"
CHAT_ID = 1154455614
message_count = 0
lock = threading.Lock()

# === Flask app для Render ===
flask_app = Flask(__name__)

@flask_app.route("/healthz")
def health():
    return "OK", 200

def run_flask():
    flask_app.run(host="0.0.0.0", port=5050)

# === Логика Telegram-бота ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHAT_ID
    CHAT_ID = update.effective_chat.id
    await update.message.reply_text("Бот запущен! 🟢")

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

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, count))

    # Планирование ежедневного отчёта
    app.job_queue.run_daily(
        report,
        time=datetime.utcnow().replace(hour=21, minute=0, second=0)
    )

    await app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    asyncio.run(main())
