import requests
import re
from bs4 import BeautifulSoup

data = {
    'Register[username]': '',
    'Register[password]': '',
    'Register[rememberMe]': '0',
    'yt0': '登录'
}
header = {
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
}
homepage_url = 'http://www.vpgame.com/'
login_url = 'http://passport.vpgame.com/login.html?redirect=http://www.vpgame.com/'
my_url = 'http://www.vpgame.com/user/my.html'


def login(data, login_url, session):
    data['Register[username]']=input('用户名/邮箱：')
    data['Register[password]']=input('密码：')
    session.post(login_url, data=data)
    r = session.get('http://market.vpgame.com/')
    pattern = re.compile(
        '"id":.*?,"nickname":"(.*?)","level":"(.*?)","exp":.*?,"avatar":.*?,"steam_id":.*?')
    try:
        User_info = re.findall(pattern, str(r.content))[0]
        print('登陆成功！')
        print('用户名：' + User_info[0] + '\n' + '等级：' + User_info[1])
    except:
        print('登录失败')


session = requests.session()
session.headers = header
login(data, login_url, session)
