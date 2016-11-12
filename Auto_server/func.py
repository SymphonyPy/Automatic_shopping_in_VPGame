import requests
import re
import info
import time
import multiprocessing
import personal_account_info
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def login(session, account):
    info.data['Register[username]'] = account['username']
    info.data['Register[password]'] = account['password']
    response = session.post(info.login_url, data=info.data, headers=headers)
    pattern = re.compile(
        '"nickname":"(.*?)","avatar":.*?,"steam_id":.*?,"gold":"(.*?)","level":"(.*?)"},"session_id":"(.*?)","user_id":"(.*?)"')
    try:
        User_info = re.findall(pattern, str(response.text))[0]
        i = 0
        for tag in ['nickname', 'gold', 'level', 'session_id', 'user_id']:
            info.user_info[tag] = User_info[i]
            i += 1
        print('Login sucessfully!\n')
        return info.user_info
    except:
        print('Login failed!')
        return False


def get_items_info(session):
    response = session.get(info.item_info_url, headers=info.user_agent)
    false = 0
    while false == 0:
        try:
            dict = response.json()
            false = 1
        except:
            false = 0
    list = []
    for i in range(0, 50):
        list.append(dict['body']['item'][i])
    return list


def get_item_price_in_steam(item):
    try:
        return requests.get(info.item_info_in_steam_url + item['item']['name'], headers=info.user_agent).json()
    except:
        return False


def zip_arguments(item_info, ignored_item_id_list, request_discount, user_info, session):
    return zip(item_info, [ignored_item_id_list] * len(item_info), [request_discount] * len(item_info),
               [user_info] * len(item_info), [session] * len(item_info))


def zip_arguments_to_buy(item_info, user_info, session):
    return zip(item_info, [user_info] * len(item_info), [session] * len(item_info))


def judge_and_submit_order(item, ignored_item_id_list, request_discount, user_info, session):
    if item['item']['name'] not in personal_account_info.unaimed_item and item['id'] not in ignored_item_id_list:
        if (float(item["discount"]) <= request_discount and item['item']['market_price'] >= 1600) or (
                    item['item']['name'] in personal_account_info.aimed_item) or (item['price'] <= 20):
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
    header = {
        'Accept': 'application / json, text / javascript, * / *; q = 0.01',
        'Accept - Encoding': 'gzip, deflate',
        'Accept - Language': 'zh - CN, zh;q = 0.8',
        'Connection': 'keep - alive',
        'Content - Length': '83',
        'Content - Type': 'application / x - www - form - urlencoded;charset = UTF - 8'
    }
    item['url'] = 'http://market.vpgame.com/product.html?product_id=' + item['id'] + '&num=' + item[
        'inventory']
    order_data = info.order_data
    order_data['product_id'] = item['id']
    order_data['num'] = item['inventory']
    order_data['session'] = user_info['session_id']
    submit_order_url = info.submit_order_url_1 + user_info['user_id'] + info.submit_order_url_2
    print(order_data)
    print(submit_order_url)
    session.post(submit_order_url, data=order_data)


def get_order_list(user_info, session):
    try:
        order_list = session.get(info.management_url + user_info['session_id'], headers=info.user_agent).json()['body'][
            'item']
        return order_list
    except:
        print("Failed to get management info!")
        print(str(time.strftime('%H:%M:%S', time.localtime(time.time()))) + '\n')


def buy(item, user_info, session):
    buy_data = {
        'order_ids[]': '',
        'session': '',
        'lang': 'en_US'
    }
    if (float(item['package'][0]['discount']) <= 2.5 and int(
            item['package'][0]['product']['item']['market_price']) >= 4000) or int(
        item['package'][0]['price']) <= 100 or item['package'][0]['product']['item'][
        'name'] in personal_account_info.aimed_item:
        pay_url = info.submit_order_url_1 + user_info['user_id'] + info.buy_url
        buy_data['order_ids[]'] = item['order']['id']
        buy_data['session'] = user_info['session_id']
        buy_data['trade_password'] = personal_account_info.trade_password
        session.post(pay_url, data=buy_data, headers=info.user_agent)


def notification(aimed_item):
    express_in_CMD(aimed_item)
    email(aimed_item, personal_account_info.qq_email_account)
    # pushbullet(aimed_item, personal_account_info.pushbullet_Access_Token)


def express_in_CMD(aimed_item):
    if (aimed_item != []):
        for item in aimed_item:
            print(item['url'])


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
        message['From'] = Header('预计收入：' + str(income) + 'P豆', 'utf-8')
        message['To'] = Header("My Lord", 'utf-8')
        message['Subject'] = '预计收入：' + str(income) + 'P豆'
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.quit()


def pushbullet(aimed_item, Access_Token):
    if (aimed_item != []):
        msg_list = []
        income = 0
        for item in aimed_item:
            income += (int(item['item']['market_price']) - int(item['price'])) * int(item['inventory'])
            msg_str = 'name:%s\tprice:%s\tmarket_price:%s\tdiscount:%s\tinventory:%s\n%s' % (
                item['item']['name'], item['price'], item['item']['market_price'], item['discount'], item['inventory'],
                item['url'])
            msg_list.append(msg_str)
        msg = '\n\n\n\n'.join(msg_list) + '\n\n\n\n' + info.my_shopping_cart_url
        headers = {
            'Access-Token': Access_Token,
            'Content-Type': 'application/json'
        }
        json = {
            "type": "push",
            "body": msg,
            "title": 'Expect income:' + str(income) + 'P',
            "type": "note"
        }
        requests.post(info.pushbullet_url, headers=headers, json=json)
