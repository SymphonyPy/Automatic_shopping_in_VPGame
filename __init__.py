import requests
import re
import info
from bs4 import BeautifulSoup


def login(session):
    info.data['Register[username]'] = input('用户名/邮箱：')
    info.data['Register[password]'] = input('密码：')
    response = session.post(info.login_url, data=info.data)
    pattern = re.compile('"nickname":"(.*?)","avatar":.*?,"steam_id":.*?,"gold":"(.*?)","level":"(.*?)"')
    try:
        User_info = re.findall(pattern, str(response.content))[0]
        print('登陆成功！')
        print('用户名：' + User_info[0] + '\n' + '等级：' + User_info[2] + '\n' + 'P豆：' + User_info[1])
        return True

    except:
        print('登录失败')
        return False


def get_items():
    response = requests.get(info.item_info_url)
    pattern = re.compile(
        '''"id":"(\d+)","availably":(.*?),"status":.*?,"type":.*?,"num":.*?,"price":(.*?),"views":.*?,"inventory":"(.*?)","discount":(.*?),"max_buy_num":(.*?),"description":.*?,"create_time"''')
    content = re.findall(pattern, str(response.content).replace(' ', '').replace('\\n', ''))
    print(content)
    for i in range(0, 15):
        j = 0
        for tag in info.item_info[i]:
            info.item_info[i][tag] = content[0][j]
            j += 1
    print(info.item_info[0])


session = requests.session()
if login(session) == True:
    get_items()
