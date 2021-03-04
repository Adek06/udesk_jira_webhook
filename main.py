from flask import Flask
from jira import JIRA_CLIENT
from udesk import UDESK_TICKET
app = Flask(__name__)

@app.route('/webhook/jira/issue/<int:issue_id>')
def jira_issue(issue_id: str): 
    j = JIRA_CLIENT()
    data = j.get_issue_by_id(issue_id)
    if j.get_ticket_id(data):
        # TODO: 发送 api 到工单系统
        u = UDESK_TICKET()
    return data

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
