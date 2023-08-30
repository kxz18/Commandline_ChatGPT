#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import logging
from time import sleep
from random import random

import undetected_chromedriver as uc
import selenium.common.exceptions as Exceptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .helpers import detect_chrome_version


LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(level=LOGLEVEL)


def random_delay(delay):
    rand = random() * 3
    sleep(delay + rand)


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
        
        if driver_type == 'firefox':
            options = webdriver.FirefoxOptions()
        elif driver_type == 'chrome':
            options = uc.ChromeOptions()
        else:
            raise NotImplementedError(f'driver type {driver_type} not implemented')

        # incognito mode
        options.add_argument('--incognito')
        # headless browser
        options.add_argument('--headless')

        # initialize selenium webdriver
        if driver_type == 'firefox':
            # add complete header to bypass cloudflare bot check
            options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/117.0')
            service = webdriver.firefox.service.Service(executable_path=driver_path)
            self.driver = webdriver.Firefox(service=service, options=options)
        elif driver_type == 'chrome':
            self.driver = uc.Chrome(
                driver_executable_path=driver_path,
                options=options,
                headless=True,
                version_main=detect_chrome_version(),
                log_level=10,
            )
            self.driver.set_page_load_timeout(15)
            random_delay(1)

        # constants
        # self.login_url = 'https://chat.openai.com/auth/login'
        self.login_url = 'https://chat.openai.com/auth/login?next=/chat'
        self.delay = 5 # 5 seconds delay

        # login
        self.login()

    def login(self):
        self.driver.get(self.login_url)
        random_delay(self.delay)
        logging.info('Home page loaded')

        # find log in button and click
        login_button = find_button(self.driver, 'Log in')
        login_button.click()
        random_delay(self.delay)
        logging.info('Login button clicked')

        self.wait_verification()

        if self.login_type == '':
            # enter account
            input_account = find_input(self.driver, 'text')
            input_account.send_keys(self.username)
            submit_button = find_button(self.driver, 'Continue')
            submit_button.click()
            random_delay(self.delay)
            logging.info('Accound entered')

            # enter password
            input_password = find_input(self.driver, 'password')
            input_password.send_keys(self.password)
            submit_button = find_button(self.driver, 'Continue')
            submit_button.click()
            random_delay(self.delay)
            logging.info('Password entered')

        elif self.login_type == 'Microsoft':
            login_button = find_button(self.driver, 'Continue with Microsoft Account')
            login_button.click()
            random_delay(self.delay)
            logging.info('Login with Microsoft account')

            # enter account
            input_account = find_input(self.driver, 'email')
            input_account.send_keys(self.username)
            input_next = find_input(self.driver, 'submit')
            input_next.click()
            random_delay(self.delay)
            logging.info('Accound entered')

            # enter password
            input_password = find_input(self.driver, 'password')
            input_password.send_keys(self.password)
            input_signin = find_input(self.driver, 'submit')
            input_signin.click()
            random_delay(self.delay)
            logging.info('Password entered')

            # stay sign in option
            input_yes = find_input(self.driver, 'submit')
            input_yes.click()
            random_delay(self.delay)
        else:
            raise NotImplementedError(f'Accound type {self.login_type} not implemented')

        # close help
        go_button = find_button(self.driver, "Okay, let’s go")
        if go_button:
            go_button.click()
            random_delay(self.delay)
            logging.info('Closed help page')
        logging.info('Log in successfully!')

    def wait_verification(self):

        def check_login_page():
            login_button = self.driver.find_elements(By.XPATH, '//button[//div[text()="Log in"]]')
            return len(login_button) == 0

        while check_login_page():
            verify_button = self.driver.find_elements(By.ID, 'challenge-stage')
            if len(verify_button):
                try:
                    verify_button[0].click()
                    logging.info('Clicked verification button')
                except Exceptions.ElementNotInteractableException:
                    logging.info('Verification button is not present or clickable')
            random_delay(2)
        return

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
