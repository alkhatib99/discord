import json
import os

ACCOUNT_FILE = "accounts.json"

def load_accounts():
    if not os.path.exists(ACCOUNT_FILE):
        print("❗ No account file found.")
        return []

    with open(ACCOUNT_FILE, "r") as f:
        return json.load(f)

def list_emails():
    accounts = load_accounts()
    if not accounts:
        print("📭 No accounts saved yet.")
        return

    print("📋 Saved Account Emails:")
    for i, acc in enumerate(accounts, 1):
        print(f"{i}. {acc['email']}")

if __name__ == "__main__":
    list_emails()
