import os
import subprocess

# Set the path to the text file containing the list of mailing lists
MAILING_LIST_FILE = "mailing_lists.txt"

# Read the mailing lists from the file
with open(MAILING_LIST_FILE, "r") as file:
    for line in file:
        # Split the line into name and description (assuming they are separated by a comma)
        parts = line.strip().split(",")
        name = parts[0].strip()
        description = parts[1].strip() if len(parts) > 1 else ""
        
        # Construct the command to create the mailing list using your CLI application
        command = f"mailgun create {name} '{description}'"
        
        try:
            # Execute the command using subprocess
            output = subprocess.check_output(command, shell=True, universal_newlines=True)
            print(f"Mailing list '{name}' created successfully.")
            print("Output:")
            print(output)
        except subprocess.CalledProcessError as e:
            print(f"Failed to create mailing list '{name}'.")
            print("Error:")
            print(e.output)
        
        print("------------------------")