import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = "YOUR_TOKEN"

async def start(update, context):
    await update.message.reply_text("Привет! Бот снова на связи!")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
