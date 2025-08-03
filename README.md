# Telegram No-Link Filter Bot

This bot deletes messages containing links from users who are not exempt in a group.
It also supports commands to manage "no-exempt" admin lists per group.

## 🔧 Commands

- `/addnoexempt <group_id> <user_id>` - Add a user to the no-exempt list for a group
- `/removenoexempt <group_id> <user_id>` - Remove a user from no-exempt list
- `/listnoexempt <group_id>` - List users in the no-exempt list
- `/start` - Check bot is running

## ▶️ How to Run
1. Replace your bot token in `bot.py`
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the bot:
   ```bash
   python bot.py
   ```

## 📌 Notes
- Admins can post links unless they are in the no-exempt list.
- Anonymous admins are **not allowed** to post links.
