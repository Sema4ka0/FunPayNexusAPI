"""Взаимодействие с аккаунтом на FunPay"""
from typing import TYPE_CHECKING, Literal, Any, Optional, IO
from bs4 import BeautifulSoup
import requests
import aiohttp
import json
import time



class Client:
    """Данный класс делает подключение к аккаунту FunPay"""

    def __init__(self, golden_key: str, user_agent: str, requests_timeout=10) -> None:

        self._headers = {
            "cookie": f"golden_key={golden_key}",
            "PHPSESSID": 'PHPSESSID=IdeG2Q8stEqaaw3rH2eM-qXNdKXs1cEe',
            "User-Agent": f"User-Agent={user_agent}"
        }

        response = requests.get("https://funpay.com/",headers=self._headers)
        if response.status_code == 200:
            parser = BeautifulSoup(response.text,"html.parser")

            check_data = parser.body["data-app-data"]
            if "webpush" in check_data:
               self._golden_key: str = golden_key
               self.phpsessid = response.cookies.get_dict()['PHPSESSID']
               self.user_agent = user_agent
               self.requests_timeout = requests_timeout

               self._headers = {
                    "cookie": f"golden_key={golden_key}" + f";PHPSESSID={self.phpsessid}"
               }
            else:
                raise ValueError("Invalid token, double-check its correctness")      
        else:
            raise ValueError(f"[INFO] - error.\ncode error: {response.status_code}")
        
    async def __api_requests(self, reqiest=["post","get"], api_method=str, headers={}, payload={}):
            async with aiohttp.ClientSession() as client:
              if reqiest == "get":
                  response = await client.get(api_method,headers=headers,data=payload)
                  return [await response.text(),response.status]
              else:
                  response = await client.post(api_method,data=payload,headers=headers)
                  return [response.status]