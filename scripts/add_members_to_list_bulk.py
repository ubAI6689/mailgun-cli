import os
import subprocess

# Set the file containing the list of mailing lists
MAILING_LIST_FILE = "mailing_lists.txt"

# Set the directory containing the CSV files
CSV_DIRECTORY = "../csv/mailing_list"

# Read the mailing lists from the file
with open(MAILING_LIST_FILE, "r") as file:
    for list_name in file:
        list_name = list_name.strip()
        
        # Check if the corresponding CSV file exists
        csv_file = os.path.join(CSV_DIRECTORY, f"{list_name}.csv")
        if os.path.isfile(csv_file):
            # Add members to the mailing list using the CLI application
            subprocess.run(["mailgun", "add_from_csv", list_name, csv_file])
        else:
            print(f"CSV file not found for mailing list: {list_name}")