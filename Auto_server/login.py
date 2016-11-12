import re
import info
import personal_account_info

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Content-Length': '125',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'passport.vpgame.com',
    'Origin': 'http://passport.vpgame.com',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
}
headers2 = {
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
headers3 = {
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


def login(session):
    info.data['Register[username]'] = personal_account_info.VPGame_account['username']
    info.data['Register[password]'] = personal_account_info.VPGame_account['password']
    try:
        response = session.post('http://passport.vpgame.com/login.html?redirect=http://www.vpgame.com/user/my.html',
                                data=info.data, headers=headers)
        response = session.get('http://www.vpgame.com/')
        pattern = re.compile(
            '"nickname":"(.*?)","avatar":.*?,"steam_id":.*?,"gold":"(.*?)","level":"(.*?)"},"session_id":"(.*?)","user_id":"(.*?)"')
        User_info = re.findall(pattern, str(response.text))[0]
    except:
        data = {'name': info.data['Register[username]']}
        session.get("http://passport.vpgame.com/login.html?redirect=http://www.vpgame.com")
        session.post('http://passport.vpgame.com/login.html?redirect=http://www.vpgame.com/user/my.html',
                     data=info.data,
                     headers=headers)
        print(session.post("http://passport.vpgame.com/verify/sent.html", data=data, headers=headers2).text)
        data = {'email': info.data['Register[username]'],
                'verify-code': ''}
        data['verify-code'] = input("Verify Code:")
        session.post(
            "http://passport.vpgame.com/login/accountverify.html?redirect=http://passport.vpgame.com/login.html?redirect=http://www.vpgame.com",
            data=data, headers=headers3)
    response = session.get('http://www.vpgame.com/')
    User_info = re.findall(pattern, str(response.text))[0]
    i = 0
    for tag in ['nickname', 'gold', 'level', 'session_id', 'user_id']:
        info.user_info[tag] = User_info[i]
        i += 1
    print(info.user_info)
    return info.user_info
