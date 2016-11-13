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
    sent_url = "http://passport.vpgame.com/verify/sent.html"
    verify_url = "http://passport.vpgame.com/login/accountverify.html?redirect=http://passport.vpgame.com/login.html?redirect=http://www.vpgame.com"
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
        data = {'name': account["username"]}
        print(session.post(sent_url, data=data).text)
        data = {'email': account["username"], 'verify-code': ''}
        data['verify-code'] = input("Verify Code:")
        session.post(verify_url, data=data)

# login(personal_account_info.VPGame_account)
