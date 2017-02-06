import Item
import time
import login
import random
import requests
import get_info_item
import multiprocessing
import personal_account_info


def for_multi(primary_info, user_info, session, pushbullet_access_token):
    modified_item = Item.Item(primary_info)
    modified_item.operate(user_info=user_info, session=session, pushbullet_access_token=pushbullet_access_token)


if __name__ == '__main__':
    session = requests.session()
    user_info = login.login(personal_account_info.VPGame_account, session=session)
    while True:
        modified_list = []
        pool = multiprocessing.Pool(processes=16)
        try:
            primary_list = get_info_item.get()
            pool.starmap(for_multi, zip(primary_list, [user_info] * 45, [session] * 45,
                                        [personal_account_info.pushbullet_access_token] * 45))
        except:
            print("visit refused!")
            time.sleep(10)
        pool.close()
        random_time = random.random() + 1
        print(random_time)
        print(str(time.strftime('%H:%M:%S', time.localtime(time.time()))) + '\n')
        time.sleep(random_time)
        print("\n\n")
