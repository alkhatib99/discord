import json
import os

ACCOUNT_FILE = "accounts.json"

FIELDS = [
    ("email", "📧 Enter your email"),
    ("bearer_token", "🪙 Enter Bearer Token"),
    ("consumer_key", "🔑 Enter Consumer Key"),
    ("consumer_secret", "🔐 Enter Consumer Secret"),
    ("access_token", "🔓 Enter Access Token"),
    ("access_token_secret", "🔏 Enter Access Token Secret")
]

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

def prompt_account():
    accounts = load_accounts()
    new_account = {}

    print("=== Add New X (Twitter) Account ===\n")
    
    for key, prompt in FIELDS:
        value = input(f"{prompt}: ").strip()

        if key == "email" and email_exists(value, accounts):
            print(f"⚠️ Email `{value}` already exists. Aborting.")
            return

        new_account[key] = value

    accounts.append(new_account)
    save_accounts(accounts)
    print("\n✅ Account saved successfully!")

if __name__ == "__main__":
    prompt_account()
