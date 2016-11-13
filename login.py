import re
import requests


def login(account, session=requests.session()):
    data = {
        "Register[username]": account["username"],
        "Register[password]": account["password"],
        "Register[rememberMe]": "",
        "yt0": "登录"
    }
    user_info = {
        "nickname": "",
        "gold": "",
        "level": "",
        "session_id": "",
        "user_id": ""
    }
    homepage_url = "http://www.vpgame.com/"
    login_url = "http://passport.vpgame.com/login.html?redirect=http://www.vpgame.com"
    session.post(login_url, data=data)
    pattern = re.compile(
        '''"nickname":"(.*?)".*?"gold":"(.*?)","level":"(.*?)"}.*?"session_id":"(.*?)","user_id":"(.*?)"''')
    try:
        html = session.get(homepage_url).text
        for i, j in zip(["nickname", "gold", "level", "session_id", "user_id"],
                        re.findall(pattern=pattern, string=str(html))[0]):
            user_info[i] = j
        print(user_info)
        return user_info
    except:
        print("Login failed!")

# login(personal_account_info.VPGame_account)
