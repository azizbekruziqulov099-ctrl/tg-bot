from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
from flask import Flask
import threading

# 🌐 KEEP ALIVE
app_web = Flask(__name__)

@app_web.route("/")
def home():
    return "Bot ishlayapti!"

def run_web():
    app_web.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_web).start()

TOKEN = os.getenv("TOKEN")
ADMIN_ID = 401251407

menu = ReplyKeyboardMarkup(
    [
        ["📊 PPT yaratish"],
        ["🪙 Tangalarim", "💰 Tanga sotib olish"],
        ["ℹ️ Yordam"]
    ],
    resize_keyboard=True
)

user_states = {}
user_data = {}
user_balances = {}

def get_balance(user_id):
    if user_id not in user_balances:
        user_balances[user_id] = 10
    return user_balances[user_id]

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Xush kelibsiz 🚀\nSizga 10 ta tanga berildi 🎁",
        reply_markup=menu
    )

# MAIN LOGIC
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    # 🚀 BOSHLASH
    if text == "📊 PPT yaratish":
        if get_balance(user_id) < 5:
            await update.message.reply_text("❌ Tanga yetarli emas")
            return

        user_states[user_id] = "topic"
        await update.message.reply_text("📌 PPT mavzusini yozing:")
        return

    # 📌 MAVZU
    if user_states.get(user_id) == "topic":
        user_data[user_id] = {"topic": text}
        user_states[user_id] = "content_choice"

        await update.message.reply_text(
            "📝 Maruza matni bormi?\n\n"
            "1️⃣ Ha\n2️⃣ Yo‘q (o‘zi qiladi)"
        )
        return

    # 📝 MATN TANLOV
   if user_states.get(user_id) == "content_choice":
    if text in ["1", "ha", "Ha", "HA"]:
        user_states[user_id] = "content_input"
        await update.message.reply_text("📝 Maruza matnini yozing (1000 so‘zgacha):")
    
    elif text in ["2", "yoq", "yo'q", "Yo‘q", "yo‘q"]:
        user_data[user_id]["content"] = "auto"
        user_states[user_id] = "type"

        await update.message.reply_text(
            "📝 PPT turini tanlang:\n1. Maruza\n2. Oddiy yozma"
        )
    
    else:
        await update.message.reply_text("❌ 1 yoki 2 tanlang")
    
    return
       if user_states.get(user_id) == "content_choice":
    if text in ["1", "ha", "Ha", "HA"]:
        user_states[user_id] = "content_input"
        await update.message.reply_text("📝 Maruza matnini yozing (1000 so‘zgacha):")
    
    elif text in ["2", "yoq", "yo'q", "Yo‘q", "yo‘q"]:
        user_data[user_id]["content"] = "auto"
        user_states[user_id] = "type"

        await update.message.reply_text(
            "📝 PPT turini tanlang:\n1. Maruza\n2. Oddiy yozma"
        )
    
    else:
        await update.message.reply_text("❌ 1 yoki 2 tanlang")
    
    return

    # ✍️ MATN KIRITISH
    if user_states.get(user_id) == "content_input":
        user_data[user_id]["content"] = text
        user_states[user_id] = "type"
        await update.message.reply_text("📝 Tur tanlang (1 yoki 2):")
        return

    # 📝 TUR
    if user_states.get(user_id) == "type":
        user_data[user_id]["type"] = text
        user_states[user_id] = "design"
        await update.message.reply_text("🎨 Dizayn (1–6):")
        return

    # 🎨 DIZAYN
    if user_states.get(user_id) == "design":
        user_data[user_id]["design"] = text
        user_states[user_id] = "style"
        await update.message.reply_text("🖼 Stil (1–5):")
        return

    # 🖼 STIL
    if user_states.get(user_id) == "style":
        user_data[user_id]["style"] = text
        user_states[user_id] = "slides"
        await update.message.reply_text("📄 Slayd (5–60):")
        return

    # 📄 SLAYD
    if user_states.get(user_id) == "slides":
        try:
            slides = int(text)
        except:
            await update.message.reply_text("❌ Son kiriting")
            return

        if slides < 5 or slides > 60:
            await update.message.reply_text("❌ 5–60 oralig‘ida")
            return

        if get_balance(user_id) < slides:
            await update.message.reply_text("❌ Tanga yetarli emas")
            return

        user_data[user_id]["slides"] = slides
        user_balances[user_id] -= slides
        user_states[user_id] = None

        data = user_data[user_id]

        content = data.get("content", "auto")
        if content == "auto":
            content_text = "🤖 Avtomatik"
        else:
            content_text = content[:200] + "..."

        summary = (
            f"📊 PPT ma'lumotlari:\n\n"
            f"📌 Mavzu: {data['topic']}\n"
            f"🧾 Matn: {content_text}\n"
            f"📝 Tur: {data['type']}\n"
            f"🎨 Dizayn: {data['design']}\n"
            f"🖼 Stil: {data['style']}\n"
            f"📄 Slayd: {data['slides']}\n"
        )

        await update.message.reply_text(summary)
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🆕 Yangi PPT\nUser: {user_id}\n\n{summary}"
        )
        return

    # 🪙 BALANS
    if text == "🪙 Tangalarim":
        await update.message.reply_text(f"{get_balance(user_id)} ta tanga bor 🪙")
        return

    # 💰 SOTIB OLISH
    if text == "💰 Tanga sotib olish":
        await update.message.reply_text(
            "💳 10 tanga = 5000 so‘m\n40 tanga = 20000 so‘m\n\nChek yuboring 📸"
        )
        return

    await update.message.reply_text("Tushunmadim 😅")


# 📸 CHEK
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    await update.message.reply_text("✅ Chek qabul qilindi")

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=update.message.photo[-1].file_id,
        caption=f"💸 To‘lov\nUser: {user_id}"
    )


# 💰 ADMIN
async def add_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    user_id = int(context.args[0])
    amount = int(context.args[1])

    user_balances[user_id] = user_balances.get(user_id, 0) + amount

    await update.message.reply_text("✅ Qo‘shildi")

    await context.bot.send_message(
        chat_id=user_id,
        text=f"💰 +{amount} tanga qo‘shildi!\nJami: {user_balances[user_id]}"
    )


# RUN
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add_coin))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

app.run_polling()
