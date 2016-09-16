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
order_data = {
    'source': 'quick',
    'product_id': '',
    'num': '',
    'session': '',
    'lang': 'zh_CN'
}
email_headers = ['来生意了！', '出来接客！']
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
item_info_url = 'http://www.vpgame.com/gateway/v1/market/search?callback=&current_page=1&page_size=15&lang=en_US&product_type=sell&order_type=update_time'
item_info_in_steam_url = 'http://steamcommunity.com/market/priceoverview/?appid=570&currency=1&market_hash_name='
submit_order_url_1 = 'http://www.vpgame.com/gateway/v1/market/'
submit_order_url_2 = '/order/generate'
my_shopping_cart_url = 'http://market.vpgame.com/order/manage.html'
