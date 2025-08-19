from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# Твой токен и ID автора (тебя)
TOKEN = "7800572322:AAFZmkwK_kXnhey1oZk289dQLv0s2uQOgyw"
AUTHOR_ID = 1446412573  # поставь свой Telegram ID

# Приветственное сообщение
WELCOME_TEXT = "Приветственное сообщение"
SUGGEST_TEXT = "Предложите новость"

# Старт команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Предложить", callback_data="suggest")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(WELCOME_TEXT, reply_markup=reply_markup)

# Нажатие кнопки
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "suggest":
        await query.message.reply_text(SUGGEST_TEXT)
        return

# Получение предложения
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    # Ответ пользователю
    await update.message.reply_text("Спасибо за предложение")
    # Отправка автору
    await context.bot.send_message(chat_id=AUTHOR_ID, text=f"Новое предложение: {text}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    app.run_polling()

if __name__ == "__main__":
    main()
