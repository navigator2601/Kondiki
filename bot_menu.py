from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters, CallbackContext
import logging
import os
from flask import Flask, request

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levellevelname)s - %(message)s',
                    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()])
logger = logging.getLogger(__name__)

# Створення Flask додатку
app = Flask(__name__)

# Головне меню
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [['ℹ️ Інформація', '⚙️ Налаштування'],
                ['📞 Підтримка', '🔙 Назад'],
                ['Просто велика кнопка']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("Чіназес! Просто імбово що ти підключився. Будемо чілитися разом", reply_markup=reply_markup)

# Меню "ℹ️ Інформація"
def info(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton("📋 Марки кондиціонерів", callback_data='brands')],
                [InlineKeyboardButton("❄️ Типи фреонів", callback_data='freon')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("ℹ️ Інформація:", reply_markup=reply_markup)

# Отримання списку марок кондиціонерів (без запиту до БД)
def get_brands(update: Update, context: CallbackContext) -> None:
    brands_list = "\n".join(["✅ Brand1", "✅ Brand2", "✅ Brand3"])
    update.callback_query.message.reply_text(f"📋 **Марки кондиціонерів:**\n{brands_list}", parse_mode="Markdown")

# Отримання типів фреонів (без запиту до БД)
def get_freon(update: Update, context: CallbackContext) -> None:
    freon_list = "\n".join(["❄️ Freon1 – Chemical1", "❄️ Freon2 – Chemical2", "❄️ Freon3 – Chemical3"])
    update.callback_query.message.reply_text(f"❄️ **Типи фреонів:**\n{freon_list}", parse_mode="Markdown")

# Обробка натискання кнопок
def button_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'brands':
        get_brands(update, context)
    elif query.data == 'freon':
        get_freon(update, context)
    elif query.data == 'back':
        start(update, context)

# Обробка повідомлень
def message_handler(update: Update, context: CallbackContext) -> None:
    text = update.message.text

    if text == "ℹ️ Інформація":
        info(update, context)
    elif text == "⚙️ Налаштування":
        update.message.reply_text("⚙️ Тут колись плануються налаштування.")
    elif text == "📞 Підтримка":
        update.message.reply_text("📞 Ну може колись і підтримаємо, але зараз все в режимі розробки")
    elif text == "🔙 Назад":
        start(update, context)
    elif text == "Просто велика кнопка":
        update.message.reply_text("Якщо вона велика, то це не означає що її нада тицяти. Пон?")

# Головна функція
def main():
    updater = Updater(token=os.getenv("TELEGRAM_BOT_TOKEN"), use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button_callback))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))

    logger.info("✅ Бот запущено...")
    updater.start_polling()
    updater.idle()

@app.route('/')
def index():
    return "Telegram Bot is running."

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        update = Update.de_json(request.get_json(force=True), updater.bot)
        dispatcher.process_update(update)
        return 'ok', 200

if __name__ == '__main__':
    main()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8080)))