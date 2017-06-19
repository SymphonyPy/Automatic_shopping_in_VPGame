import requests


def get(lang="en_US", product_type="sell", page_size="45", order_type="update_time", order="desc"):
    url = "http://www.vpgame.com/webservice/v2/market/search/item?callback=&lang=" + lang + "&app_id=570bet=0&product_type=" + product_type + "&current_page=1&page_size=" + page_size + "&order_type=" + order_type + "&order=" + order
    try:
        item = [item for item in requests.get(url).json()["body"]["item"]]
    except:
        item = []
    return item

# print(get())
