# Mailgun CLI Scripts

Python scripts to run bulk operations using mailgun-cli.

## Scripts

### add_members_to_list_bulk.py

Add members to one or more mailing lists.

**Usage:**

```bash
# With command-line arguments
python3 scripts/add_members_to_list_bulk.py list1 list2 list3

# Interactive mode
python3 scripts/add_members_to_list_bulk.py
```

**Interactive example:**

```
Enter mailing list names (one per line, empty line to finish):
List: E11
List: E12
List:

Enter email addresses (one per line, empty line to finish):
Email: user1@email.com
Email: user2@email.com
Email:

Adding 2 member(s) to 2 list(s)...

[E11]
  Adding user1@email.com...
  Adding user2@email.com...

[E12]
  Adding user1@email.com...
  Adding user2@email.com...

Done.
```

### remove_members_from_list_bulk.py

Remove members from one or more mailing lists.

**Usage:**

```bash
# With command-line arguments
python3 scripts/remove_members_from_list_bulk.py list1 list2 list3

# Interactive mode
python3 scripts/remove_members_from_list_bulk.py
```

**Interactive example:**

```
Enter mailing list names (one per line, empty line to finish):
List: E11
List: E12
List:

Enter email addresses to remove (one per line, empty line to finish):
Email: user1@email.com
Email: user2@email.com
Email:

Removing 2 member(s) from 2 list(s)...

[E11]
  Removing user1@email.com...
  Removing user2@email.com...

[E12]
  Removing user1@email.com...
  Removing user2@email.com...

Done.
```

### create_list_bulk.py

Create multiple mailing lists from a text file.

**Usage:**

1. Create a `mailing_lists.txt` file with list names and descriptions (comma-separated):
   ```
   listname1,Description for list 1
   listname2,Description for list 2
   ```

2. Run the script:
   ```bash
   cd scripts
   python3 create_list_bulk.py
   ```
