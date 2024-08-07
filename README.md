# Mailgun Mailing List CLI

A command-line interface (CLI) program to control Mailgun mailing lists.

## Installation

1. Clone the repository:
```
git clone https://github.com/ubAI6689/mailgun-cli.git
```
2. Navigate to the project-directory:
```
cd mailgun-cli
```
3. Create and activate a venv:
```
python -m venv venv
source venv/bin/activate
```
4. Install the package:
```
pip install -e .
```

## Usage

1. Set up your Mailgun configuration:
```
mailgun setup
```
2. Use the available commands to manage your mailing lists:
- Create a mailing list: `mailgun create <address> <name>`
- Delete a mailing list: `mailgun delete <address>`
- Add a member to a mailing list: `mailgun add <list_address> <member_address> <name>`
- Add members from a csv file: `mailgun add_from_csv <list_address> <csv_file_path>`
- Remove a member from a mailing list: `mailgun remove <list_address> <member_address>`
- Print a mailing list members: `mailgun print <list_address>`
- Send a message to a mailing list: `mailgun send <list_address> <subject> <text>`
- List all mailing lists: `mailgun list`
- List all groups an email is a member of: `mailgun list_groups <email>`

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

[Include your license information here]