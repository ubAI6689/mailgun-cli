import os
import subprocess
import sys

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
    """Get email addresses from user input (one per line, empty line to finish)."""
    print("Enter email addresses to remove (one per line, empty line to finish):")
    emails = []
    while True:
        line = input("Email: ").strip()
        if not line:
            break
        emails.append(line)
    return emails


def remove_members_from_list(list_name, emails):
    """Remove members from a mailing list."""
    for email in emails:
        print(f"  Removing {email}...")
        subprocess.run([MAILGUN_CMD, "remove", list_name, email])


if __name__ == "__main__":
    list_names = get_list_names()
    if not list_names:
        print("No list names provided.")
        sys.exit(1)

    emails = get_emails()
    if not emails:
        print("No emails provided.")
        sys.exit(1)

    print(f"\nRemoving {len(emails)} member(s) from {len(list_names)} list(s)...\n")
    for list_name in list_names:
        print(f"[{list_name}]")
        remove_members_from_list(list_name, emails)
        print()
    print("Done.")
