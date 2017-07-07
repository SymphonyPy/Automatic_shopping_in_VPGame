from User import User
import requests
import time
from personal_account_info import VPGame_account


def get_buy_list(item_id):
    url = "http://www.vpgame.com/webservice/v2/market/product/list?callback=&item_id=" + str(
        item_id) + "&type=buy&current_page=1&lang=en_US"
    items = [item for item in requests.get(url).json()["body"]["items"]]
    return items


def purchase(item_id, price, inventory, password, session_id, session):
    url = "http://www.vpgame.com/webservice/v2/market/purchase/create"
    data = {
        "item_id": item_id,
        "price": price,
        "inventory": inventory,
        "password": password,
        "description": "",
        "lang": "en_US",
        "session": session_id
    }
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        'Host': 'www.vpgame.com',
        'Origin': 'http://www.vpgame.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    print("item_id:" + str(item_id) + "\tprice:" + str(price) + "\tinventory:" + inventory)
    session.post(url, data, headers)


def get_own_purchase_list(session):
    url = "http://www.vpgame.com/webservice/v2/market/store/purchaseProductList?callback=&lang=en_US&appid=0&status=&page=1&page_size=6"
    items = [item for item in session.get(url).json()["body"]["items"]]
    return items


def cancel_purchase(session, session_id, product_id):
    url = "http://www.vpgame.com/webservice/v2/market/purchase/cancel"
    data = {
        "lang": "en_US",
        "session": session_id,
        "product_id": product_id
    }
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        'Host': 'www.vpgame.com',
        'Origin': 'http://www.vpgame.com',
        "Referer": "http: // www.vpgame.com / market / purchase",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    session.post(url, data, headers)


item_id = 3641
number = str(1)
cur_price = 0
highest_price = 633000
user = User(VPGame_account)
while True:
    req = get_buy_list(item_id)
    for i in range(0, len(req) - 1):
        if int(req[i]["price"]) >= highest_price:
            del req[i]
    if int(req[0]["user_id"]) != int(user.info["user_id"]):
        cur_price = int(req[0]["price"]) + 1
        items = get_own_purchase_list(user.session)
        for item in items:
            if int(item["item_id"]) == item_id and int(item["pro_price"]) != cur_price and item["status"][
                "text"] == "purchase":
                cancel_purchase(user.session, user.info["session_id"], item["id"])
        purchase(item_id, cur_price, number, VPGame_account["trade_password"], user.info["session_id"],
                 user.session)
    elif int(req[0]["user_id"]) == int(user.info["user_id"]) and cur_price - int(req[1]["price"]) != 1:
        cur_price = int(req[0]["price"]) + 1
        items = get_own_purchase_list(user.session)
        for item in items:
            if int(item["item_id"]) == item_id and int(item["pro_price"]) != cur_price and item["status"][
                "text"] == "purchase":
                cancel_purchase(user.session, user.info["session_id"], item["id"])
        purchase(item_id, cur_price, number, VPGame_account["trade_password"], user.info["session_id"],
                 user.session)
    print("\t\t\t\t\t\t\t\t", end="\r")
    print("当前价格:" + str(cur_price) + "\t当前时间" + str(time.strftime('%H:%M:%S', time.localtime(time.time()))), end="\r")
    time.sleep(3)
