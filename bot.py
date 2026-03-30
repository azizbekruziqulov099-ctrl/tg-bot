from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
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
    await update.message.reply_text("Xush kelibsiz 🚀", reply_markup=menu)

# 🎯 BUTTON HANDLER
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    # MATN TANLASH
    if data == "content_yes":
        user_states[user_id] = "content_input"
        await query.message.reply_text("📝 Matnni yozing (1000 so‘zgacha):")

    elif data == "content_no":
        user_data[user_id]["content"] = "auto"
        user_states[user_id] = "design"
        await send_design(query)

    # DESIGN
    elif data.startswith("design"):
        user_data[user_id]["design"] = data.split("_")[1]
        user_states[user_id] = "style"
        await send_style(query)

    # STYLE
    elif data.startswith("style"):
        user_data[user_id]["style"] = data.split("_")[1]
        user_states[user_id] = "slides"
        await query.message.reply_text("📄 Slayd soni (5–60):")

# 🎨 DESIGN MENU
async def send_design(query):
    keyboard = [
        [InlineKeyboardButton("1", callback_data="design_1"),
         InlineKeyboardButton("2", callback_data="design_2"),
         InlineKeyboardButton("3", callback_data="design_3")],
        [InlineKeyboardButton("4", callback_data="design_4"),
         InlineKeyboardButton("5", callback_data="design_5"),
         InlineKeyboardButton("6", callback_data="design_6")]
    ]

    await query.message.reply_text("🎨 Dizayn tanlang:", reply_markup=InlineKeyboardMarkup(keyboard))

# 🖼 STYLE MENU
async def send_style(query):
    keyboard = [
        [InlineKeyboardButton("1", callback_data="style_1"),
         InlineKeyboardButton("2", callback_data="style_2"),
         InlineKeyboardButton("3", callback_data="style_3")],
        [InlineKeyboardButton("4", callback_data="style_4"),
         InlineKeyboardButton("5", callback_data="style_5")]
    ]

    await query.message.reply_text("🖼 Stil tanlang:", reply_markup=InlineKeyboardMarkup(keyboard))

# MAIN
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    if text == "📊 PPT yaratish":
        user_states[user_id] = "topic"
        await update.message.reply_text("📌 PPT mavzusini yozing:")
        return

    if user_states.get(user_id) == "topic":
        user_data[user_id] = {"topic": text}
        user_states[user_id] = "content_choice"

        keyboard = [
            [InlineKeyboardButton("✍️ Matn yozaman", callback_data="content_yes")],
            [InlineKeyboardButton("🤖 O‘zi qilsin", callback_data="content_no")]
        ]

        await update.message.reply_text(
            "📝 Maruza matni bormi?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    if user_states.get(user_id) == "content_input":
        user_data[user_id]["content"] = text
        user_states[user_id] = "design"

        await update.message.reply_text("✅ Matn qabul qilindi")
        await send_design(update)
        return

    if user_states.get(user_id) == "slides":
        try:
            slides = int(text)
        except:
            await update.message.reply_text("❌ Son kiriting")
            return

        user_data[user_id]["slides"] = slides
        user_states[user_id] = None

        data = user_data[user_id]

        summary = (
            f"📊 PPT:\n\n"
            f"📌 {data['topic']}\n"
            f"🎨 {data['design']}\n"
            f"🖼 {data['style']}\n"
            f"📄 {data['slides']}"
        )

        await update.message.reply_text(summary)
        return

    if text == "🪙 Tangalarim":
        await update.message.reply_text(f"{get_balance(user_id)} ta tanga bor")
        return

    await update.message.reply_text("Tushunmadim 😅")

# RUN
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(CallbackQueryHandler(handle_buttons))

app.run_polling()
