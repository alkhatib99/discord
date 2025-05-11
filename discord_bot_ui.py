import discord
import json
import os

TOKEN = "YOUR_DISCORD_BOT_TOKEN"
ACCOUNT_FILE = "accounts.json"
ADMIN_ROLE_NAME = "AccountAdmin"

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

def is_admin(member):
    return any(role.name == ADMIN_ROLE_NAME for role in member.roles)

class AddAccountModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="➕ Add X Account")
        self.email = discord.ui.InputText(label="Email", placeholder="example@email.com", required=True)
        self.bearer = discord.ui.InputText(label="Bearer Token", required=True)
        self.ckey = discord.ui.InputText(label="Consumer Key", required=True)
        self.csecret = discord.ui.InputText(label="Consumer Secret", required=True)
        self.atoken = discord.ui.InputText(label="Access Token", required=True)
        self.asecret = discord.ui.InputText(label="Access Token Secret", required=True)

        self.add_item(self.email)
        self.add_item(self.bearer)
        self.add_item(self.ckey)
        self.add_item(self.csecret)
        self.add_item(self.atoken)
        self.add_item(self.asecret)

    async def callback(self, interaction: discord.Interaction):
        if not is_admin(interaction.user):
            await interaction.response.send_message("❌ You do not have permission to add accounts.", ephemeral=True)
            return

        accounts = load_accounts()
        email = self.email.value.strip()

        if email_exists(email, accounts):
            await interaction.response.send_message("⚠️ Email already exists!", ephemeral=True)
            return

        new_account = {
            "email": email,
            "bearer_token": self.bearer.value.strip(),
            "consumer_key": self.ckey.value.strip(),
            "consumer_secret": self.csecret.value.strip(),
            "access_token": self.atoken.value.strip(),
            "access_token_secret": self.asecret.value.strip()
        }

        accounts.append(new_account)
        save_accounts(accounts)
        await interaction.response.send_message("✅ Account saved successfully!", ephemeral=True)

class DeleteAccountModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="🗑 Delete Account")
        self.email = discord.ui.InputText(label="Email", placeholder="example@email.com", required=True)
        self.add_item(self.email)

    async def callback(self, interaction: discord.Interaction):
        if not is_admin(interaction.user):
            await interaction.response.send_message("❌ You do not have permission to delete accounts.", ephemeral=True)
            return

        email = self.email.value.strip()
        accounts = load_accounts()
        new_accounts = [acc for acc in accounts if acc["email"].lower() != email.lower()]

        if len(new_accounts) == len(accounts):
            await interaction.response.send_message("⚠️ Email not found.", ephemeral=True)
        else:
            save_accounts(new_accounts)
            await interaction.response.send_message("✅ Account deleted successfully.", ephemeral=True)

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() in ["hi", "/start"]:
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="➕ Add Account", style=discord.ButtonStyle.primary, custom_id="add_account"))
        view.add_item(discord.ui.Button(label="📄 List Accounts", style=discord.ButtonStyle.secondary, custom_id="list_accounts"))
        view.add_item(discord.ui.Button(label="🗑 Delete Account", style=discord.ButtonStyle.danger, custom_id="delete_account"))

        await message.channel.send("👋 Welcome abu elsu7ab! Choose an action:", view=view)

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        cid = interaction.data["custom_id"]

        if cid == "add_account":
            await interaction.response.send_modal(AddAccountModal())

        elif cid == "delete_account":
            await interaction.response.send_modal(DeleteAccountModal())

        elif cid == "list_accounts":
            if not is_admin(interaction.user):
                await interaction.response.send_message("❌ You do not have permission to view accounts.", ephemeral=True)
                return

            accounts = load_accounts()
            if not accounts:
                await interaction.response.send_message("📭 No accounts saved yet.", ephemeral=True)
            else:
                emails = [f"• `{acc['email']}`" for acc in accounts]
                await interaction.response.send_message("📄 Saved Accounts:\n" + "\n".join(emails), ephemeral=True)

bot.run(TOKEN)
