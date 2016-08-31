import func
import requests
import time

if __name__ == '__main__':
    session = requests.session()
    ignored_item_id_list = []
    while (not func.login(session)):
        continue
    request_discount = float(input('最高折扣限制（最高为10）：'))
    print()
    while (True):
        item_info = func.get_items_info()
        func.submit_order(item_info, ignored_item_id_list, request_discount)
        time.sleep(5)
