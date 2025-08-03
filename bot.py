import os
import re
import logging
from telegram import Update
from telegram.ext import (
    Application, ApplicationBuilder, CommandHandler,
    MessageHandler, ContextTypes, filters
)

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global no-exempt list per group
group_no_exempt_admin_ids = {}

# Regex pattern to detect links
link_pattern = re.compile(r"(http[s]?://|t\.me/)", re.IGNORECASE)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running and ready!\nYou can control me via private chat using group IDs.")

# Add user to no-exempt list
async def add_no_exempt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("⚠️ Usage: /addnoexempt <group_id> <user_id>")
        return
    try:
        group_id = int(context.args[0])
        user_id = int(context.args[1])
        group_no_exempt_admin_ids.setdefault(group_id, [])
        if user_id not in group_no_exempt_admin_ids[group_id]:
            group_no_exempt_admin_ids[group_id].append(user_id)
            await update.message.reply_text(f"✅ User {user_id} added to no-exempt list for group {group_id}.")
        else:
            await update.message.reply_text("ℹ️ Already in the list.")
    except ValueError:
        await update.message.reply_text("❌ Invalid IDs.")

# Remove user from no-exempt list
async def remove_no_exempt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("⚠️ Usage: /removenoexempt <group_id> <user_id>")
        return
    try:
        group_id = int(context.args[0])
        user_id = int(context.args[1])
        if group_id in group_no_exempt_admin_ids and user_id in group_no_exempt_admin_ids[group_id]:
            group_no_exempt_admin_ids[group_id].remove(user_id)
            await update.message.reply_text("✅ Removed from list.")
        else:
            await update.message.reply_text("ℹ️ Not found in the list.")
    except ValueError:
        await update.message.reply_text("❌ Invalid IDs.")

# List no-exempt users in group
async def list_no_exempt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 1:
        await update.message.reply_text("⚠️ Usage: /listnoexempt <group_id>")
        return
    try:
        group_id = int(context.args[0])
        ids = group_no_exempt_admin_ids.get(group_id, [])
        if not ids:
            await update.message.reply_text("ℹ️ No users in the list.")
        else:
            await update.message.reply_text("📝 No-exempt list:\n" + "\n".join(str(uid) for uid in ids))
    except ValueError:
        await update.message.reply_text("❌ Invalid group ID.")

# Auto-delete links if not exempt
async def delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat = update.effective_chat
        user = update.effective_user
        admins = await chat.get_administrators()
        admin_ids = [admin.user.id for admin in admins]
        no_exempt_ids = group_no_exempt_admin_ids.get(chat.id, [])

        if user.id in admin_ids and user.id not in no_exempt_ids:
            return

        if update.message and link_pattern.search(update.message.text or ""):
            await update.message.delete()
            await update.message.reply_text("❌ Links are not allowed!")
    except Exception as e:
        logger.warning(f"Error deleting link: {e}")

# Main bot entry
TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise ValueError("❌ TOKEN environment variable not set!")

app = ApplicationBuilder().token(TOKEN).build()

# Command handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("addnoexempt", add_no_exempt))
app.add_handler(CommandHandler("removenoexempt", remove_no_exempt))
app.add_handler(CommandHandler("listnoexempt", list_no_exempt))

# Message handler for link deletion
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), delete_links))

# Run the bot
if __name__ == "__main__":
    app.run_polling()
