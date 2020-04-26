import requests
import re

def prepare_session(s, username, password):
    init_login_req = s.get("https://makaut1.ucanapply.com/smartexam/public/get-login-form?typ=5")
    m = re.search(r"<input name=\\\"_token\\\" type=\\\"hidden\\\" value=\\\"(\S+)\\\">\\n\\t" , init_login_req.text)
    if m:
        token = m.groups()[0]
        login_req = s.post("https://makaut1.ucanapply.com/smartexam/public/checkLogin",
        data={
            "_token" : token,
            "typ": "5",
            "username": username,
            "password": password
        })
        init_activity = s.get("https://makaut1.ucanapply.com/smartexam/public/student/week-report-activity/create")
        resp = init_activity.text
        token_reg = re.search(r"<input name=\"_token\" type=\"hidden\" value=\"(\S+)\">",
        resp
        )
        token = token_reg.groups()[0]
        studentcode_reg = re.search(r"<input id=\"studentcode\" name=\"studentcode\" type=\"hidden\" value=\"(\S+)\">",
        resp
        )
        studentcode = studentcode_reg.groups()[0]
        return [token, studentcode]



# s = requests.Session()
# print(prepare_session(s, "14200118050", "EHUT359"))