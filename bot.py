import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
)
from keep_alive import keep_alive  # ✅ Keep bot alive with Flask ping

TOKEN = "7945756761:AAH9rgtEx3eOfZWGto-JD1A5DjM1MHOlflA"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

no_exempt_users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    mention = user.mention_html()
    text = (
        f"✫ 𝝜𝝚ⳐⳐ𝝤 {mention}  Ѡ𝝚Ⳑ𝗖𝝤𝝡𝝚 𝝩𝝤 ͢🦋⃟≛⃝ 𝕻𝖗𝖎𝖓𝖈𝖊𝖘𝖘≛⃝   𝝗𝝤𝝩 ✫\n\n"
        "🔸𝗖Ⳑ𝝞𝗖𝝟 𝙰𝚍𝚍 𝚃𝚘 𝙶𝚛𝚘𝚞𝚙 & G𝝞V𝝚 𝝡𝝚 𝙰𝚍𝚖𝚒𝚗 𝝦𝝚Ɍ𝝡𝝞SS𝝞𝝤𝝢 𝝩𝝤 US𝝚"
    )
    keyboard = [[InlineKeyboardButton("➕ Add To Group", url="https://t.me/princes_x_bot?startgroup=true")]]
    await update.message.reply_html(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def add_noexempt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /addnoexempt <user_id>")
    group_id = str(update.effective_chat.id)
    user_id = context.args[0]
    no_exempt_users.setdefault(group_id, set()).add(user_id)
    await update.message.reply_text(f"✅ Added {user_id} to no-exempt list.")

async def remove_noexempt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /removenoexempt <user_id>")
    group_id = str(update.effective_chat.id)
    user_id = context.args[0]
    if group_id in no_exempt_users and user_id in no_exempt_users[group_id]:
        no_exempt_users[group_id].remove(user_id)
        await update.message.reply_text(f"✅ Removed {user_id} from no-exempt list.")
    else:
        await update.message.reply_text("User not in list.")

async def list_noexempt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_id = str(update.effective_chat.id)
    users = no_exempt_users.get(group_id, set())
    if users:
        await update.message.reply_text("📌 No-Exempt Users:\n" + "\n".join(users))
    else:
        await update.message.reply_text("⚠️ No users in no-exempt list.")

async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_id = str(update.effective_chat.id)
    user_id = str(update.effective_user.id)
    text = update.message.text or ""
    if "t.me/" in text or "telegram.me/" in text:
        if user_id in no_exempt_users.get(group_id, set()):
            try:
                await update.message.delete()
            except Exception as e:
                logging.warning(f"Couldn't delete message: {e}")

if __name__ == '__main__':
    keep_alive()  # ✅ keep-alive web server start
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addnoexempt", add_noexempt))
    app.add_handler(CommandHandler("removenoexempt", remove_noexempt))
    app.add_handler(CommandHandler("listnoexempt", list_noexempt))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, check_message))

    print("✅ Bot is running and ready!")
    app.run_polling()
