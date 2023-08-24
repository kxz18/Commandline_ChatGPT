#!/usr/bin/python
# -*- coding:utf-8 -*-
import logging
from time import sleep

import selenium.common.exceptions as Exceptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def find_button(driver, text):
    buttons = driver.find_elements(By.TAG_NAME, "button")  # 获取所有的按钮元素
    for button in buttons:
        if button.text == text:
            return button
    return None


def find_input(driver, text):
    input_boxes = driver.find_elements(By.TAG_NAME, "input")
    for input_box in input_boxes:
        if input_box.get_attribute("type") == text:
            return input_box
    return None


class Client:

    def __init__(
            self,
            username: str,
            password: str,
            driver_path: str,
            driver_type: str='firefox',
            login_type: str='',
            ) -> None:
        
        self.username = username
        self.password = password
        self.login_type = login_type  # '' / 'Microsoft'
        
        service = Service(executable_path=driver_path)
        if driver_type == 'firefox':
            options = webdriver.FirefoxOptions()
            Driver = webdriver.Firefox
        else:
            raise NotImplementedError(f'driver type {driver_type} not implemented')

        # headless browser
        options.add_argument('--headless')

        # initialize selenium webdriver
        self.driver = Driver(service=service, options=options)

        # constants
        self.login_url = 'https://chat.openai.com/auth/login'
        self.delay = 5 # 5 seconds delay

        # login
        self.login()

    def login(self):
        self.driver.get(self.login_url)
        sleep(self.delay)
        logging.info('Login page loaded')

        # find log in button and click
        login_button = find_button(self.driver, 'Log in')
        login_button.click()
        sleep(self.delay)
        logging.info('Login button clicked')

        if self.login_type == 'Microsoft':
            login_button = find_button(self.driver, 'Continue with Microsoft Account')
            login_button.click()
            sleep(self.delay)
            logging.info('Login with Microsoft account')

            # enter account
            input_account = find_input(self.driver, 'email')
            input_account.send_keys(self.username)
            input_next = find_input(self.driver, 'submit')
            input_next.click()
            sleep(self.delay)
            logging.info('Accound entered')

            # enter password
            input_password = find_input(self.driver, 'password')
            input_password.send_keys(self.password)
            input_signin = find_input(self.driver, 'submit')
            input_signin.click()
            sleep(self.delay)
            logging.info('Password entered')

            # stay sign in option
            input_yes = find_input(self.driver, 'submit')
            input_yes.click()
            sleep(self.delay)
        else:
            raise NotImplementedError(f'Accound type {self.login_type} not implemented')

        # close help
        go_button = find_button(self.driver, "Okay, let’s go")
        if go_button:
            go_button.click()
            sleep(self.delay)
            logging.info('Closed help page')
        logging.info('Log in successfully!')

    def say(self, text):

        # find the input box
        text_area = self.driver.find_elements(By.ID, 'prompt-textarea')[0]
        for each_line in text.split('\n'):
            text_area.send_keys(each_line)
            text_area.send_keys(Keys.SHIFT + Keys.ENTER)
        text_area.send_keys(Keys.RETURN)
        logging.info(f'Text "{text}" sent!')

        try:
            WebDriverWait(self.driver, 15).until_not(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, 'text-2xl')))
            logging.info('Answer ready!')
        except Exceptions.TimeoutException:
            logging.error('Stuck, something wrong')

        answer = self.driver.find_elements(By.CLASS_NAME, 'text-base')[-1]

        return answer.text

    def __del__(self):
        self.driver.quit()
