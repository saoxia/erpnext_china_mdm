import hashlib
import json
import time

import requests

class Qcc:

    def __init__(self, app_key: str, secret_key: str, url: str, encode = 'utf-8') -> None:
        self.app_key = app_key
        self.secret_key = secret_key
        self.url = url
        self.encode = encode
        self.timespan = str(int(time.time()))
        self.token = self._token()

    def _token(self):
        token = self.app_key + self.timespan + self.secret_key
        hl = hashlib.md5()
        hl.update(token.encode(encoding=self.encode))
        token = hl.hexdigest().upper()
        print('MD5加密后为 ：' + token)
        return token

    def clean_keyword(self, keyword: str):
        if not keyword:
            return False
        keyword = str(keyword).replace(' ', '')
        return keyword

    def request(self, keyword: str):
        keyword = self.clean_keyword(keyword)
        if not keyword:
            return None
        query_param = "searchName=" + keyword
        url = self.url + "?key=" + self.app_key + "&" + query_param
        headers = {
            'Token': self.token,
            'Timespan': self.timespan
        }
        response = requests.get(url, headers=headers)
        result = response.json()
        return result

