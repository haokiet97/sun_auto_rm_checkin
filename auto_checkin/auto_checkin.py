import os

import requests
from lxml import html
from datetime import datetime
import pytz


class WsmSession(requests.Session):
    def __init__(self, wsm_url, check_in_url, cookie_file_path='wsm_cookie.txt'):
        super().__init__()
        self.wsm_url = wsm_url
        self.check_in_url = check_in_url
        self.cookie_file_path = cookie_file_path
        self.request_cookie = None
        self.authenticity_token = None

    def get_cookie_as_request_string(self):
        rs = ""
        for c in self.cookies:
            rs += f"{c.name}={c.value}; "
        return rs

    def import_cookie_from_file(self):
        with open(self.cookie_file_path, "r") as f:
            self.request_cookie = f.read()
            f.close()

    def export_cookie_to_file(self):
        with open(self.cookie_file_path, "w") as f:
            f.write(self.get_cookie_as_request_string())
            f.close()

    def get_authenticity_token(self):
        assert self.request_cookie, "ERROR! do not have wsm cookie"
        headers = {"cookie": self.request_cookie}
        get_res = self.get(self.wsm_url, headers=headers)
        res_content = get_res.content
        tree = html.fromstring(res_content)
        authenticity_token_ar = tree.xpath('//input[@name="authenticity_token"]/@value')
        self.authenticity_token = authenticity_token_ar[0] if authenticity_token_ar else None

    def check_in_out(self):
        if not self.authenticity_token:
            self.write_logs("ERROR! do not have authenticity_token. (checkin btn not found!)")
            return
        form_data = {'authenticity_token': self.authenticity_token}
        res = self.post(self.check_in_url, data=form_data)
        self.export_cookie_to_file()
        if "success" not in res.text:
            self.write_logs("checkin btn FOUND, FAILED! please check WSM!")
        self.write_logs(f"OK! please check WSM! {res.text}")


    def write_logs(self, message: str):
    	with open("logs.txt", "w+") as f:
    	    vn_zone = pytz.timezone("Asia/Ho_Chi_Minh")
    	    f.write(f"######################\n# {datetime.now(vn_zone)}: {message}\n")
    	    f.close()


wsm_url = '''https://wsm.sun-asterisk.vn/en/dashboard/user_timesheets'''
check_in_url = """https://wsm.sun-asterisk.vn/en/dashboard/checkin_remotes"""

if __name__ == '__main__':
    session = WsmSession(wsm_url, check_in_url)
    FOR_GIT_ACTION = os.getenv("FOR_GIT_ACTION", False)
    if not FOR_GIT_ACTION:
        session.import_cookie_from_file()
    else:
        session.request_cookie = os.getenv("WSM_COOKIE")

    # import cookie from file
    session.import_cookie_from_file()
    # get authenticity_token for checkin/out
    session.get_authenticity_token()
    # check in/out
    session.check_in_out()
