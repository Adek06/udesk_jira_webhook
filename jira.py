import json
import requests
import os
from http_client import HTTP_CLIENT

class JIRA_CLIENT:
    def __init__(self):
      self.domain = os.getenv("JIRA_DOMAIN")
      self.user_email = os.getenv("JIRA_ADMIN_EMAIL")
      self.token = os.getenv("JIRA_TOKEN")
      self.http_client = HTTP_CLIENT().client()
    
    def create_issue(self, info_hash):
        data = {
            "fields": {
                "project": {
                    "key": info_hash["projectKey"]
                },
                "summary": info_hash["summary"],
                "description": info_hash["description"],
                "issuetype": {
                    "name": info_hash["issueType"]
                },
                # customfield 是固定字符，后面的 id 是自定义字段 id
                "customfield_10029": info_hash["ticketID"]
            }
        }
        resp = self.http_client.post(f"{self.domain}/rest/api/2/issue/", json=data, auth=(self.user_email, self.token))
        return resp.json()
    
    def get_ticket_platform(self):
        ...
  
    def get_ticket_id(self, jira_resp_hash):
        ticket_id = jira_resp_hash["fields"].get("customfield_10029")
        return ticket_id
    

    def is_finished(self, jira_resp_hash):
        status_id = jira_resp_hash["fields"]["status"]["id"]
        if status_id == '10002':
            return True
        return False
    

    def get_issue_by_id(self, issue_id):
        resp = self.http_client.get(f"{self.domain}/rest/api/3/issue/{issue_id}", auth=(self.user_email, self.token))
        return resp.json()
    
    def update_issue(self, payload: dict):
        data = {
            "fields": {
                "summary": payload['summary'],
                "description": payload['description']
            }
        }
        resp = self.http_client.put(f"{self.domain}/rest/api/3/issue/", json=data, auth=(self.user_email, self.token))
        return resp.json()
