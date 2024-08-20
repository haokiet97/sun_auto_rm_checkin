import os

import requests
from lxml import html
from datetime import datetime
import pytz


class WsmSession(requests.Session):
    def __init__(
        self,
        login_get_url,
        login_post_url,
        wsm_url,
        check_in_url,
        cookie_file_path="wsm_cookie.txt",
    ):
        super().__init__()
        self.login_get_url = login_get_url
        self.login_post_url = login_post_url
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
        assert self.request_cookie or self.cookies, "ERROR! do not have wsm cookie"
        if not self.cookies:
            headers = {"cookie": self.request_cookie}
            get_res = self.get(self.wsm_url, headers=headers)
        else:
            get_res = self.get(self.wsm_url)
        res_content = get_res.content
        tree = html.fromstring(res_content)
        authenticity_token_ar = tree.xpath('//input[@name="authenticity_token"]/@value')
        self.authenticity_token = (
            authenticity_token_ar[0] if authenticity_token_ar else None
        )

    def check_in_out(self):
        if not self.authenticity_token:
            self.write_logs(
                "ERROR! do not have authenticity_token. (checkin btn not found!)"
            )
            return
        form_data = {"authenticity_token": self.authenticity_token}
        res = self.post(self.check_in_url, data=form_data)
        if not os.getenv("FOR_GIT_ACTION", False):
            self.export_cookie_to_file()
            if "success" not in res.text:
                self.write_logs("checkin btn FOUND, FAILED! please check WSM!")
            self.write_logs(f"OK! please check WSM! {res.text}")

    def write_logs(self, message: str):
        with open("logs.txt", "w+") as f:
            vn_zone = pytz.timezone("Asia/Ho_Chi_Minh")
            f.write(f"######################\n# {datetime.now(vn_zone)}: {message}\n")
            f.close()

    def login(self):
        WSM_EMAIL = os.getenv("WSM_EMAIL")
        WSM_PASSWORD = os.getenv("WSM_PASSWORD")
        FOR_GIT_ACTION = os.getenv("FOR_GIT_ACTION", False)
        if WSM_EMAIL and WSM_PASSWORD:
            login_page = self.get(self.login_get_url)
            self.cookies = login_page.cookies
            login_tree = html.fromstring(login_page.content)
            authenticity_token_ar = login_tree.xpath(
                '//form[@id="devise-login-form"]//input[@name="authenticity_token"]/@value'
            )
            authenticity_token = (
                authenticity_token_ar[0] if authenticity_token_ar else None
            )
            login_form_data = {
                "utf8": "✓",
                "authenticity_token": f"{authenticity_token}",  # Replace with the actual token
                "user[token_core_value]": "",
                "user[email]": WSM_EMAIL,
                "user[password]": WSM_PASSWORD,
                "user[remember_me]": "1",
            }
            response = self.post(self.login_post_url, data=login_form_data)
            res_json = response.json()
            if "success" not in res_json:
                if not FOR_GIT_ACTION:
                    self.import_cookie_from_file()
            self.cookies = response.cookies

        elif not FOR_GIT_ACTION:
            self.import_cookie_from_file()
        else:
            self.request_cookie = os.getenv("WSM_COOKIE")


wsm_url = """https://wsm.sun-asterisk.vn/en/dashboard/user_timesheets"""
check_in_url = """https://wsm.sun-asterisk.vn/en/dashboard/checkin_remotes"""
login_get_url = """https://wsm.sun-asterisk.vn/vi"""
login_post_url = """https://wsm.sun-asterisk.vn/en/users/sign_in"""

if __name__ == "__main__":
    wsm_cookie_file_path = f"{os.path.abspath(os.path.dirname(__file__))}/wsm_cookie.txt"
    session = WsmSession(
        login_get_url=login_get_url,
        login_post_url=login_post_url,
        wsm_url=wsm_url,
        check_in_url=check_in_url,
        cookie_file_path=wsm_cookie_file_path,
    )
    session.login()
    # get authenticity_token for checkin/out
    session.get_authenticity_token()
    # check in/out
    session.check_in_out()
