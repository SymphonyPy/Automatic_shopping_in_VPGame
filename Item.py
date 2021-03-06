import time
import requests
import notification
import personal_account_info


class Item(object):
    def __init__(self, item):
        self.item_id = item["item_id"]
        self.name = item["name"]
        self.rarity = item["rarity"]
        self.slot = item["slot"]
        self.type = item["type"]
        self.hero = item["hero"]
        self.price = item["price"]
        self.market_price = item["market_price"]
        self.pro_price = item["pro_price"]
        self.inventory = item["inventory"]
        self.discount = item["discount"]
        self.sell_num = item["sell_num"]
        self.id = item["id"]

    def get_sell_list(self):
        """{
                "user_id": "1",
                "product_id": "5818996",
                "nickname": "\u6211\u7814\u6211\u7814",
                "level": "94",
                "avatar": "15707f557.png",
                "pro_type": "sell",
                "max_buy_num": 0,
                "inventory": "971",
                "price": "50",
                "market_price": 0,
                "own_inventory": 0
            }"""
        url = "http://www.vpgame.com/webservice/v2/market/product/list?callback=&item_id=" + str(
            self.item_id) + "&type=sell&current_page=1&lang=en_US"
        items = [item for item in requests.get(url).json()["body"]["items"]]
        return items

    def get_buy_list(self):
        """{
                "user_id": "2447978",
                "product_id": "5885272",
                "nickname": "flyingz",
                "level": "19",
                "avatar": "154c4e83c.png",
                "pro_type": "buy",
                "max_buy_num": 0,
                "inventory": 8,
                "price": "2200",
                "market_price": 172800,
                "own_inventory": 0
            }"""
        url = "http://www.vpgame.com/webservice/v2/market/product/list?callback=&item_id=" + str(
            self.item_id) + "&type=buy&current_page=1&lang=en_US"
        try:
            items = [item for item in requests.get(url).json()["body"]["items"]]
        except:
            items = []
        return items

    def get_history_list(self):
        """ {
            "id": "11997109",
            "trade_user": {
                "id": "8554715",
                "nickname": "fuck you",
                "level": "2",
                "avatar": "\/\/thumb.vpgcdn.com\/file\/fb2bcc07fabc4482bd16d37380f0184.jpg"
            },
            "num": "1",
            "type": "sell",
            "price": 30,
            "timestamp": "1478961952",
            "time": "18 mins ago"
        }"""
        url = "http://www.vpgame.com/webservice/v2/market/product/history?callback=&item_id=" + str(
            self.item_id) + "&lang=en_US"
        try:
            events = [event for event in requests.get(url).json()["body"]]
        except:
            events = []
        return events

    def buy(self, product_id, number, session_id, session):
        url = "http://www.vpgame.com/webservice/v2/market/product/buy"
        data = {
            "product_id": product_id,
            "num": number,
            "password": personal_account_info.VPGame_account["trade_password"],
            "session": session_id,
            "lang": "en_US"
        }
        session.post(url, data=data)

    def operate(self, user, wechat_SCKEY=0):
        try:
            buy_list = self.get_buy_list()
        except:
            buy_list = []
            print("Failed to call get_buy_list")
            print(str(time.strftime('%H:%M:%S', time.localtime(time.time()))))
            time.sleep(5)
        try:
            sell_list = self.get_sell_list()
        except:
            sell_list = []
            print("Failed to call get_sell_list")
            print(str(time.strftime('%H:%M:%S', time.localtime(time.time()))))
            time.sleep(5)
        if buy_list:
            for item in buy_list:
                if int(item["inventory"]) > 0:
                    highest_buy_price = float(item["price"])
                    break
        else:
            highest_buy_price = 0
        for item in sell_list:
            buy_reason = 0
            if int(item["price"]) <= 20:
                buy_reason = "price <= 20 "
            elif highest_buy_price != 0:
                if float(item["price"]) * 1.1 <= highest_buy_price * 0.95:
                    buy_reason = "price << highest buy price"
            elif int(item["price"]) <= self.market_price * 0.95 * 0.75:
                history_list = self.get_history_list()
                lower = 0
                for event in history_list:
                    if float(item["price"]) <= (float(event["price"]) / float(event["num"])) * 0.95 * 0.75:
                        lower += 1
                if lower >= 6:
                    buy_reason = "price << market_price"
            # elif 100000 <= int(item["price"]) <= self.market_price:
            #     buy_reason = "Reasonable luxury"
            if buy_reason:
                try:
                    gold = user.get_gold()
                except:
                    gold = 200000
                    print("Failed to call user.get_gold.")
                    print(str(time.strftime('%H:%M:%S', time.localtime(time.time()))))
                    time.sleep(5)
                amount = min((gold / int(item["price"]), item["inventory"]))
                print("name:{}\tprice:{}\tinventory:{}".format(self.name, self.price, self.inventory))
                print("slot:{}\ttype:{}\thero:{}".format(self.slot, self.type, self.hero))
                print(buy_reason + "\n")
                self.buy(item["product_id"], amount, user.info["session_id"], user.session)
                # if pushbullet_access_token:
                #     try:
                #         notification.pushbullet(self, buy_reason, pushbullet_access_token)
                #     except:
                #         print("Failed to call notification.pushbullet.")
                #         print(str(time.strftime('%H:%M:%S', time.localtime(time.time()))))
                #         time.sleep(5)
                if wechat_SCKEY:
                    try:
                        notification.wechat(self, buy_reason, wechat_SCKEY)
                    except:
                        print("Failed to call notification.wechat.")
                        print(str(time.strftime('%H:%M:%S', time.localtime(time.time()))))
                        time.sleep(5)
            else:
                break
