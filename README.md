# SB24 ToDo List Bot

Focused Telegram task manager for @SB24ToDoBot.

## Main actions

- Add Task
- My Tasks
- Complete Task

No external URLs, redirects, gambling, betting, casino, prize, or real-money gaming functionality.

## Setup

1. Use Python 3.12+.
2. Install dependencies with: pip install -r requirements.txt
3. Set BOT_TOKEN.
4. Run: python -m app.main

## Render

Use a Background Worker with build command "pip install -r requirements.txt" and start command "python -m app.main". Set BOT_TOKEN as a secret.

SQLite is used for the small single-bot deployment. Use persistent storage if the host uses ephemeral worker disks.

Telegram Ads approval is not guaranteed; moderation decisions are made by Telegram.
