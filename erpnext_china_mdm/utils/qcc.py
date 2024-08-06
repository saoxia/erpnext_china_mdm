import hashlib
import json
import time

import requests

class Qcc:

    def __init__(self, app_key: str, secret_key: str, encode = 'utf-8') -> None:
        self.app_key = app_key
        self.secret_key = secret_key
        self.encode = encode

    def get_token(self):
        timespan = str(int(time.time()))
        token = self.app_key + timespan + self.secret_key
        hl = hashlib.md5()
        hl.update(token.encode(encoding=self.encode))
        token = hl.hexdigest().upper()
        return token, timespan

    def clean_keyword(self, keyword: str):
        if not keyword:
            return None
        keyword = str(keyword).replace(' ', '')
        return keyword

    def name_search(self, name: str):
        url = "https://api.qichacha.com/NameSearch/GetList"
        
        name = self.clean_keyword(name)
        if not name:
            return []
        
        url = url + "?key=" + self.app_key + "&searchName=" + name
        token, timespan = self.get_token()
        headers = {
            'Token': token,
            'Timespan': timespan
        }
        
        resp = requests.get(url, headers=headers)
        
        if resp.status_code != 200:
            return 500, f"企查查接口请求失败http code: {resp.status_code}"
        result = resp.json()
        if result.get("Status") != "200":
            msg = result.get("Message")
            return 500, f"企查查接口调用失败：{msg}"

        data = result.get('Result').get('Data')
        return 200, [i.get("Name") for i in data]


