import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# 🔑 Данные бота из переменных окружения (Render → Environment)
TOKEN = os.environ["TOKEN"]
OWNER_ID = int(os.environ["OWNER_ID"])

WELCOME_TEXT = """
🍀 Привет~
Это предложка Дуни.  

Нажмите кнопку «Предложить» и отправьте сообщение чтобы:
1. Предложить новость 
2. Добавить развернутый комментарий/дополнение к уже существующей новости

‼️ Сообщения анонимны, я не вижу ваш ник. Если хотите, чтобы я указала вас как автора предложения — пишите ник текстом ‼️

💞 Любые поступающие сюда сообщения могут быть использованы в телеграм-канале и/или в моих видео.  
✨ Я рассчитываю на ваше понимание, если новость не была опубликована. Я должна оценивать и публиковать то, что является релевантным и уместным в интересах своего блога, спасибо!
"""

# 🔹 Старт — показывает приветственное сообщение с кнопкой
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Предложить", callback_data="send_message")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(WELCOME_TEXT, reply_markup=reply_markup)

# 🔹 Обработка нажатия на кнопку
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("Отправьте ваше предложение ниже 👇")

# 🔹 Обработка любого текста от пользователя
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text("Спасибо за предложение 💞 Надеюсь ваш день проходит хорошо")
    await context.bot.send_message(
        chat_id=OWNER_ID,
        text=f"📩 Новое предложение:\n\n{user_message}",
    )

# 🔹 Запуск приложения
from telegram.ext import ApplicationBuilder

def main():
    app = ApplicationBuilder().token(TOKEN).build()  # <-- исправлено

    # Регистрируем хендлеры
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler, pattern="send_message"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Бот запущен и слушает сообщения...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
