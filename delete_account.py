import json
import os

ACCOUNT_FILE = "accounts.json"

def load_accounts():
    if not os.path.exists(ACCOUNT_FILE):
        return []
    with open(ACCOUNT_FILE, "r") as f:
        return json.load(f)

def save_accounts(accounts):
    with open(ACCOUNT_FILE, "w") as f:
        json.dump(accounts, f, indent=4)

def delete_account(email):
    accounts = load_accounts()
    new_accounts = [acc for acc in accounts if acc["email"].lower() != email.lower()]
    
    if len(new_accounts) == len(accounts):
        print("❌ Email not found.")
    else:
        save_accounts(new_accounts)
        print("✅ Account deleted successfully.")

if __name__ == "__main__":
    target_email = input("🗑 Enter the email of the account to delete: ").strip()
    delete_account(target_email)
