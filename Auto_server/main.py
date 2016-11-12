import func
import requests
import random
import time
import login
import multiprocessing

if __name__ == '__main__':
    session = requests.session()
    ignored_item_id_list = []
    aimed_item = []
    user_info = {}
    while (True):
        request_discount = 7.5
        user_info = login.login(session)
        while (True):
            aimed_item = []
            if len(ignored_item_id_list) >= 100:
                ignored_item_id_list = ignored_item_id_list[50:]
            try:
                item_info = func.get_items_info(session)
                data = func.zip_arguments(item_info, ignored_item_id_list, request_discount, user_info, session)
                pool_for_order = multiprocessing.Pool()
                item_info = pool_for_order.starmap(func.judge_and_submit_order, data)
                pool_for_order.close()
                print('Already ordered!')
                for item in item_info:
                    if item != None:
                        ignored_item_id_list.append(item['id'])
                        aimed_item.append(item)
                if aimed_item != []:
                    order_list = func.get_order_list(user_info, session)
                    data = func.zip_arguments_to_buy(order_list, user_info, session)
                    try:
                        pool_for_buy = multiprocessing.Pool()
                        pool_for_buy.starmap(func.buy, data)
                        pool_for_buy.close()
                        print('Already bought!')
                    except:
                        print('Multiprocessing Failed')
                func.notification(aimed_item)
            except:
                print("Internet Failed")
                print(str(time.strftime('%H:%M:%S', time.localtime(time.time()))))
                time.sleep(300)
            randomtime = random.random() * 5 + 1
            print(randomtime)
            print(str(time.strftime('%H:%M:%S', time.localtime(time.time()))) + '\n')
            time.sleep(randomtime)
