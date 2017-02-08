import Item
import time
import User
import random
import get_info_item
import multiprocessing
import personal_account_info


def for_multi(primary_info, user, pushbullet_access_token):
    modified_item = Item.Item(primary_info)
    modified_item.operate(user=user, pushbullet_access_token=pushbullet_access_token)


if __name__ == '__main__':
    user = User.User(personal_account_info.VPGame_account)
    while True:
        modified_list = []
        pool = multiprocessing.Pool(processes=16)
        try:
            primary_list = get_info_item.get()
            pool.starmap(for_multi,
                         zip(primary_list, [user] * 45, [personal_account_info.pushbullet_access_token] * 45))
        except:
            print("visit refused!")
            time.sleep(10)
        pool.close()
        if int(time.strftime('%H', time.localtime(time.time()))) == 1 and int(
                time.strftime('%M', time.localtime(time.time()))) == 0 and 0 <= int(
            time.strftime('%S', time.localtime(time.time()))) <= 20:
            user.check_in()
        random_time = random.random() + 1
        print(random_time)
        print(str(time.strftime('%H:%M:%S', time.localtime(time.time()))) + '\n')
        time.sleep(random_time)
        print("\n\n")
