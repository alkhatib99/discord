# 🤖 Discord Account Collector Bot

A smart interactive bot for Discord that collects and manages X (Twitter) account credentials securely using modals and button-based UI.

## 🧩 Features
- ➕ Add account via interactive modal
- 📄 List all saved emails
- 🗑 Delete account by email
- 🔐 Role-based access (`AccountAdmin`)
- ✅ Validations (duplicate email, permission check)
- 💾 Stores data in local `accounts.json` file

## 🚀 Setup Instructions

### 1. Clone & Install Dependencies

```bash
git clone git@github.com:alkhatib99/discord.git
cd discord
pip install -U py-cord python-dotenv
```

### 2. Add Bot Token

Create `.env` file and add:
```env
DISCORD_TOKEN=your_token_here
```

### 3. Run the Bot

```bash
python main.py
```

## 🛡 Permissions Needed

Invite the bot with:
- `Send Messages`
- `Read Message History`
- `Use Slash Commands`

## 📂 Data Storage

All account info is saved in:
```
accounts.json
```
