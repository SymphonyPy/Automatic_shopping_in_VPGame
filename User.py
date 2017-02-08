import re
import requests


class User(object):
    def __init__(self, account):
        self.session = requests.session()
        self.info = self.login(account)

    def login(self, account):
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
        self.session.post(login_url, data=data)
        pattern = re.compile(
            '''"nickname":"(.*?)".*?"gold":"(.*?)","level":"(.*?)"}.*?"session_id":"(.*?)","user_id":"(.*?)"''')
        try:
            html = self.session.get(homepage_url).text
            for i, j in zip(["nickname", "gold", "level", "session_id", "user_id"],
                            re.findall(pattern=pattern, string=str(html))[0]):
                user_info[i] = j
            print(user_info)
            return user_info
        except:
            data = {'name': account["username"]}
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Connection': 'keep-alive',
                'Content-Length': '21',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'passport.vpgame.com',
                'Origin': 'http://passport.vpgame.com',
                'Referer': 'http://passport.vpgame.com/login/accountverify.html?redirect=http://passport.vpgame.com/login.html?redirect=http://www.vpgame.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            }
            print(self.session.post(sent_url, data=data, headers=headers).text)
            data = {'email': account["username"], 'verify-code': ''}
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Content-Length': '43',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'passport.vpgame.com',
                'Origin': 'http://passport.vpgame.com',
                'Referer': 'http://passport.vpgame.com/login/accountverify.html?redirect=http://passport.vpgame.com/login.html?redirect=http://www.vpgame.com',
                'pgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
            }
            data['verify-code'] = input("Verify Code:")
            self.session.post(verify_url, data=data, headers=headers)
            html = self.session.get(homepage_url).text
            for i, j in zip(["nickname", "gold", "level", "session_id", "user_id"],
                            re.findall(pattern=pattern, string=str(html))[0]):
                user_info[i] = j
            print(user_info)
            return user_info

    def get_gold(self):
        homepage_url = "http://www.vpgame.com/"
        pattern = re.compile(
            '''"nickname":"(.*?)".*?"gold":"(.*?)","level":"(.*?)"}.*?"session_id":"(.*?)","user_id":"(.*?)"''')
        html = self.session.get(homepage_url).text
        return re.findall(pattern=pattern, string=str(html))[0][1]

    def check_in(self):
        headers = {
            "Host": "www.vpgame.com",
            "Proxy-Connection": "keep-alive",
            "Referer": "http://www.vpgame.com/user/my.html",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        print(self.session.get("http://www.vpgame.com/user/default-checkinajax.html", headers=headers))
