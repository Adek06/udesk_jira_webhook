import hashlib
import time
import uuid
import os
import requests

class YiChuang:
    L3_GROUP_ID         = os.getenv("YICHUANG_L3_GROUP_ID")
    JIRA_ISSUE_FILED_ID = os.getenv("YICHUANG_JIRA_ISSUE_FILED_ID")

    def __init__(self):
        self.sub_domain  = os.getenv("YICHUANG_SUB_DOMAIN")
        self.admin_email = os.getenv("YICHUANG_ADMIN_EMAIL")
        self.token       = os.getenv("YICHUANG_TOKEN")

    def get_ticket(self, ticket_id):
        url = f"https://{self.sub_domain}/apiv2/tickets/{ticket_id}.json"
        resp = self._fetch('GET', url)
        return resp['ticket']

    def update_ticket(self, ticket_id: str, payload: dict):
        if payload.get("issue_id"):
            # TODO：更新自定义字段
            data = {
                "ticket":{
                    "custom_fields": [{"name": self.JIRA_ISSUE_FILED_ID, "value": payload['issue_id']}]
                }
            }
        else:
            data = {
                "ticket": {
                    "subject": payload['subject'],
                    "content": payload.get('content')
                }
            }
        url = f"https://{self.sub_domain}/apiv2/tickets/#{ticket_id}.json"
        resp = self._fetch('PUT', url, json=data)
        ticket = resp['ticket']
        print("更新工单完成")
        return ticket

    def _fetch(self, method: str, url: str, **kwargs) -> dict:
        request_code = {
            'GET':    200,
            'POST':   201,
            'PUT':    200,
            'DELETE': 204
        }

        auth = (self.admin_email, self.token)
        methods = {
            "POST": requests.post,
            "GET":  requests.get,
            "PUT":  requests.put
        }
        http_request = methods[method]
        resp = http_request(url, auth=auth, **kwargs)
        if resp.status_code != request_code[method]:
            print(f"{method}: {url}: {resp.text}")
            raise AssertionError
        return resp.json()

if __name__ == "__main__":
    y = YiChuang()
    y.get_ticket(12)
