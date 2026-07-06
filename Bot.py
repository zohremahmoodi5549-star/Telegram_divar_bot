from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

TOKEN ="8862543927:AAFab0buerlXtECOiqOgl-BUA5NS6uMlhg8 "

PHOTO, TEXT = range(2)

keyboard = [["🛒 ثبت کالا"]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\nبه ربات پیمان سمساری خوش اومدی.",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
    )

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📷 لطفاً عکس کالا را ارسال کن.")
    return PHOTO

async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["photo"] = update.message.photo[-1].file_id
    await update.message.reply_text("📝 حالا توضیحات کالا را بنویس.")
    return TEXT

async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=context.user_data["photo"],
        caption=f"📦 آگهی جدید\n\n{update.message.text}",
    )
    await update.message.reply_text("✅ آگهی ثبت شد.")
    return ConversationHandler.END

app = Application.builder().token(TOKEN).build()

conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^🛒 ثبت کالا$"), register)],
    states={
        PHOTO: [MessageHandler(filters.PHOTO, photo)],
        TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, text)],
    },
    fallbacks=[],
)

app.add_handler(CommandHandler("start", start))
app.add_handler(conv)

print("Bot Started...")
app.run_polling()
