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
login_url = 'http://passport.vpgame.com/login.html?redirect=http://www.vpgame.com/'
my_url = 'http://www.vpgame.com/user/my.html'
sell_url = 'http://market.vpgame.com/search.html#/current_page=1&product_type=sell&order_type=update_time&order=desc&nav_key=2-1'


def login(login_url, data, session):
    data['Register[username]'] = input('用户名/邮箱：')
    data['Register[password]'] = input('密码：')
    response = session.post(login_url, data=data)
    pattern = re.compile('"nickname":"(.*?)","avatar":.*?,"steam_id":.*?,"gold":"(.*?)","level":"(.*?)"')
    try:
        User_info = re.findall(pattern, str(response.content))[0]
        print('登陆成功！')
        print('用户名：' + User_info[0] + '\n' + '等级：' + User_info[2] + '\n' + 'P豆：' + User_info[1])

    except:
        print('登录失败')


def shopping(sell_url, session, header):
    response = session.get(sell_url, headers=header)
    soup = BeautifulSoup(response.content)
    print(soup)


session = requests.session()
login(login_url, data, session)
shopping(sell_url, session, header)
