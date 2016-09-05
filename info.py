user_info = {
    'nickname': '',
    'gold': '',
    'level': '',
    'session_id': '',
    'user_id': ''
}
data = {
    'Register[username]': '',
    'Register[password]': '',
    'Register[rememberMe]': '0',
    'yt0': '登录'
}
headers = {
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
    'Host': 'market.vpgame.com',
    'Origin': 'http://market.vpgame.com',
    'Referer': ''
}
order_data = {
    'source': 'quick',
    'product_id': '',
    'num': '',
    'session': '',
    'lang': 'zh_CN'
}
item_info = []
for i in range(0, 15):
    item_info.append({
        'id': '',
        'price': '',
        "inventory": '',
        "discount": '',
        'max_buy_num': '',
        'market_price': '',
        "description": ''
    })
login_url = 'http://passport.vpgame.com/login.html?redirect=http://www.vpgame.com/'
item_info_url = 'http://www.vpgame.com/gateway/v1/market/search?callback=&current_page=1&page_size=15&product_type=sell&order_type=update_time'
submit_order_url_1 = 'http://www.vpgame.com/gateway/v1/market/'
submit_order_url_2 = '/order/generate'
