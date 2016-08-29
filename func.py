import requests
import re
import info
import winsound
import webbrowser
import os


def login(session):
    info.data['Register[username]'] = input('用户名/邮箱：')
    info.data['Register[password]'] = input('密码：')
    response = session.post(info.login_url, data=info.data)
    pattern = re.compile('"nickname":"(.*?)","avatar":.*?,"steam_id":.*?,"gold":"(.*?)","level":"(.*?)"')
    os.system('cls')
    try:
        User_info = re.findall(pattern, str(response.content))[0]
        print('登陆成功！')
        print('用户名：' + User_info[0] + '\n' + '等级：' + User_info[2] + '\n' + 'P豆：' + User_info[1])
        return True

    except:
        print('登录失败')
        return False


def get_items_info():
    response = requests.get(info.item_info_url)
    pattern = re.compile(
        '''"id":"(\d+)","availably":(.*?),"status":.*?,"type":.*?,"num":.*?,"price":(.*?),"views":.*?,"inventory":"(.*?)","discount":(.*?),"max_buy_num":(.*?),"description":.*?,"create_time"''')
    content = re.findall(pattern, str(response.content).replace(' ', '').replace('\\n', ''))
    for i in range(0, 15):
        j = 0
        for tag in ['id', 'availably', 'price', "inventory", "discount", 'max_buy_num']:
            info.item_info[i][tag] = content[i][j]
            j += 1
    return info.item_info


def submit_order(item_info, ignored_item_id_list):
    for item in item_info:
        if float(item["discount"]) < 8.0 and item['id'] not in ignored_item_id_list:
            headers = info.headers
            headers['Referer'] = 'http://market.vpgame.com/product.html?product_id=' + item['id']
            winsound.Beep(600, 500)
            webbrowser.open_new(headers['Referer'])
            ignored_item_id_list.append(item['id'])
            print(headers['Referer'])
