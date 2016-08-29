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
    'Referer': 'http://market.vpgame.com/product.html?product_id='
}
item_info = []
for i in range(0, 15):
    item_info.append({
        'id': '',
        'availably': '',
        'price': '',
        "inventory": '',
        "discount": '',
        'max_buy_num': ''
    })
login_url = 'http://passport.vpgame.com/login.html?redirect=http://www.vpgame.com/'
my_url = 'http://www.vpgame.com/user/my.html'
item_info_url = 'http://www.vpgame.com/gateway/v1/market/search?callback=&current_page=1&page_size=15&product_type=sell&order_type=update_time'
submit_order_url = 'http://market.vpgame.com/js/mall/order.payment.js?1.0.0'
