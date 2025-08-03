# Telegram Link Filter Bot

A Telegram bot that deletes messages containing links (like http, https, t.me) unless the sender is exempted.

## Commands

- `/addnoexempt <group_id> <user_id>`
- `/removenoexempt <group_id> <user_id>`
- `/listnoexempt <group_id>`

## Usage

Install dependencies:

```
pip install -r requirements.txt
```

Run the bot:

```
python bot.py
```

Set your bot token in an environment variable or directly in `bot.py`.
