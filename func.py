import requests
import re
import info
import winsound
import webbrowser
import os
import time


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
        '''"id":"(\d+)","availably":.*?,"status":.*?,"type":.*?,"num":.*?,"price":(.*?),"views":.*?,"inventory":"(.*?)","discount":(.*?),"max_buy_num":(.*?),"description":.*?,"create_time"''')
    content = re.findall(pattern, str(response.content).replace(' ', '').replace('\\n', ''))
    for i in range(0, 15):
        j = 0
        for tag in ['id', 'price', "inventory", "discount", 'max_buy_num']:
            if tag != 'discount':
                info.item_info[i][tag] = int(content[i][j])
            else:
                info.item_info[i][tag] = float(content[i][j])
            j += 1
        if info.item_info[i]['discount'] != 0:
            info.item_info[i]['market_price'] = int(info.item_info[i]['price'] * 10 / info.item_info[i]['discount'])
        else:
            info.item_info[i]['market_price'] = 999999
    return info.item_info


def submit_order(item_info, ignored_item_id_list, request_discount):
    for item in item_info:
        if float(item["discount"]) <= request_discount and item['id'] not in ignored_item_id_list and item[
            'market_price'] >= 1000:
            headers = info.headers
            headers['Referer'] = 'http://market.vpgame.com/product.html?product_id=' + str(item['id'])
            winsound.Beep(600, 500)
            webbrowser.open_new(headers['Referer'])
            ignored_item_id_list.append(item['id'])
            print(
                '价格：%d\t原价：%d\t折扣：%.1f\t数量：%d' % (
                item['price'], item['market_price'], item['discount'], item['inventory']))
            print(headers['Referer'])
            print('当前时间：' + str(time.strftime('%H:%M:%S', time.localtime(time.time()))) + '\n')
