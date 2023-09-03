#!/usr/bin/python
# -*- coding:utf-8 -*-
from cmd_chatgpt.client import Client

YOUR_USERNAME = ''
YOUR_PASSWORD = ''

client = Client(
    username=YOUR_USERNAME,
    password=YOUR_PASSWORD,
    driver_path='/path/to/webdriver',
    browser_path=None,  # or specify binary executable file of the browser
    driver_type='chrome',
    login_type='Microsoft',
    proxy_server=None, # e.g. 'socks5://ip:port'
)

while True:
    user_input = input('You: ')
    if user_input.lower() == 'exit':
        break

    response = client.say(user_input)
    print('AI:', response)
