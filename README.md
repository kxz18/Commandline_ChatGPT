# Requirements

```bash
pip install -r requirements.txt
```

# Example

```python
from cmd_chatgpt.client import Client

YOUR_USERNAME = ''
YOUR_PASSWORD = ''

client = Client(
    username=YOUR_USERNAME,
    password=YOUR_PASSWORD,
    driver_path='/path/to/your/driver',
    browser_path=None,  # or specify binary executable file of the browser
    driver_type='chrome',
    login_type='Microsoft',
    proxy_server=None # e.g. 'socks5://ip:port'
)

print(client.say('Hello World!'))
```

You can also try the command line interactive demo by:

```bash
python example.py
```

Currently supported driver type:
  - "firefox": Firefox, needs [geckodriver](https://github.com/mozilla/geckodriver/releases).
  - "chrome": Google chrome, needs [chromedriver](https://chromedriver.chromium.org/downloads).

Currently supported login type:
  - "": Normal OpenAI account
  - "Microsoft": Microsoft account

# Acknowledgement

The open-source project [ChatGPT_Automation](https://github.com/ugorsahin/ChatGPT_Automation) helps a lot!
