import re
import time
import requests


class User(object):
    def __init__(self, account):
        self.session = requests.session()
        self.info = self.login(account)
        self.check_status = 0

    def login(self, account):
        user_info = {
            "nickname": "",
            "gold": "",
            "level": "",
            "session_id": "",
            "user_id": ""
        }
        homepage_url = "http://www.vpgame.com/"
        login_url = "http://passport.vpgame.com/account/signin"
        sent_url = "http://passport.vpgame.com/account/securitycode"
        verify_url = "http://passport.vpgame.com/account/security"
        data = {
            "account": account["username"],
            "password": account["password"],
            "captcha": ""
        }
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '55',
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            'Host': 'passport.vpgame.com',
            'Origin': 'http://passport.vpgame.com',
            'Referer': 'http://passport.vpgame.com/signin?redirect=http%3A%2F%2Fwww.vpgame.com%2F',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.session.post(login_url, data=data, headers=headers)
        pattern = re.compile(
            '''"nickname":"(.*?)".*?"gold":"(.*?)","level":"(.*?)".*?"session_id":"(.*?)","user_id":"(.*?)"''')
        try:
            html = self.session.get(homepage_url).text
            for i, j in zip(["nickname", "gold", "level", "session_id", "user_id"],
                            re.findall(pattern=pattern, string=str(html))[0]):
                user_info[i] = j
            print(user_info)
            return user_info
        except:
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Content-Length': '0',
                'Host': 'passport.vpgame.com',
                'Origin': 'http://passport.vpgame.com',
                "Proxy-Connection": "keep-alive",
                'Referer': 'http://passport.vpgame.com/signin?redirect=http%3A%2F%2Fwww.vpgame.com%2F',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            }
            print(self.session.post(sent_url, headers=headers).text)
            data = {'account': account["username"], 'verify_code': ''}
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Content-Length': '45',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'passport.vpgame.com',
                'Origin': 'http://passport.vpgame.com',
                'Referer': 'http://passport.vpgame.com/signin?redirect=http%3A%2F%2Fwww.vpgame.com%2F',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
                "X - Requested - With": "XMLHttpRequest"
            }
            data['verify_code'] = input("Verify Code:")
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
            '''"nickname":"(.*?)".*?"gold":"(.*?)","level":"(.*?)".*?"session_id":"(.*?)","user_id":"(.*?)"''')
        html = self.session.get(homepage_url).text
        return re.findall(pattern=pattern, string=str(html))[0][1]

    def check_in(self):
        hour = int(time.strftime('%H', time.localtime(time.time())))
        minute = int(time.strftime('%M', time.localtime(time.time())))
        if hour == 1 and minute == 0 and self.check_status == 0:
            self.check_status = 1
            headers = {
                "Accept": "application/json,text/javascript,*/*; q=0.01",
                "Accept - Encoding": "gzip, deflate",
                "Accept - Language": "zh-CN,zh;q=0.8",
                "Connection": "keep-alive",
                "Host": "www.vpgame.com",
                "Referer": "http://www.vpgame.com/market/product?tab=item",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"
            }
            self.session.get("http://www.vpgame.com/user/default-checkinajax.html", headers=headers)
            return True
        elif hour == 0 and minute == 0 and self.check_status == 1:
            self.check_status = 0
        return False
