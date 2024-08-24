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
Обновление библиотеки:
```bash
pip install --upgrade FunPayNexusAPI
```
## Пример использования
Ниже приведены несколько примеров с использованием FunPayNexusAPI
### Получение информации о профиле


```python
from FunPayNexusAPI import Bot, Dispatcher
import asyncio

bot = Bot(golden_key="GOLDEN_KEY") # заменяем "GOLDEN_KEY"
dispatcher = Dispatcher(bot)

async def main() -> None:
    account = dispatcher.account
    message = (
        f"username: {await account.username}\n"
        f"user_id: {await account.id}\n"
        f"balance: {await account.balance}\n"
        f"new_message: {len(await account.get_new_messages)}\n"
    )
    print(message)
    
if __name__ == "__main__":
    asyncio.run(main())
```
Заменяем "GOLDEN_KEY" на golden_key вашего аккаунта.
### Отправление сообщения в чат

```python
from FunPayNexusAPI import Bot, Dispatcher
import asyncio

bot = Bot(golden_key="GOLDEN_KEY") # заменяем "GOLDEN_KEY"
dispatcher = Dispatcher(bot)

async def main() -> None:
    await dispatcher.send_message("USER_ID", "Привет!") # заменяем "USER_ID"
    
if __name__ == "__main__":
    asyncio.run(main())
```
Заменяем "GOLDEN_KEY" на golden_key вашего аккаунта.  
Заменяем "USER_ID" на id собеседника.

## Заключение
Проект находится в самом начале своего развития, и активно разрабатывается, вскоре будет добавлен новый функционал, по надобности обновлен старый.

На данный момент нет документации, поэтому по вопросам пишите в чат, указан выше.