# Requirements

```bash
pip install selenium
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
    driver_type='firefox',
    login_type='Microsoft'
)

print(client.say('Hello World!'))
```

Currently supported driver type:
  - firefox

Currently supported login type:
  - Microsoft