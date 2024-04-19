#!/usr/bin/env python3

import argparse
import configparser
import os
import requests

# Configuration file path
CONFIG_FILE = os.path.expanduser('~/.mailgun-cli.ini')

def create_mailing_list(address, name, domain, api_key):
    mailing_list_url = 'https://api.mailgun.net/v3/lists'
    data = {
        'address': address+'@'+domain,
        'name': name
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

def add_member(list_address, member_address, name, domain, api_key):
    base_url = f'https://api.mailgun.net/v3/{domain}'
    mailing_list_url = f'{base_url}/lists'
    list_url = f'{mailing_list_url}/{list_address}/members'
    data = {
        'address': member_address,
        'name': name
    }
    response = requests.post(list_url, auth=('api', api_key), data=data)
    return response.json()

def remove_member(list_address, member_address, domain, api_key):
    base_url = f'https://api.mailgun.net/v3/{domain}'
    mailing_list_url = f'{base_url}/lists'
    list_url = f'{mailing_list_url}/{list_address}/members/{member_address}'
    response = requests.delete(list_url, auth=('api', api_key))
    return response.status_code

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
    create_parser.add_argument('address', help='Mailing list address')
    create_parser.add_argument('name', help='Mailing list name')

    # Delete mailing list
    delete_parser = subparsers.add_parser('delete', help='Delete a mailing list')
    delete_parser.add_argument('address', help='Mailing list address')

    # Add member
    add_parser = subparsers.add_parser('add', help='Add a member to a mailing list')
    add_parser.add_argument('list_address', help='Mailing list address')
    add_parser.add_argument('member_address', help='Member email address')
    add_parser.add_argument('name', help='Member name')

    # Remove member
    remove_parser = subparsers.add_parser('remove', help='Remove a member from a mailing list')
    remove_parser.add_argument('list_address', help='Mailing list address')
    remove_parser.add_argument('member_address', help='Member email address')

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
            create_mailing_list(args.address, args.name, domain, api_key)
        elif args.command == 'delete':
            delete_mailing_list(args.address, api_key)
        elif args.command == 'add':
            add_member(args.list_address, args.member_address, args.name, domain, api_key)
        elif args.command == 'remove':
            remove_member(args.list_address, args.member_address, domain, api_key)
        elif args.command == 'send':
            send_message(args.list_address, args.subject, args.text, domain, api_key)
        elif args.command == 'list' :
            list_mailing_lists(api_key)


if __name__ == '__main__':
    main()