#!/usr/bin/env python3

import argparse
import configparser
import os
import requests
import csv

# Configuration file path
CONFIG_FILE = os.path.expanduser('~/.mailgun-cli.ini')

def create_mailing_list(name, description, domain, api_key):
    mailing_list_url = 'https://api.mailgun.net/v3/lists'
    data = {
        'address': name+'@'+domain,
        'description': description
    }
    response = requests.post(mailing_list_url, auth=('api', api_key), data=data)
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

def delete_mailing_list(address, api_key):
    list_url = f'https://api.mailgun.net/v3/lists/{address}'
    response = requests.delete(list_url, auth=('api', api_key))
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")
    

def add_member(list_name, member_name, member_address, domain, api_key):
    list_address = list_name + "@" + domain
    list_url = f'https://api.mailgun.net/v3/lists/{list_address}/members'
    data = {
        "name": member_name,
        "address": member_address,
    }
    response = requests.post(list_url, auth=('api', api_key), data=data)
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")
    

def add_members_from_csv(list_name, csv_file_path, domain, api_key, ):
    list_address = list_name + "@" + domain
    # Prepare the API endpoint URL
    url = f"https://api.mailgun.net/v3/lists/{list_address}/members.csv"
    
    # Read the CSV file
    with open(csv_file_path, "rb") as csv_file:
        # Prepare the request data
        data = {
            "members": csv_file
        }
        
        # Send the POST request to add members using the CSV file
        response = requests.post(url, files=data, auth=("api", api_key))
        
        # Check the response status code
        if response.status_code == 200:
            print(f"Members added successfully to mailing list: {list_address}")
        else:
            print(f"Failed to add members to mailing list: {list_address}")
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.text}")

def remove_member(list_name, member_address, domain, api_key):
    list_address = list_name + "@" + domain
    base_url = f'https://api.mailgun.net/v3'
    mailing_list_url = f'{base_url}/lists'
    list_url = f'{mailing_list_url}/{list_address}/members/{member_address}'
    response = requests.delete(list_url, auth=('api', api_key))
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

def print_list_members(list_name, domain, api_key):
    list_address = list_name + '@' + domain
    url = "https://api.mailgun.net/v3/lists/" + list_address + "/members"
    response = requests.get(url, auth=('api', api_key))
    if response.status_code == 200:
        print(f"List: {list_address}")
        print(f'Total members: {response.json()["total_count"]}')
        lists = response.json()["items"]
        print(f"Name, Email")
        for mlist in lists:
            print(f"{mlist['name']}, {mlist['address']}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def send_message(list_address, subject, text, domain, api_key):
    base_url = f'https://api.mailgun.net/v3/{domain}'
    mailing_list_url = f'{base_url}/lists'
    list_url = f'{mailing_list_url}/{list_address}/messages'
    data = {
        'from': f'Your Name <mailgun@{domain}>',
        'to': list_address,
        'subject': subject,
        'text': text
    }
    response = requests.post(list_url, auth=('api', api_key), data=data)
    return response.json()

def list_mailing_lists(api_key):
    url = "https://api.mailgun.net/v3/lists"
    auth = ("api", api_key)
    response = requests.get(url, auth=auth)
    
    if response.status_code == 200:
        lists = response.json()["items"]
        for mlist in lists:
            print(f"Address: {mlist['address']}, Description: {mlist['description']}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def load_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config

def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        config.write(file)

def setup_config():
    config = configparser.ConfigParser()
    config['mailgun'] = {
        'domain': input('Enter your Mailgun domain: '),
        'api_key': input('Enter your Mailgun API key: ')
    }
    save_config(config)
    print('Configuration saved.')

def main():
    parser = argparse.ArgumentParser(description='Mailgun Mailing List CLI')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Setup configuration
    setup_parser = subparsers.add_parser('setup', help='Set up Mailgun configuration')

    # Create mailing list
    create_parser = subparsers.add_parser('create', help='Create a new mailing list')
    create_parser.add_argument('name', help='Mailing list name (without the domain part)')
    create_parser.add_argument('description', help='Mailing list description')

    # Create lists from CSV
    # create_csv_parser = subparsers.add_parser('create_from_csv', help='Create mailing lists from a CSV file')
    # create_csv_parser.add_argument('csv_file_path', help='Path to the CSV file containing list data')

    # Delete mailing list
    delete_parser = subparsers.add_parser('delete', help='Delete a mailing list')
    delete_parser.add_argument('address', help='Mailing list address')

    # Add member
    add_parser = subparsers.add_parser('add', help='Add a member to a mailing list')
    add_parser.add_argument('list_name', help='Mailing list name (without the domain part)')
    add_parser.add_argument('member_name', help='Member name')
    add_parser.add_argument('member_address', help='Member email address')

    # Add members from CSV
    add_csv_parser = subparsers.add_parser('add_from_csv', help='Add members to a mailing list from a CSV file')
    add_csv_parser.add_argument('list_name', help='Mailing list name (without the domain part)')
    add_csv_parser.add_argument('csv_file_path', help='Path to the CSV file containing member data')
    
    # Remove member
    remove_parser = subparsers.add_parser('remove', help='Remove a member from a mailing list')
    remove_parser.add_argument('list_address', help='Mailing list address')
    remove_parser.add_argument('member_address', help='Member email address')

    # Print member
    print_parser = subparsers.add_parser('print', help='Get all members from a mailing list')
    print_parser.add_argument('list_name', help='Mailing list name (without the domain part)')
    
    # Send message
    send_parser = subparsers.add_parser('send', help='Send a message to a mailing list')
    send_parser.add_argument('list_address', help='Mailing list address')
    send_parser.add_argument('subject', help='Message subject')
    send_parser.add_argument('text', help='Message text')
    
    # List mailing lists
    list_parser = subparsers.add_parser('list', help='List all mailing lists')

    args = parser.parse_args()

    if args.command == 'setup':
        setup_config()
    else:
        config = load_config()
        if 'mailgun' not in config:
            print('Mailgun configuration not found. Please run `mailgun setup` first.')
            return

        domain = config['mailgun']['domain']
        api_key = config['mailgun']['api_key']

        if args.command == 'create':
            create_mailing_list(args.name, args.description, domain, api_key)
        elif args.command == 'delete':
            delete_mailing_list(args.address, api_key)
        elif args.command == 'add':
            add_member(args.list_name, args.member_name, args.member_address, domain, api_key)
        elif args.command == 'remove':
            remove_member(args.list_address, args.member_address, domain, api_key)
        elif args.command == 'send':
            send_message(args.list_address, args.subject, args.text, domain, api_key)
        elif args.command == 'list' :
            list_mailing_lists(api_key)
        elif args.command == 'print':
            print_list_members(args.list_name, domain, api_key)
        # elif args.command == 'create_from_csv':
        #     create_lists_from_csv(args.csv_file_path, domain, api_key)  
        elif args.command == 'add_from_csv':
            add_members_from_csv(args.list_name, args.csv_file_path, domain, api_key)
            


if __name__ == '__main__':
    main()