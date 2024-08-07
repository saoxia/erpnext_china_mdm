import hashlib
import json
import time
from typing import Any

import requests

class QccResult:

	def __init__(self, code:int=200, message: str='success', data: Any=None) -> None:
		self.code = code
		self.message = message
		self.data = data


class Qcc:

	def __init__(self, app_key: str, secret_key: str, encode = 'utf-8') -> None:
		self.app_key = app_key
		self.secret_key = secret_key
		self.encode = encode

	def get_token(self)->tuple[str, str]:
		timespan = str(int(time.time()))
		token = self.app_key + timespan + self.secret_key
		hl = hashlib.md5()
		hl.update(token.encode(encoding=self.encode))
		token = hl.hexdigest().upper()
		return token, timespan

	def get_header(self)->dict[str, str]:
		token, timespan = self.get_token()
		headers = {'Token': token, 'Timespan': timespan}
		return headers


class QccApi(Qcc):

	def clean_keyword(self, keyword: str):
		if not keyword:
			return None
		keyword = str(keyword).replace(' ', '')
		return keyword

	def get_result(self, response: requests.Response):
		if response.status_code != 200:
			return QccResult(500, f"企查查接口请求失败http code: {response.status_code}")

		result = response.json()
		if result.get("Status") != "200":
			msg = result.get("Message")
			return QccResult(500, f"企查查接口调用失败：{msg}")
		
		return QccResult(200, data=result)

	def http_get(self, url: str, params: dict):
		headers = self.get_header()
		resp =  requests.get(url, headers=headers, params=params)
		return self.get_result(resp)

	def http_post(self, url: str, data: dict):
		pass


class QccApiNameSearch(QccApi):

	def name_search(self, name: str):
		"""
		企业搜索

		:param name: 企业名称（模糊匹配）
		"""
		url = "https://api.qichacha.com/NameSearch/GetList"
		
		name = self.clean_keyword(name)
		if not name: return QccResult(200, data=[])
		
		params = { "key": self.app_key, "searchName": name }
		result = self.http_get(url, params)
		data = result.data.get('Result').get('Data')
		return QccResult(200, data=[i.get("Name") for i in data])


class QccApiEnterpriceVerify(QccApi):

	def enterprice_verify(self, name: str):
		"""
		企业信息核验

		:param name: 搜索关键字（企业名称、统一社会信用代码、注册号）
		"""
		url = "https://api.qichacha.com/EnterpriseInfo/Verify"
		pass
