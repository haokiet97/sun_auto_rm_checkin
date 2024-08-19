_sun_wsm_session = input("Input your _sun_wsm_session(get it in your browser's cookie):")
user_expires_at = input("Input your user.expires_at(get it in your browser's cookie):")
user_id = input("Input your user.id(get it in your browser's cookie):")

COOKIE_FILE_PATH = "wsm_cookie.txt"

with open(COOKIE_FILE_PATH, "w") as f:
	_cookie = f"_sun_wsm_session={_sun_wsm_session}; user.expires_at={user_expires_at}; user.id={user_id};"
	f.write(_cookie)
	f.close()

