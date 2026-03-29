from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN topilmadi")

menu = ReplyKeyboardMarkup(
    [
        ["📊 PPT yaratish"],
        ["🪙 Tangalarim", "ℹ️ Yordam"]
    ],
    resize_keyboard=True
)

user_balances = {}

def get_balance(user_id):
    if user_id not in user_balances:
        user_balances[user_id] = 10
    return user_balances[user_id]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Assalomu alaykum!\nBotga xush kelibsiz 🚀",
        reply_markup=menu
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    if text == "📊 PPT yaratish":
        if get_balance(user_id) < 10:
            await update.message.reply_text("❌ Tanga yetarli emas")
            return
        
        user_balances[user_id] -= 10
        await update.message.reply_text("⏳ PPT tayyorlanmoqda...")

    elif text == "🪙 Tangalarim":
        await update.message.reply_text(f"{get_balance(user_id)} ta tanga bor")

    elif text == "ℹ️ Yordam":
        await update.message.reply_text("Bot PPT yaratadi")

    else:
        await update.message.reply_text("Tushunmadim 😅")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
