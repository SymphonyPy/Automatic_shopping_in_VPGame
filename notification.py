import requests


def pushbullet(item, buy_reason, access_token):
    row1 = "name:{}\tprice:{}\tinventory:{}\n".format(item.name, item.price, item.inventory)
    row2 = "slot:{}\ttype:{}\thero:{}\n".format(item.slot, item.type, item.hero)
    row3 = buy_reason + "\n"
    row4 = "http://www.vpgame.com/user/my.html"
    msg = row1 + row2 + row3 + row4
    pushbullet_send(item.name,msg,access_token)


def wechat(item, buy_reason, wechat_SCKEY):
    row1 = "name:{}\tprice:{}\tinventory:{}\n".format(item.name, item.price, item.inventory)
    row2 = "slot:{}\ttype:{}\thero:{}\n".format(item.slot, item.type, item.hero)
    row3 = buy_reason + "\n"
    row4 = "http://www.vpgame.com/user/my.html"
    msg = row1 + row2 + row3 + row4
    wechat_send(item.name, msg, wechat_SCKEY)


def pushbullet_send(title, message, access_token):
    headers = {
        'Access-Token': access_token,
        'Content-Type': 'application/json'
    }
    json = {
        "type": "push",
        "body": message,
        "title": title,
        "type": "note"
    }
    requests.post("https://api.pushbullet.com/v2/pushes", headers=headers, json=json)


def wechat_send(title, message, wechat_SCKEY):
    requests.get("http://sc.ftqq.com/" + wechat_SCKEY + ".send?text=" + str(
        title) + "&desp=" + str(message))
