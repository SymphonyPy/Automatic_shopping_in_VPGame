import Item
import time
import login
import random
import requests
import get_info_item
import multiprocessing
import personal_account_info


def for_multi(primary_info, user_info, session):
    modified_item = Item.Item(primary_info)
    modified_item.operate(user_info=user_info, session=session)


if __name__ == '__main__':
    session = requests.session()
    user_info = login.login(personal_account_info.VPGame_account, session=session)
    while True:
        modified_list = []
        primary_list = get_info_item.get()
        pool = multiprocessing.Pool(processes=16)
        pool.starmap(for_multi, zip(primary_list, [user_info] * 30, [session] * 30))
        pool.close()
        random_time = random.random() + 1
        print(random_time)
        print(str(time.strftime('%H:%M:%S', time.localtime(time.time()))) + '\n')
        time.sleep(random_time)
        print("\n\n")
