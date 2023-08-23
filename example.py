#!/usr/bin/python
# -*- coding:utf-8 -*-
from cmd_chatgpt.client import Client

YOUR_USERNAME = ''
YOUR_PASSWORD = ''

client = Client(
    username=YOUR_USERNAME,
    password=YOUR_PASSWORD,
    driver_path='/path/to/your/driver',
    driver_type='firefox',
    login_type='Microsoft'
)

while True:
    user_input = input('You: ')
    if user_input.lower() == 'exit':
        break

    response = client.say(user_input)
    print('ChatGPT:', response)
