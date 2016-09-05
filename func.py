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
    pattern = re.compile(
        '"nickname":"(.*?)","avatar":.*?,"steam_id":.*?,"gold":"(.*?)","level":"(.*?)"},"session_id":"(.*?)","user_id":"(.*?)"')
    os.system('cls')
    try:
        User_info = re.findall(pattern, str(response.content))[0]
        i = 0
        for tag in ['nickname', 'gold', 'level', 'session_id', 'user_id']:
            info.user_info[tag] = User_info[i]
            i += 1
        print('登陆成功！')
        print('用户名：' + info.user_info['nickname'] + '\n' + '等级：' + info.user_info['level'] + '\n' + 'P豆：' +
              info.user_info['gold'])
        return info.user_info
    except:
        print('登录失败')
        return False


def get_items_info():
    response = requests.get(info.item_info_url)
    dict = response.json()
    list = []
    for i in range(0, 15):
        list.append(dict['body']['item'][i])
    return list


def submit_order(user_info, item_info, ignored_item_id_list, request_discount, session):
    for item in item_info:
        if float(item["discount"]) <= request_discount and item['id'] not in ignored_item_id_list and item['item'][
            'market_price'] >= 800:
            headers = info.headers
            headers['Referer'] = 'http://market.vpgame.com/product.html?product_id=' + item['id'] + '&num=' + item[
                'inventory']
            # order_data = info.order_data
            # order_data['product_id'] = str(item['id'])
            # order_data['num'] = str(item['inventory'])
            # order_data['session'] = user_info['session_id']
            # submit_order_url = info.submit_order_url_1 + user_info['user_id'] + info.submit_order_url_2
            # session.post(submit_order_url, data=order_data, headers=headers)
            winsound.Beep(600, 500)
            webbrowser.open_new(headers['Referer'])
            ignored_item_id_list.append(item['id'])
            print('物品名称：%s\t价格：%s\t原价：%s\t折扣：%s\t数量：%s' % (
                item['description'], item['price'], item['item']['market_price'], item['discount'], item['inventory']))
            print(headers['Referer'])
            print('当前时间：' + str(time.strftime('%H:%M:%S', time.localtime(time.time()))) + '\n')
