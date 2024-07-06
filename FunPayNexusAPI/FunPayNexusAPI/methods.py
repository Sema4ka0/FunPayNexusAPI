"""Список всех методов в FunPayAPI"""

from bs4 import BeautifulSoup
import json

from .account import Client
import aiohttp
import re


class ObjectAccount(Client):
    """ObjectAccount - позволяет получить актуальную информацию о вашем аккаунте"""
    def __init__(self,client) -> None:
        self._golden_key = client._golden_key
        self._headers = client._headers


    async def __api_requests(self, reqiest=["post","get"], api_method=str, headers={}, payload={}):
        async with aiohttp.ClientSession() as client:
            if reqiest == "get":
                response = await client.get(api_method,headers=headers,data=payload)
                return [await response.text(),response.status]
            else:
                response = await client.post(api_method,data=payload,headers=headers)
                return [response.status]
    
    @property
    def account_token(self) -> str | None:
        """Вовзращает golden_key вашего аккаунта"""
        return self._golden_key
    
    @property
    async def username(self) -> str | None:
        """Вовзращает никнейм вашего аккаунта"""
        response = await self.__api_requests("get","https://funpay.com",headers=self._headers)
        if response[1] == 200:
            parser = BeautifulSoup(response[0],"html.parser")
            return parser.find("div",class_="user-link-name").text
        
    @property
    async def url(self) -> str | None:
        """Вовзращает ссылку на ваш аккаунт"""
        response = await self.__api_requests("get","https://funpay.com",headers=self._headers)
        if response[1] == 200:
            parser = BeautifulSoup(response[0],"html.parser")
            return parser.find("a",class_="user-link-dropdown")['href']
        
    @property
    async def user_id(self) -> int | None:
        """Вовзращает уникальный идентификатор аккаунта"""
        response = await self.__api_requests("get","https://funpay.com",headers=self._headers)
        if response[1] == 200:
           parser = BeautifulSoup(response[0],"html.parser")
           return int(parser.find("a",class_="user-link-dropdown")['href'].split("/")[4])
        
    @property
    async def csrf_token(self) -> str | None:
        """Вовзращает уникальный токен аккаунта с страницы FunPay"""
        respone = await self.__api_requests("get","https://funpay.com",headers=self._headers)
        parser = BeautifulSoup(respone[0],"html.parser")
        info_crsf_token = json.loads(parser.body["data-app-data"])
        if info_crsf_token != None:
           return info_crsf_token['csrf-token']
        
    @property
    async def balans(self) -> list | None:
        """Вовзращает список с балансом на аккаунте\nФормат: [0.0, 0.0, 0.0], [рубли, доллары, евро]"""
        response = await self.__api_requests("get","https://funpay.com/account/balance",headers=self._headers)
        if response[1] == 200:
           parser = BeautifulSoup(response[0],"html.parser")
           info_balanse = parser.find_all("span",class_="balances-value")
           if info_balanse != []:
               list_balanse = []
               for event in info_balanse:
                   list_balanse.append(float(event.text.split(" ")[0])) 
               return list_balanse
           else:
               return []
        
        
    @property
    async def reg_date(self) -> str | None:
        """Вовзращает дату регистрации аккаунта"""
        response = await self.__api_requests("get",f"https://funpay.com/users/{await self.user_id}/",headers=self._headers)
        if response[1] == 200:
           parser = BeautifulSoup(response[0],"html.parser")
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
           else:
               return None
           
    @property   
    async def account_operation(self) -> list | None:
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
        respone = await self.__api_requests("get","https://funpay.com/account/balance",headers=self._headers)
        if respone[1] == 200:
            parser = BeautifulSoup(respone[0],"html.parser")
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
            
    