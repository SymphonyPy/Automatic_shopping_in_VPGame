import func
import requests
import time

if __name__ == '__main__':
    session = requests.session()
    ignored_item_id_list = []
    aimed_item = []
    user_info = {}
    while (True):
        user_info = func.login(session)
        if user_info == False:
            continue
        else:
            break
    request_discount = float(input('最高折扣限制（最高为10）：'))
    auto_browser = input("自动打开浏览器（'Y/N'）：")
    print()
    while (True):
        item_info = func.get_items_info()
        aimed_item = func.judge(item_info, request_discount, ignored_item_id_list)
        func.submit_order(user_info, aimed_item, auto_browser, session)
        time.sleep(5)
