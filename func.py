import requests
import re
import info
import winsound
import webbrowser
import os
import time
import random
import smtplib
import personal_account_info
from email.mime.text import MIMEText
from email.header import Header


def login(session, account):
    # info.data['Register[username]'] = input('用户名/邮箱：')
    # info.data['Register[password]'] = input('密码：')
    info.data['Register[username]'] = account['username']
    info.data['Register[password]'] = account['password']
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
    false = 0
    while false == 0:
        try:
            dict = response.json()
            false = 1
        except:
            false = 0
    list = []
    for i in range(0, 30):
        list.append(dict['body']['item'][i])
    return list


def get_item_price_in_steam(item):
    try:
        return requests.get(info.item_info_in_steam_url + item['item']['name']).json()
    except:
        return False


def zip_arguments(item_info, ignored_item_id_list, request_discount, user_info, session):
    return zip(item_info, [ignored_item_id_list] * 30, [request_discount] * 30, [user_info] * 30, [session] * 30)


def judge_and_submit_order(item, ignored_item_id_list, request_discount, user_info, session):
    if (float(item["discount"]) <= request_discount and item['id'] not in ignored_item_id_list and item['item'][
        'market_price'] >= 500) or (
                    item['item']['name'] in personal_account_info.aimed_item and item[
                'id'] not in ignored_item_id_list):
        try:
            item['info_from_steam'] = get_item_price_in_steam(item)
            if float(item['item']['price']) * 0.5 <= float(
                    item['info_from_steam']['lowest_price'].replace('$', '')):
                submit_order(user_info, item, session)
                return item
        except:
            submit_order(user_info, item, session)
            return item


def submit_order(user_info, item, session):
    item['url'] = 'http://market.vpgame.com/product.html?product_id=' + item['id'] + '&num=' + item[
        'inventory']
    order_data = info.order_data
    order_data['product_id'] = item['id']
    order_data['num'] = item['inventory']
    order_data['session'] = user_info['session_id']
    submit_order_url = info.submit_order_url_1 + user_info['user_id'] + info.submit_order_url_2
    session.post(submit_order_url, data=order_data)


def notification(auto_browser, notification_by_email, aimed_item, qq_email_account):
    express_in_CMD(auto_browser, aimed_item)
    if (notification_by_email == 'Y'):
        email(aimed_item, qq_email_account)


def express_in_CMD(auto_browser, aimed_item):
    if (aimed_item != []):
        winsound.Beep(600, 500)
        for item in aimed_item:
            if (auto_browser == 'Y'):
                webbrowser.open_new(item['url'])
            print('物品名称：%s\t价格：%s\t原价：%s\t折扣：%s\t数量：%s' % (
                item['item']['name'], item['price'], item['item']['market_price'], item['discount'], item['inventory']))
            try:
                print('Steam：最低价格：%s\t中位价格：%s\t数量：%s' % (
                    item['info_from_steam']['lowest_price'], item['info_from_steam']['median_price'],
                    item['info_from_steam']['volume']))
            except:
                print('Steam访问过于频繁！')
            print(item['url'])
            print('当前时间：' + str(time.strftime('%H:%M:%S', time.localtime(time.time()))) + '\n')


def email(aimed_item, qq_email_account):
    if (aimed_item != []):
        mail_host = "smtp.qq.com"
        mail_user = qq_email_account['mail_user']
        mail_pass = qq_email_account['mail_pass']
        sender = qq_email_account['mail_user']
        receivers = [qq_email_account['mail_user']]
        msg_list = []
        income = 0
        for item in aimed_item:
            income += (int(item['item']['market_price']) - int(item['price'])) * int(item['inventory'])
            msg_str = '物品名称：%s\t价格：%s\t原价：%s\t折扣：%s\t数量：%s' % (
                item['item']['name'], item['price'], item['item']['market_price'], item['discount'], item['inventory'])
            msg_list.append(msg_str)
        msg = '\n\n\n\n'.join(msg_list) + '\n\n\n\n' + info.my_shopping_cart_url
        message = MIMEText(msg, 'plain', 'utf-8')
        message['From'] = Header(random.choice(info.email_headers), 'utf-8')
        message['To'] = Header("My Lord", 'utf-8')
        message['Subject'] = '预计收入：' + str(income) + 'P豆'
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.quit()
