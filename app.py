import nest_asyncio
nest_asyncio.apply()

import asyncio
from datetime import datetime
from flask import Flask
from telegram import Update, CommandHandler
import threading
import os

# --- Настройки ---
TOKEN = "7979735611:AAEaLiilXvzzKucfxEghYAf_VNZNvmAJzdI"
CHAT_ID = 1154455614  # <-- Твой chat_id

# --- Flask app для Render healthcheck ---
flask_app = Flask(__name__)

def health():
    return "OK", 200

def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5050)))

# --- Telegram логика ---
message_count = 0
lock = threading.Lock()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот активен. Я считаю сообщения 🧮")
    async def report(context: ContextTypes.DEFAULT_TYPE):
        text=f"📊 {date}: получено {count} сообщений за день.",
    )


async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, count))
    app.job_queue.run_daily(
        report,
        time=datetime.utcnow().replace(hour=21, minute=0, second=0)
    )

    await app.run_polling()


if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    asyncio.run(main())
