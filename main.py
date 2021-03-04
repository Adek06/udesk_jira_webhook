from flask import Flask, request
from jira import JIRA_CLIENT
from udesk import UDESK_TICKET

app = Flask(__name__)

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/webhook/jira/issue/<int:issue_id>')
def jira_issue(issue_id: str): 
    j = JIRA_CLIENT()
    data = j.get_issue_by_id(issue_id)
    if not j.get_ticket_id(data):
        return
    u = UDESK_TICKET()
    if j.is_finished(data):
        payload = {
        }
    else:
        payload = {
            "subject": data['fields']['summary'],
            "content": data['fields']['description']['content']['content']['text']
        }
    try:
        u.update_ticket(payload)
    except AssertionError as err:
        print(err)
        return
    return data

@app.route('/webhook/udesk/ticket', methods=['POST'])
def udesk_ticket():
    """
    1. 判断是否分配给 L3。不是则返回
    2. 判断是否存在 jiraIssueID, 存在则仅更新 jira ISSUE, 否则创建 ISSUE, 
       并更新工单的 jiraIssueID 值
    """
    params      = request.json
    ticket_id   = params['ticketID']
    summary     = params['summary']
    description = params['description']

    # L3 以外不工作
    u = UDESK_TICKET()
    try:
        ticket = u.get_ticket(ticket_id)
        if ticket['user_group_name'] != 'L3':
            return ''
    except AssertionError as err:
        print(err)
        return ''

    j = JIRA_CLIENT()
    issue_id = ticket['custom_fields'].get("TextField_206751")
    if issue_id:
        try:
            j.update_issue(issue_id, {
                "summary": summary,
                "description": description
            })
        except AssertionError as err:
            print(err)
            return
    else:
        try:
            t = j.create_issue(request.json)
        except AssertionError as err:
            print(err)
            return ''
            
        issue_id = t.get("id")
        try:
            u.update_ticket(ticket_id, {"issue_id": issue_id})
        except AssertionError as err:
            print(err)
            return ''
    return ''

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
