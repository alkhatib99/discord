import discord
from discord import Option
import json
import os

TOKEN = "YOUR_DISCORD_BOT_TOKEN"
ACCOUNT_FILE = "accounts.json"

intents = discord.Intents.default()
bot = discord.Bot(intents=intents)

def load_accounts():
    if not os.path.exists(ACCOUNT_FILE):
        with open(ACCOUNT_FILE, "w") as f:
            json.dump([], f)
        return []
    with open(ACCOUNT_FILE, "r") as f:
        return json.load(f)

def save_accounts(accounts):
    with open(ACCOUNT_FILE, "w") as f:
        json.dump(accounts, f, indent=4)

def email_exists(email, accounts):
    return any(acc["email"].lower() == email.lower() for acc in accounts)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.slash_command(name="addaccount", description="Add a new Twitter/X account to the system.")
async def add_account(
    ctx: discord.ApplicationContext,
    email: Option(str, "Your email"),
    bearer_token: Option(str, "Bearer token"),
    consumer_key: Option(str, "Consumer key"),
    consumer_secret: Option(str, "Consumer secret"),
    access_token: Option(str, "Access token"),
    access_token_secret: Option(str, "Access token secret")
):
    accounts = load_accounts()

    if email_exists(email, accounts):
        await ctx.respond("⚠️ This email already exists in the database.", ephemeral=True)
        return

    new_account = {
        "email": email,
        "bearer_token": bearer_token,
        "consumer_key": consumer_key,
        "consumer_secret": consumer_secret,
        "access_token": access_token,
        "access_token_secret": access_token_secret
    }

    accounts.append(new_account)
    save_accounts(accounts)

    await ctx.respond("✅ Account successfully saved!", ephemeral=True)

bot.run(TOKEN)
