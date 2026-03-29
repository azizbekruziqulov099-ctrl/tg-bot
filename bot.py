from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

TOKEN = os.getenv("TOKEN")

ADMIN_ID = 401251407  # 👈 BU YERGA O‘ZINGNI ID QO‘Y

menu = ReplyKeyboardMarkup(
    [
        ["📊 PPT yaratish"],
        ["🪙 Tangalarim", "💰 Tanga sotib olish"],
        ["ℹ️ Yordam"]
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
        "Xush kelibsiz 🚀\nSizga 10 ta tanga berildi 🎁",
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
        await update.message.reply_text(f"{get_balance(user_id)} ta tanga bor 🪙")

    elif text == "💰 Tanga sotib olish":
        await update.message.reply_text(
            "💳 Paketlar:\n\n"
            "10 tanga = 5,000 so‘m\n"
            "40 tanga = 20,000 so‘m\n\n"
            "💸 To‘lov uchun karta:\n"
            "8600 XXXX XXXX XXXX\n\n"
            "To‘lagach chek yuboring 📸"
        )

    elif text == "ℹ️ Yordam":
        await update.message.reply_text("Bot PPT yaratadi")

    else:
        await update.message.reply_text("Tushunmadim 😅")

# 📸 CHEK QABUL QILISH
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id

    await update.message.reply_text("✅ Chek qabul qilindi")

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=update.message.photo[-1].file_id,
        caption=f"💸 Yangi to‘lov!\nUser ID: {user_id}"
    )

# 💰 ADMIN TANGA BERADI
async def add_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return
    
    try:
        user_id = int(context.args[0])
        amount = int(context.args[1])

        user_balances[user_id] = user_balances.get(user_id, 0) + amount

        await update.message.reply_text("✅ Tanga qo‘shildi")
    except:
        await update.message.reply_text("Xato format")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add_coin))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

app.run_polling()
