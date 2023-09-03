#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
Adapted from https://github.com/ugorsahin/ChatGPT_Automation/blob/main/chatgpt_automation/helpers.py
'''
import re
import subprocess
import logging
import platform

def detect_chrome_version(executable_path=None):

    if executable_path is None:
        out = subprocess.check_output(['google-chrome', '--version'])
    else:
        out = subprocess.check_output([executable_path, '--version'])
    out = re.search(r'(\d+)\.\d+\.\d+\.\d+', out.decode())
    _v = 112
    if not out:
        logging.info('Could\'nt locate chrome version, using default value: 112')
    else:
        _v = int(out.group(1))
        logging.info(f'The version is {_v}')

    return _v


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        print(detect_chrome_version(sys.argv[1]))
    else:
        print(detect_chrome_version())
