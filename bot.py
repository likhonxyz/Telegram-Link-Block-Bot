import os
import re
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters
from telegram import Update
from telegram.ext import ContextTypes

# No-exempt list
no_exempt_admin_ids = []

# Regex for links
link_pattern = re.compile(r"(http[s]?://|t\.me/)", re.IGNORECASE)

async def delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_administrators = await update.effective_chat.get_administrators()
    admin_ids = [admin.user.id for admin in chat_administrators]

    if user.id in admin_ids and user.id not in no_exempt_admin_ids:
        return

    if update.message and link_pattern.search(update.message.text or ""):
        try:
            await update.message.delete()
            await update.message.reply_text("❌ Links are not allowed!")
        except Exception as e:
            print(f"Error deleting message: {e}")

async def add_no_exempt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Usage: /addnoexempt <user_id>")
        return
    try:
        user_id = int(context.args[0])
        if user_id not in no_exempt_admin_ids:
            no_exempt_admin_ids.append(user_id)
            await update.message.reply_text(f"✅ User ID {user_id} added to no-exempt list.")
        else:
            await update.message.reply_text(f"ℹ️ User ID {user_id} already in no-exempt list.")
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID.")

async def remove_no_exempt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Usage: /removenoexempt <user_id>")
        return
    try:
        user_id = int(context.args[0])
        if user_id in no_exempt_admin_ids:
            no_exempt_admin_ids.remove(user_id)
            await update.message.reply_text(f"✅ User ID {user_id} removed from no-exempt list.")
        else:
            await update.message.reply_text(f"ℹ️ User ID {user_id} not found in no-exempt list.")
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID.")

async def list_no_exempt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not no_exempt_admin_ids:
        await update.message.reply_text("ℹ️ No user IDs in no-exempt list.")
    else:
        ids_text = "\n".join(str(uid) for uid in no_exempt_admin_ids)
        await update.message.reply_text(f"📝 No-exempt list:\n{ids_text}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running and ready to delete links!")

TOKEN = os.environ.get("TOKEN")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), delete_links))
app.add_handler(CommandHandler("addnoexempt", add_no_exempt))
app.add_handler(CommandHandler("removenoexempt", remove_no_exempt))
app.add_handler(CommandHandler("listnoexempt", list_no_exempt))
app.add_handler(CommandHandler("start", start))

print("✅ Bot is running...")
app.run_polling()
