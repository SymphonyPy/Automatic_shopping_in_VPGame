import requests


def pushbullet(item, buy_reason, access_token):
    row1 = "name:{}\tprice:{}\tinventory:{}\n".format(item.name, item.price, item.inventory)
    row2 = "slot:{}\ttype:{}\thero:{}\n".format(item.slot, item.type, item.hero)
    row3 = buy_reason + "\n"
    row4 = "http://www.vpgame.com/user/my.html"
    msg = row1 + row2 + row3 + row4
    headers = {
        'Access-Token': access_token,
        'Content-Type': 'application/json'
    }
    json = {
        "type": "push",
        "body": msg,
        "title": item.name,
        "type": "note"
    }
    requests.post(info.pushbullet_url, headers=headers, json=json)
