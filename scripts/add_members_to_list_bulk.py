import os
import subprocess
import sys

# Suppress LibreSSL warning on macOS
os.environ["PYTHONWARNINGS"] = "ignore::UserWarning"

# Path to mailgun executable in venv
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MAILGUN_CMD = os.path.join(SCRIPT_DIR, "..", "venv", "bin", "mailgun")

def get_list_names():
    """Get list names from command-line arguments or prompt user."""
    if len(sys.argv) > 1:
        return [arg.strip() for arg in sys.argv[1:]]

    print("Enter mailing list names (one per line, empty line to finish):")
    lists = []
    while True:
        line = input("List: ").strip()
        if not line:
            break
        lists.append(line)
    return lists


def get_emails():
    """Get email addresses from user input."""
    print("Paste email addresses (one per line), then press Enter twice to finish:")
    print("-" * 50)

    emails = []
    empty_count = 0

    while True:
        try:
            line = input().strip()
            if not line:
                empty_count += 1
                if empty_count >= 1:
                    break
                continue
            empty_count = 0

            # Handle comma or space separated emails
            if ',' in line or (' ' in line and '@' in line):
                parts = line.replace(',', ' ').split()
                for part in parts:
                    part = part.strip()
                    if part and '@' in part:
                        emails.append(part)
            elif '@' in line:
                emails.append(line)
        except EOFError:
            break

    print("-" * 50)
    print(f"Captured {len(emails)} email(s)")
    return emails


def add_members_to_list(list_name, emails):
    """Add members to a mailing list."""
    for email in emails:
        print(f"  Adding {email}...")
        subprocess.run([MAILGUN_CMD, "add", list_name, email, email], stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    list_names = get_list_names()
    if not list_names:
        print("No list names provided.")
        sys.exit(1)

    emails = get_emails()
    if not emails:
        print("No emails provided.")
        sys.exit(1)

    print(f"\nAdding {len(emails)} member(s) to {len(list_names)} list(s)...\n")
    for list_name in list_names:
        print(f"[{list_name}]")
        add_members_to_list(list_name, emails)
        print()
    print("Done.")
