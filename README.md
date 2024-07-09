<h1 align="center"> FunPay Nexus API </h1>
<h3 align="center">  библиотека для взаимодействия с сайтом funpay.com, предоставляющая удобные методы работы с аккаунтом. </h3>

<h1 align="center"> Важные ссылки</h1>
<h4 align="center">
    <a href="https://t.me/FunPayNexus">Telegram канал</a><br>
<h4 align="center">
    <a href="https://t.me/FunPayNexus_chat">Telegram чат</a><br>
<h4 align="center">
    <a href="https://github.com/Sema4ka0/FunPayNexusAPI">GitHub</a><br>
<h4 align="center">
    <a href="https://pypi.org/project/FunPayNexusAPI/">PyPi</a><br>

## Установка
Установка библиотеки:
```bash
pip install FunPayNexusAPI
```
## Пример использования

### Получение информации о профиле

Ниже приведены несколько примеров с использованием FunPayNexusAPI

```python
from FunPayNexusAPI.account import Client
from FunPayNexusAPI.methods import ObjectAccount
import asyncio

# Вводим golden_key и user_agent
golden_key = "golden_key аккаунта"
user_agent = "ваш user_agent" 

# инициализируем аккаунт
client = Client(golden_key=golden_key, user_agent=user_agent)
account = ObjectAccount(client)

async def info_handler() -> None:
    username = await account.username
    user_id = await account.user_id
    url_account = await account.url
    balance = await account.balance
    print(f"username: {username}\nID: {user_id}\nurl: {url_account}\nbalance: {balance[0]}₽ {balance[1]}$ {balance[2]}€")
    
async def main() -> None:
    await info_handler()

if __name__ == "__main__":
    asyncio.run(main())
```

### Получение непрочитанных чатов на аккунте

```python
from FunPayNexusAPI.account import Client
from FunPayNexusAPI.methods import ObjectAccount
import asyncio

# Вводим golden_key и user_agent
golden_key = "golden_key аккаунта"
user_agent = "ваш user_agent" 

# инициализируем аккаунт
client = Client(golden_key=golden_key, user_agent=user_agent)
account = ObjectAccount(client)

async def func():
    a = await account.get_new_messages
    print(a)

async def main():
    await func()

if __name__ == "__main__":
    asyncio.run(main())
```
### Отправление сообщения в чат

```python
from FunPayNexusAPI.account import Client
from FunPayNexusAPI.methods import ObjectAccount
import asyncio

# Вводим golden_key и user_agent
golden_key = "golden_key аккаунта"
user_agent = "ваш user_agent" 

# инициализируем аккаунт
client = Client(golden_key=golden_key, user_agent=user_agent)
account = ObjectAccount(client)

user_id = 'айди аккаунта собеседника'
mess = 'текст сообщения'

async def func():
    await account.send_message(user_id, mess)

async def main():
    await func()

if __name__ == "__main__":
    asyncio.run(main())
```
## Описание классов и методов

### account.py

Этот модуль содержит класс `Client`, который используется для подключения к аккаунту FunPay.

### methods.py

Этот модуль содержит класс `ObjectAccount`, который предоставляет методы для взаимодействия с аккаунтом.

## Заключение
Проект находится в самом начале своего развития, и активно разрабатывается, вскоре будет добавлен новый функционал, по надобности обновлен старый.
