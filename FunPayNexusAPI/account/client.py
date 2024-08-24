from bs4 import BeautifulSoup
import requests,aiohttp,json

from typing import Literal, List
from enum import Enum
import re, math

class Bot:
    def __init__(self,golden_key: str,user_agent: str = None,requests_timeout: float|int = 1) -> None:
        from ..exceptions import errors
        

        self.golden_key: str = golden_key
        self.user_agent: str|None = user_agent
        self.requests_timeout: float|int = requests_timeout
        self._exceptions = errors
        self.dispatcher: Dispatcher = Dispatcher(self,timeout=self.requests_timeout)

        response_status = requests.get("https://funpay.com/",headers={
            "cookie": "golden_key=" + self.golden_key,
            "user_agent": self.user_agent
        })

        parser = BeautifulSoup(markup=response_status.text, features="html.parser")
        account_auth_info = json.loads(parser.body["data-app-data"])
        if account_auth_info['userId'] == 0:
            raise self._exceptions.InvalidGoldenKey()
        else:
            self.account_id: int = account_auth_info['userId']
            self.csrf_token: str = account_auth_info['csrf-token']
            self.phpsessid = response_status.cookies.get_dict()['PHPSESSID']

            self._headers = {
                "cookie": "golden_key=" + self.golden_key + ";" + "PHPSESSID=" + self.phpsessid,
                "csrf_token": self.csrf_token,
                "User-Agent": "User-Agent=" + self.user_agent if self.user_agent != None else "",
                "accept": "*/*",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "x-requested-with": "XMLHttpRequest",
            }

    async def _api_requests(self, requests: Literal['GET','POST'] = "GET", 
                                 method: str = "", 
                                 headers: dict = {}, 
                                 payload: dict = {},
                                 cookies: dict = {},
                                 link: str = "") -> None:
        """Метод для создания requests запросов на сервер FunPay
        
        Если GET запрос, то возвращает статус запроса и HTML текст

        Если POST запрос, то возвращает статус запроса
        """

        async with aiohttp.ClientSession() as session_request:
            link_request = "https://funpay.com/" + method if link == "" else link
        
            if headers == {} and cookies == {}:

                self._headers = {
                    "cookie": "golden_key=" + self.golden_key + ";" + "PHPSESSID=" + self.phpsessid,
                    "csrf_token": self.csrf_token,
                    "accept": "application/json, text/javascript, */*; q=0.01",

                }
                headers = self._headers

            if requests.lower() == "get":
                response = await session_request.get(link_request,headers=headers, params=payload)
                status_request = response.status
                html_text = await response.text()
                return [status_request, html_text]
            else:
                response = await session_request.post(link_request, headers=headers,cookies=cookies, data=payload)
                status_request = response.status
                json = {}
                try:
                    json = await response.json()
                except:
                    ...
                return [status_request,json]

class Dispatcher:
    def __init__(self, bot: Bot, timeout: float|int = 1) -> None:
        from ..types import AccountInfo
        self.bot: Bot = bot
        self.timeout_request: int|float = timeout
        self.account = AccountInfo(self.bot)

    async def send_message(self, user_id: int, text: str = "", image_id: str|int = ""):
        """### Описание метода send_message

        Метод send_message предназначен для отправки сообщений пользователям в системе. Он поддерживает отправку как текстовых сообщений, так и сообщений с медиа-контентом, что позволяет пользователю эффективно взаимодействовать с другими участниками.

        #### Параметры:

        - userid (int | str)**: Уникальный идентификатор пользователя, которому будет отправлено сообщение. Может быть представлен как целое число или строка.

        - **text (str, optional)**: Текст сообщения, которое будет отправлено пользователю. По умолчанию пустая строка.

        - **imageid (str | int, optional): Идентификатор медиа-контента (например, изображение), который будет прикреплен к сообщению. Может быть представлен как целое число или строка. По умолчанию пустая строка.

        #### Возвращаемое значение:

        - None: Метод не возвращает значения. Он выполняет действие по отправке сообщения.

        #### Исключения:

        - NoTextToMedia: Выбрасывается, если попытаться отправить медиа-сообщение с прикреплённым текстом.
        """
        csrf_token = await self.account.csrf_token
        my_id = await self.account.id

        if my_id > user_id:
            answer_id = my_id
            awtor_id = user_id
        else:
            awtor_id = my_id
            answer_id = user_id

        if image_id != "":
            image_id = str(image_id)

            data = {
                "request": '{"action":"chat_message","data":{"node":"users-'+str(awtor_id)+'-'+str(answer_id)+'","content":"","image_id":'+image_id+'}}',
                'csrf_token': csrf_token,
            }
            if not text == "":
                raise self.bot._exceptions.NoTextToMedia()
            await self.bot._api_requests("POST", "runner/", payload=data,headers=self.bot._headers)
            return
        else:
          data = {
              "request": '{"action":"chat_message","data":{"node":"users-'+str(awtor_id)+'-'+str(answer_id)+'", "content":"'+str(text)+'"}}',
              'csrf_token': csrf_token,
          }
          await self.bot._api_requests("POST", "runner/", payload=data,headers=self.bot._headers)
    
    async def raising_lots(self, game_id: int, node_id: int, node_ids: list) -> None:
        """### Описание метода raising_lots

        Метод `raising_lots` позволяет пользователю поднять ставку на один или несколько лотов в рамках определенной игры. Этот метод асинхронно отправляет запрос на сервер для обновления ставок, обеспечивая динамичное взаимодействие с платформой.

       #### Параметры:

       - **game_id (int)**: Уникальный идентификатор игры, в рамках которой производится поднятие ставки. Этот идентификатор необходим для корректной идентификации контекста ставки.

       - **node_id (int)**: Идентификатор узла, на который будет повышена ставка. Указывает, к какому конкретному лоту или группе лотов применяется действие.

       - **node_ids (list)**: Список идентификаторов лотов, на которые будет поднята ставка. Каждый элемент списка представляет уникальный идентификатор лота, на который пользователь хочет сделать ставку.

       #### Возвращаемое значение:

       - **None**: Метод не возвращает значения. Он выполняет действие по поднятию ставки на указанные лоты.

       #### Исключения:

       - **Exception**: Метод может выбрасывать исключение, если возникла ошибка при отправке запроса. Это может произойти, например, из-за проблем с сетью или некорректными данными.

       #### Примечания:
        Метод формирует необходимые заголовки и куки для авторизации перед отправкой POST-запроса на сервер.
        Успешное выполнение метода приведет к обновлению ставок на указанные лоты, что позволяет пользователю активно участвовать в процессе торгов.
        """
        headers = {
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "x-requested-with": "XMLHttpRequest"
        }

        cookies = {
            "golden_key": self.bot.golden_key,
            "PHPSESID": self.bot.phpsessid,
            "csrf_token": self.bot.csrf_token
        }

        response = await self.bot._api_requests("POST","lots/raise",payload={
            "game_id": str(game_id),
            "node_id": str(node_id),
            "node_ids[]": [str(event) for event in node_ids]
        },headers=headers,cookies=cookies)
        

    async def parsing_lots(self,offer_id: int) -> dict:
        respone = await self.bot._api_requests("GET",method=f"lots/offer?id={offer_id}")
        parser = BeautifulSoup(respone[1], "html.parser")
        option = parser.find('option')
        value = option['data-content']
        value = float(BeautifulSoup(value, 'html.parser').find('span', class_='payment-value').text.split(" ")[1])

        type_lot = parser.find("div", class_="text-bold").text
        quantity = parser.find_all("div", class_="param-item")[1].div.text.split(" ")[0]
        
        short_description = parser.find_all("div", class_="param-item")

        return {
            "type": type_lot, "quantity": quantity,
            "short_description": short_description[2].div.text, "description": short_description[3].div.text,
        }
    
    
    
    async def parsing_lots_account(self, id: int = None) -> list:
        """Парсит все лоты с определённого аккаунта
        
        Возвращает кортедж с словарями внутри - \n[{'type': 'Очки Steam', 'name': 'Название лота', 'lot_id': 714, 
        'id': 25477194, 'short_descriptions': 'Название лота', 'price': 
        0.100601, 'auto': False}]"""
        respone = await self.bot._api_requests("GET",method=f"users/{await self.account.id if id == None else id}/")
        parser = BeautifulSoup(respone[1], "html.parser")
        lots_list = []

        names = [event.text for event in parser.find_all("div", class_="offer-list-title")]
        lot_fun_pay_ids = [int(re.search(r'lots/(\d+)', event.find("a")['href']).group(1)) for event in parser.find_all("div",class_="offer-list-title")]
        ids = [int(re.search(r"id=(\d+)",event.find("a")['href']).group(1)) for event in parser.find_all("div", class_="tc table-hover table-clickable tc-short showcase-table tc-sortable")]
        short_descriptions = [re.sub(r'\s+', ' ', event.text).strip() for event in parser.find_all("div", class_="tc-desc-text")]
        type_lot = [event.split(",")[0].strip() for event in short_descriptions]
        short_descriptions = [event.split(",")[0].strip() for event in short_descriptions]
        price = [event.get("data-s") for event in parser.find_all("div", class_="tc-price")][1:]
        new_price = []
        for event in price:
            if event == None:
                continue
            else:
                new_price.append(float(event))
        
        price = [float(event) for event in new_price]
        auto = [event for event in parser.find_all("div", class_="sc-offer-icons")]
        
        for count, event in enumerate(lot_fun_pay_ids):
            lot = {
                "type": names[count].replace("\n", ""),
                "name": type_lot[count],
                "lot_id": lot_fun_pay_ids[count],
                "id": ids[count],
                "short_descriptions": short_descriptions[count],
                "price": price[count],
                "auto": False
            }

            if auto != []:
                if auto[count] != []:
                    lot['auto'] = True
            lots_list.append(lot)
        return lots_list

    async def review(self, order_id: str, text: str, rating: Literal[1, 2, 3, 4, 5] = 5) -> str: 
        payload={
            'authorId': self.bot.account_id,
            'text': text,
            'rating': rating,
            'csrf_token': self.bot.csrf_token,
            'orderId': order_id,
        }

        response = await self.bot._api_requests("POST", "orders/review", 
                                                payload=payload, 
                                                )
        if response[0] != 200:
            raise self.bot._exceptions.ReviewError(response, 
                                                   response[1],
                                                   order_id)
        
    async def refund(self, order_id):
        """
        Оформляет возврат заказа с переданным order_id

        :param order_id: ID заказа.
        :type order_id: :obj:`str`
        """

        payload = {
            "id": order_id,
            "csrf_token": self.bot.csrf_token
        }
        response = await self.bot._api_requests("POST", "orders/refund", 
                                                payload=payload,
                                                headers=self.bot._headers)
        if response[1].get("error"):
            raise self.bot._exceptions.RefundError(response, 
                                                   response[1], 
                                                   order_id)
        
