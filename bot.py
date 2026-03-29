from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
TOKEN = os.getenv("TOKEN")

menu = ReplyKeyboardMarkup(
    [
        ["📊 PPT yaratish"],
        ["🪙 Tangalarim", "ℹ️ Yordam"]
    ],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Assalomu alaykum!\nBotga xush kelibsiz 🚀",
        reply_markup=menu
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📊 PPT yaratish":
        await update.message.reply_text("Mavzu yuboring 📩")

    elif text == "🪙 Tangalarim":
        await update.message.reply_text("Sizda hozircha 0 ta tanga mavjud 🪙")

    elif text == "ℹ️ Yordam":
        await update.message.reply_text(
            "Bu bot sizga prezentatsiya yaratib beradi.\n\n"
            "📊 PPT yaratish - prezentatsiya\n"
            "🪙 Tangalar - balans\n"
        )

    else:
        await update.message.reply_text("Tushunmadim 😅")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()