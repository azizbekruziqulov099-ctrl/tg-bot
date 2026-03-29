from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
user_states = {}
user_data = {}

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
elif text == "📊 PPT yaratish":
    user_states[user_id] = "topic"
    await update.message.reply_text("📌 PPT mavzusini yozing:")
if user_states.get(user_id) == "topic":
    user_data[user_id] = {"topic": text}
    user_states[user_id] = "type"

    await update.message.reply_text(
        "📝 PPT turini tanlang:\n1. Maruza\n2. Oddiy yozma"
    )
    if user_states.get(user_id) == "topic":
    user_data[user_id] = {"topic": text}
    user_states[user_id] = "type"

    await update.message.reply_text(
        "📝 PPT turini tanlang:\n1. Maruza\n2. Oddiy yozma"
    )
    elif user_states.get(user_id) == "design":
    user_data[user_id]["design"] = text
    user_states[user_id] = "style"

    await update.message.reply_text(
        "🖼 Rasm stilini tanlang (1–5):"
    )
    elif user_states.get(user_id) == "design":
    user_data[user_id]["design"] = text
    user_states[user_id] = "style"

    await update.message.reply_text(
        "🖼 Rasm stilini tanlang (1–5):"
    )
elif user_states.get(user_id) == "slides":
    slides = int(text)

    if slides < 5 or slides > 60:
        await update.message.reply_text("❌ 5–60 oralig‘ida kiriting")
        return

    user_data[user_id]["slides"] = slides
    user_states[user_id] = None

    await update.message.reply_text("⏳ PPT tayyorlanmoqda...")
user_data[user_id]
{
 "topic": "...",
 "type": "...",
 "design": "...",
 "style": "...",
 "slides": 20
}
{
 "topic": "...",
 "type": "...",
 "design": "...",
 "style": "...",
 "slides": 20
}
await update.message.reply_text("Tasdiqlaysizmi? (ha/yo‘q)")
user_states[user_id] = "confirm"
elif user_states.get(user_id) == "confirm":
    if text.lower() == "ha":
        await update.message.reply_text("🚀 PPT yaratilmoqda...")
    else:
        await update.message.reply_text("❌ Bekor qilindi")
    
    user_states[user_id] = None
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

    user_states[user_id] = "topic"
    await update.message.reply_text("📌 PPT mavzusini yozing:")
 # tanga ayiramiz
user_balances[user_id] -= user_data[user_id]["slides"]
    elif user_states.get(user_id) == "slides":
    slides = int(text)

    if slides < 5 or slides > 60:
        await update.message.reply_text("❌ 5–60 oralig‘ida kiriting")
        return

    user_data[user_id]["slides"] = slides
    user_states[user_id] = None

    # 💰 TANGA AYIRISH
    if get_balance(user_id) < slides:
        await update.message.reply_text("❌ Tanga yetarli emas")
        return

    user_balances[user_id] -= slides

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
async def add_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return
    
    try:
        user_id = int(context.args[0])
        amount = int(context.args[1])

        user_balances[user_id] = user_balances.get(user_id, 0) + amount

        # 👇 ADMIN ga
        await update.message.reply_text("✅ Tanga qo‘shildi")

        # 👇 USER ga xabar
        await context.bot.send_message(
            chat_id=user_id,
            text=f"💰 Hisobingizga {amount} ta tanga qo‘shildi!"
        )

    except:
        await update.message.reply_text("Xato format")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add_coin))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

app.run_polling()
