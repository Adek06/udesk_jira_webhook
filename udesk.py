import hashlib
import time
import uuid
import os
import requests

class UDESK_TICKET:
    def __init__(self):
        self.sub_domain = os.getenv("UDESK_SUB_DOMAIN")
        self.admin_email = os.getenv("UDESK_ADMIN_EMAIL")
        self.token = os.getenv("UDESK_TOKEN")

    def get_sign(self, timestamp: str, nonce: str, sign_version: str = "v2") -> str:
        data = f"{self.admin_email}&{self.token}&{timestamp}&{nonce}&{sign_version}"
        data_sha = hashlib.sha256(data.encode('utf-8')).hexdigest()
        return data_sha

    def get_ticket(self, id):
        url = self._get_api_url(f"tickets/detail") + f"&id={id}"
        resp = requests.get(url)
        ticket = resp.json()
        return ticket['ticket']

    def update_ticket(self, id: str, payload: dict):
        url = self._get_api_url(f"tickets/{id}")
        if payload.get("ticket_id"):
            # TODO：更新自定义字段
            data = {
                "ticket":{
                    ""
                }
            }
        else:
            data = {
                "ticket": {
                    "subject": payload['subject'],
                    "content": payload['content']
                }
            }
        resp = requests.put(url, json=data)
        ticket = resp.json()
        return ticket['ticket']

    def _get_api_url(self, api: str) -> str:
        timestamp = str(time.time()).split('.')[0]
        nonce = str(uuid.uuid4())
        sign_version = "v2"
        sign = self.get_sign(timestamp, nonce)
        url = f"https://{self.sub_domain}.udesk.cn/open_api_v1/{api}?email={self.admin_email}" \
              f"&timestamp={timestamp}&sign={sign}&nonce={nonce}&sign_version={sign_version}"
        return url
