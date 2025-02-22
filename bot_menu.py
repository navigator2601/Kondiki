from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters, CallbackContext
import logging
import os
import psycopg2
from flask import Flask, request

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levellevelname)s - %(message)s',
                    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()])
logger = logging.getLogger(__name__)

# Створення Flask додатку
app = Flask(__name__)

# Підключення до бази даних Neon.tech
def connect_db():
    conn = psycopg2.connect(
        dsn="postgresql://neondb_owner:npg_dhwrDX6O1keB@ep-round-star-a9r38wl3-pooler.gwc.azure.neon.tech/neondb"
    )
    return conn

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
                [InlineKeyboardButton("❄️ Фреони", callback_data='freons')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("ℹ️ Інформація:", reply_markup=reply_markup)

# Отримання списку марок кондиціонерів з бази даних
def get_brands(update: Update, context: CallbackContext) -> None:
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT name FROM cond_brand")
    brands_list = "\n".join([f"✅ {row[0]}" for row in cur.fetchall()])
    conn.close()
    update.callback_query.message.reply_text(f"📋 **Марки кондиціонерів:**\n{brands_list}", parse_mode="Markdown")

# Отримання типів фреонів з бази даних
def get_freons(update: Update, context: CallbackContext) -> None:
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT name, chemical_name FROM freons")
    freon_list = "\n".join([f"❄️ {row[0]} – {row[1]}" for row in cur.fetchall()])
    conn.close()
    update.callback_query.message.reply_text(f"❄️ **Типи фреонів:**\n{freon_list}", parse_mode="Markdown")

# Обробка натискання кнопок
def button_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'brands':
        get_brands(update, context)
    elif query.data == 'freons':
        get_freons(update, context)
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
    updater = Updater(token="8177185933:AAGvnm0JmuTxucr8VqU0nzGd4WrNkn5VHpU", use_context=True)

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