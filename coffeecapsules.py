import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode

# ---------- Flask keep-alive ----------
flask_app = Flask(__name__)

@flask_app.route("/")
def health():
    return "I'm alive", 200

def start_flask():
    # Replit обычно ожидает порт 8080
    flask_app.run(host="0.0.0.0", port=8080)

# ---------- Telegram bot ----------
# Список капсул с описанием и фото
capsules = {
    "Buenos Aires 🌰 [===4=========]": {
        "grade": "Горчинка: ■ □ □ □ □\nПлотность: ■ □ □ □ □\nКислинка: ■ ■ □ □ □\nОбжарка: ■ □ □ □ □\n",
        "desc": "Купаж с ореховыми зерновыми нотками, обильной сладостью.",
        "photo": "https://drive.google.com/uc?export=view&id=1WMdLT2_dNsdfcSut7tikq18JRYBWasxT"
    },
    "Chiaro 🍬 [====5========]": {
        "grade": "Горчинка: ■ □ □ □ □\nПлотность: ■ ■ ■ ■ □\nКислинка: ■ ■ ■ ■ □\nОбжарка: ■ □ □ □ □\n",
        "desc": "Ноты карамели и сладкого бисквита в сочетании с молоком.",
        "photo": "https://drive.google.com/uc?export=view&id=1e6qt5OEvJQxZhEYuL6XA9t0tkD_IRWtb"
    },
    "Paris Black 🍋🌰 [=====6=======]": {
        "grade": "Горчинка: ■ ■ ■ □ □\nПлотность: ■ ■ ■ □ □\nКислинка: ■ ■ □ □ □\nОбжарка: ■ ■ ■ □ □\n",
        "desc": "Зерновые нотки печенья и приятная кислинка с оттенком цитрусовых.",
        "photo": "https://drive.google.com/uc?export=view&id=1tvOLH5pFLaZ4Sw9kYDSFv8x9p5fUkezL"
    },
    "Peru Organic 🍇🌾 [=====6=======]": {
        "grade": "Горчинка: ■ ■ ■ □ □\nПлотность: ■ ■ ■ □ □\nКислинка: ■ ■ ■ ■ □\nОбжарка: ■ ■ ■ □ □\n",
        "desc": "Фруктовые ноты, обжаренные злаки.",
        "photo": "https://drive.google.com/uc?export=view&id=1I7nfTzpypCHMjInV55AUplMOyUCBY72J"
    },
    "Tokyo Lungo 🌸🍇 [=====6=======]": {
        "grade": "Горчинка: ■ ■ □ □ □\nПлотность: ■ ■ ■ □ □\nКислинка: ■ □ □ □ □\nОбжарка: ■ ■ ■ ■ □\n",
        "desc": "Нежные цветочные и фруктовые ноты.",
        "photo": "https://drive.google.com/uc?export=view&id=1ps5_SXrJZsWI7HccgrDjk0cDQNUaKE8r"
    },
    "Zambia 🥭🌸 [======7======]": {
        "grade": "Горчинка: ■ □ □ □ □\nПлотность: ■ ■ ■ □ □\nКислинка: ■ ■ ■ ■ □\nОбжарка: ■ ■ ■ □ □\n",
        "desc": "Ноты экзотических фруктов и цветов.",
        "photo": "https://drive.google.com/uc?export=view&id=1x1zoEGCS35lfq9Mp52TEqINQsvSxknbT"
    },
    "Cadiz 🍫🍯 [=======8=====]": {
        "grade": "Горчинка: ■ ■ ■ □ □\nПлотность: ■ ■ ■ ■ □\nКислинка: ■ ■ □ □ □\nОбжарка: ■ ■ ■ □ □\n",
        "desc": "Ноты солода, какао и карамели.",
        "photo": "https://drive.google.com/uc?export=view&id=1wY_5COObBp3tramofsmiUA3Sl8oToiZw"
    },
    "Rio De Janeiro 🌰🌿 [========9====]": {
        "grade": "Горчинка: ■ ■ ■ ■ □\nПлотность: ■ ■ ■ ■ □\nКислинка: ■ □ □ □ □\nОбжарка: ■ ■ ■ ■ □\n",
        "desc": "Приятная горчинка с нотами грецкого ореха, сандала и трав.",
        "photo": "https://drive.google.com/uc?export=view&id=1nDDWCeF6Yn8EQfVf3O0ctoTZVYEvB7LR"
    },
}

# стартовое сообщение
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот кофейных капсул ☕.")
    keyboard = [[InlineKeyboardButton("📋 Показать список капсул", callback_data="show_capsules")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Нажми кнопку ниже:", reply_markup=reply_markup)

# обработчик кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "show_capsules":
        keyboard = [[InlineKeyboardButton(name, callback_data=name)] for name in capsules.keys()]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Выбери капсулу:", reply_markup=reply_markup)

    elif query.data in capsules:
        capsule = capsules[query.data]

        # Разделяем название на имя и интенсивность
        full_name = query.data
        if "[" in full_name and "]" in full_name:
            name_part = full_name.split("[")[0].strip()
            intensity_part = "[" + full_name.split("[")[1]
        else:
            name_part = full_name
            intensity_part = ""

        # Экранирование Markdown V2
        def escape_md(text: str) -> str:
            for ch in ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']:
                text = text.replace(ch, f"\\{ch}")
            return text

        safe_name = escape_md(name_part)
        safe_intensity = escape_md(intensity_part)
        safe_grade = escape_md(capsule['grade'])
        safe_desc = escape_md(capsule['desc'])

        await query.message.reply_photo(
            photo=capsule["photo"],
            caption=f"*{safe_name}*\n{safe_intensity}\n{safe_grade}\n_{safe_desc}_",
            parse_mode=ParseMode.MARKDOWN_V2
        )

        keyboard = [[InlineKeyboardButton("📋 Показать список капсул", callback_data="show_capsules")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Хочешь выбрать другую капсулу?", reply_markup=reply_markup)

def main():
    # Стартуем Flask в отдельном потоке (для keep-alive/пинга UptimeRobot)
    threading.Thread(target=start_flask, daemon=True).start()

    # Запускаем Telegram-бота
    tg_app = Application.builder().token(os.getenv("BOT_TOKEN")).build()
    tg_app.add_handler(CommandHandler("start", start))
    tg_app.add_handler(CallbackQueryHandler(button_handler))
    tg_app.run_polling()

if __name__ == "__main__":
    main()
