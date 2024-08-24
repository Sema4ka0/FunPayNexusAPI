from bs4 import BeautifulSoup
from ..account import Bot,Dispatcher
import aiohttp,json,asyncio
import string,random
import datetime, re

import json
from . import utils
from typing import Optional

class AccountInfo:
      def __init__(self, bot: Bot) -> None:
            self.bot: Bot = bot

      @property
      async def username(self) -> str|None:
            """Возвращает username вашего аккаунта, при неудачном получении вернёт None"""
            response = await self.bot._api_requests("GET")
            if response[0] == 200:
                  parser = BeautifulSoup(response[1], "html.parser")
                  return parser.find("div", class_="user-link-name").text
            else:
                  return None
            
      @property
      async def id(self) -> int:
        """Возвращает userId аккаунта"""
        return self.bot.account_id
      
      @property
      def golden_key(self) -> str:
           """Возвращает ваш golden_key"""
           return self.bot.golden_key
      
      @property
      async def csrf_token(self) -> str:
           """Возвращает ваш csrf_token для FunPay"""
           response = await self.bot._api_requests("GET")
           parser = BeautifulSoup(response[1],"html.parser")
           account_info = json.loads(parser.body["data-app-data"])
           return account_info['csrf-token']

      
      @property
      async def phpsessid(self) -> str:
          """ID сессии"""
          return self.bot.phpsessid
      
      @property
      async def url(self) -> str:
           """Возвращает ссылку на ваш аккаунт в FunPay"""
           response = await self.bot._api_requests("GET")
           if response[0] == 200:
            parser = BeautifulSoup(response[1],"html.parser")
            return parser.find("a",class_="user-link-dropdown")['href']
           
      @property
      async def balance(self) -> list:
           """Вовзращает кортедж с балансом на аккаунте\nФормат: {"rub": 0.0, "usd": 0.0, "eur": 0.0}"""
           response = await self.bot._api_requests("GET","account/balance")
           if response[0] == 200:
                parser = BeautifulSoup(response[1],"html.parser")
                info_balance = parser.find_all("span",class_="balances-value")
                if info_balance != []:
                   list_balance = []
                   for currency in info_balance:
                       list_balance.append(float(currency.text.split(" ")[0])) 
                   currency = {"rub": list_balance[0], "usd": list_balance[1], "eur": list_balance[2]}
                   return currency
                
      @property
      async def date_register(self) -> str | None:
        """Вовзращает дату регистрации аккаунта на FunPay"""
        response = await self.bot._api_requests("GET",f"users/{await self.id}/")
        if response[0] == 200:
           parser = BeautifulSoup(response[1],"html.parser")
           info_account = parser.find("div",class_="text-nowrap").text.split(" ")
           if info_account != None:
             datas = []
             for event in info_account:
                 if event == '' or event == "\n":
                     continue
                 else:
                     if "\n" in event:
                        event = event[:5]
                           
                     datas.append(event)
             return f"{datas[0]} {datas[1]} в {datas[2]} | {datas[3]} {datas[4]} {datas[5]}" 
           
      @property   
      async def operation(self) -> list | None:
        """Выводит список со всеми операциями на аккаунте\n\nФормат: 
        [{'date': '23 июня, 8:52 ',
         'time_ago': '2 недели назад',
         'id': '#??????',
         'description': 'Заказ',
         'status': 'Завершено',
         'amount': '200.00', 
         'currency': '₽',
        'type': 'Оплата заказа / Вывод средств'
        }]"""
        respone = await self.bot._api_requests("GET","account/balance")
        if respone[0] == 200:
            parser = BeautifulSoup(respone[1],"html.parser")
            info_operation_list = parser.find_all("div","tc-item transaction-status-complete")
            info_time_operation_list = parser.find_all("span","tc-date-time")
            info_date_operation_list = parser.find_all("span","tc-date-left")

            info_operation_id = parser.find_all("span","tc-title")
            info_operation_status = parser.find_all("div","tc-status transaction-status")
            info_operation_price = parser.find_all("div","tc-price")

            info_operation_unit = parser.find_all("span","unit")
            
            new_info_operation_price = []
            for event in info_operation_price:
                if event.text != "Сумма":
                    new_info_operation_price.append(event)

            new_operation_list = []
            if info_operation_list != []:
              for count,event in enumerate(info_operation_list):
                  if count < len(info_operation_list):
                    new_operation_list.append(
                        {"date": f"{info_time_operation_list[count].text}",
                         "time_ago": f"{info_date_operation_list[count].text}",
                         "id": info_operation_id[count].text.split(" ")[-1:][0],
                         "description": info_operation_id[count].text.split(" ")[:len(info_operation_id[count].text)+1][0],
                         "status": info_operation_status[count].text,
                         "amount": new_info_operation_price[count].text.split(" ")[1],
                         "currency": info_operation_unit[count].text,
                         "type": "Пополнение" if new_info_operation_price[count].text.split(" ")[0] == "+" else "Оплата заказа / Вывод средств"
                         })
              return new_operation_list
            else:
                return []
            
      @property
      async def get_new_messages(self) -> list:
        """
        Выводит список непрочитанных чатов
        Формат:

        [{'data-node-msg': '2362438457', 'data-id': '176409301', 'username': 'Sema4ka0', 'message': 'Привет', 'time': '00:41'}, 
        {'data-node-msg': '2463802041', 'data-id': '156709301', 'username': 'Dirstd', 'message': 'Фотография', 'time': 'вчера'}, 
        {'data-node-msg': '2354308267', 'data-id': '115399301', 'username': 'Defiro4ka', 'message': 'Тут?', 'time': '05.07'}]

        time может быть равен 'вчера' или дате, если сообщения старые
        message может быть равен 'Фотография', всегда равен последнему сообщению в чате
        """

        response = await self.bot._api_requests("GET","chat/")
        if response[0] == 200:
            bs = BeautifulSoup(response[1],"html.parser")
            unred_chats = bs.find_all("a","contact-item unread")
            if unred_chats != []:
                new_message = []
                for count, event in enumerate(unred_chats):
                    new_message.append(
                        {"data-node-msg": event['data-node-msg'],
                         "data-id": event['data-id'],
                         "username": event.find("div", class_="media-user-name").text,
                         "message": event.find("div", class_="contact-item-message").text,
                         "time": event.find("div", class_="contact-item-time").text
                         }
                    )
                return new_message

            else:
                return []
            
      async def payemnts_card_account(self) -> None:
          """Получение привязаных банковских карт к аккаунту"""
          response = await self.bot._api_requests("GET", "")

      async def withdraw(self, currency: utils.Currency, 
                       wallet: utils.WithdrawingМethods, 
                       address: str, amount: int | float,
                       twofactor_code: Optional[str | int ] = None) -> float:
        """
        Функция временно не работает, в силу обновления сайта!
        Функция отправляет запрос на вывод средств.

        :param currency: тип валюты.
        :type currency: :class:`FunPayNexusAPI.types.utils.Currency`

        :param wallet: метод вывода.
        :type wallet: :class:`FunPayNexusAPI.types.utils.WithdrawingМethods`

        :param address: реквизиты заданного метода.
        :type address: :obj:`str`

        :param amount: кол-во средств.
        :type amount: :obj:`int` or :obj:`float`

        :return: кол-во выведенных средств с учетом комиссии сайта.
        :rtype: :obj:`float`
        """
        
        
        currencies = {
            utils.Currency.RUB: "rub",
            utils.Currency.USD: "usd",
            utils.Currency.EUR: "eur"
        }
        wallets = {
            utils.WithdrawingМethods.CARD_RUB: "card_rub",
            utils.WithdrawingМethods.CARD_USD: "card_usd",
            utils.WithdrawingМethods.CARD_EUR: "card_eur",
            utils.WithdrawingМethods.YOUMONEY: "fps",
            utils.WithdrawingМethods.WEBMONEY: "wmz",
            utils.WithdrawingМethods.BINANCE: "binance",
            utils.WithdrawingМethods.TRC: "usdt_trc",
        }
        payload = {
            "csrf_token": self.bot.csrf_token,
            "preview": "",
            "currency_id": currencies[currency],
            "ext_currency_id": wallets[wallet],
            "wallet": address,
            "amount_int": str(amount),
            "twofactor_code": twofactor_code
        }
        response = await self.bot._api_requests("POST", "withdraw/withdraw", 
                                                payload=payload,
                                                headers=self.bot._headers)
        if response[1].get("error"):
            raise self.bot._exceptions.WithdrawError(response, 
                                                     response[1])
        return float(response[1])
  
           
      
