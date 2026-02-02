import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

TOKEN = '7760908507:AAFaGQSHZXRrM06A7Aum-QqmVu7U7X6MVk4'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("هلا بيك! دزلي (صورة، فيديو، ملف) وأحذفه إلك بوقت محدد.")

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_id = update.message.message_id
    keyboard = [[
        InlineKeyboardButton("10 ثواني", callback_data=f"del_10_{file_id}"),
        InlineKeyboardButton("دقيقة", callback_data=f"del_60_{file_id}")
    ]]
    await update.message.reply_text("شوكت أحذفه؟", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data.split("_")
    seconds, msg_id = int(data[1]), int(data[2])
    await query.edit_message_text(text=f"سيتم الحذف بعد {seconds} ثانية...")
    await asyncio.sleep(seconds)
    try:
        await context.bot.delete_message(chat_id=query.message.chat_id, message_id=msg_id)
        await query.delete_message()
    except: pass

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO | filters.Document, handle_media))
    app.add_handler(CallbackQueryHandler(button_click))
    app.run_polling()
