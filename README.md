# Telegram No-Link Filter Bot (Fly.io Ready)

A Telegram bot that deletes link messages for non-exempt users/admins. Anonymous admins are always restricted.

## 🔧 Commands
- `/addnoexempt <group_id> <user_id>`
- `/removenoexempt <group_id> <user_id>`
- `/listnoexempt <group_id>`
- `/start`

## 🚀 Deploy to Fly.io

1. Install Fly CLI:
   ```bash
   curl -L https://fly.io/install.sh | sh
   fly auth login
   ```

2. Launch app:
   ```bash
   fly launch --name telegram-link-block-bot --no-deploy
   ```

3. Set token:
   ```bash
   fly secrets set BOT_TOKEN="YOUR_BOT_TOKEN"
   ```

4. Deploy:
   ```bash
   fly deploy
   ```

## ✅ Notes
- Uses long polling (no need for webhook).
- Token securely loaded using environment variable.
