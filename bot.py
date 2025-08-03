
import os
import re
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN") or "7945756761:AAH9rgtEx3eOfZWGto-JD1A5DjM1MHOlflA"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

no_exempt = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot is active!")

async def add_no_exempt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text("Usage: /addnoexempt <group_id> <user_id>")
        return

    group_id, user_id = context.args
    if group_id not in no_exempt:
        no_exempt[group_id] = []
    if user_id not in no_exempt[group_id]:
        no_exempt[group_id].append(user_id)
        await update.message.reply_text(f"✅ User {user_id} added to no-exempt list for group {group_id}")
    else:
        await update.message.reply_text("ℹ️ User already in no-exempt list.")

async def remove_no_exempt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text("Usage: /removenoexempt <group_id> <user_id>")
        return

    group_id, user_id = context.args
    if group_id in no_exempt and user_id in no_exempt[group_id]:
        no_exempt[group_id].remove(user_id)
        await update.message.reply_text(f"✅ User {user_id} removed from no-exempt list for group {group_id}")
    else:
        await update.message.reply_text("ℹ️ User not found in the no-exempt list.")

async def list_no_exempt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /listnoexempt <group_id>")
        return

    group_id = context.args[0]
    users = no_exempt.get(group_id, [])
    await update.message.reply_text(f"📋 No-Exempt list for {group_id}: {', '.join(users) if users else 'Empty'}")

async def delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    text = message.text or ""
    if re.search(r'(https?://|t\.me)', text):
        if not message.from_user:
            return
        user_id = str(message.from_user.id)
        group_id = str(message.chat_id)

        if message.chat.type in ['group', 'supergroup']:
            member = await context.bot.get_chat_member(group_id, user_id)
            if member.status not in ['administrator', 'creator'] or user_id in no_exempt.get(group_id, []):
                try:
                    await message.delete()
                except Exception as e:
                    logger.warning(f"Could not delete message: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addnoexempt", add_no_exempt))
    app.add_handler(CommandHandler("removenoexempt", remove_no_exempt))
    app.add_handler(CommandHandler("listnoexempt", list_no_exempt))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, delete_links))

    app.run_polling()
