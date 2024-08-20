import os

_sun_wsm_session = input("Input your _sun_wsm_session(get it in your browser's cookie):")
user_expires_at = input("Input your user.expires_at(get it in your browser's cookie):")
user_id = input("Input your user.id(get it in your browser's cookie):")
remember_user_token = input("Input your remember_user_token(get it in your browser's cookie):")

INSTALL_PY_DIR = os.path.abspath(os.path.dirname(__file__))

COOKIE_FILE_PATH = f"{INSTALL_PY_DIR}/wsm_cookie.txt"
CRONTAB_CONFIG_PATH = f"{INSTALL_PY_DIR}/crontab.config"

with open(COOKIE_FILE_PATH, "w") as f:
	_cookie = f"_sun_wsm_session={_sun_wsm_session}; user.expires_at={user_expires_at}; user.id={user_id};"
	if remember_user_token:
		_cookie += f" remember_user_token={remember_user_token};"
	f.write(_cookie)
	f.close()
with open(CRONTAB_CONFIG_PATH, "w") as f:
	auto_checkin_sh_path = f"{INSTALL_PY_DIR}/auto_checkin.sh"
	crontab_config = f"45 7,8,16,18 * * 1-5 TZ=Asia/Ho_Chi_Minh {auto_checkin_sh_path}\n"
	f.write(crontab_config)
	f.close()

