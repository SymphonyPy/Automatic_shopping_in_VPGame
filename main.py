import time
import requests
import notification
import get_info_item
import multiprocessing
from User import User
from Item import Item
from personal_account_info import wechat_SCKEY, VPGame_account


def for_multi(primary_info, user, wechat_SCKEY):
    modified_item = Item(primary_info)
    modified_item.operate(user=user, wechat_SCKEY=wechat_SCKEY)


if __name__ == '__main__':
    have_reported = 0
    user = User(VPGame_account)
    notification.wechat_send("Auto_Assistant启动成功!", str(time.strftime('%H:%M:%S', time.localtime(time.time()))),
                             wechat_SCKEY)
    while True:
        modified_list = []
        try:
            primary_list = get_info_item.get()
        except requests.exceptions.ReadTimeout:
            print("Failed to get items'info.")
            print(str(time.strftime('%H:%M:%S', time.localtime(time.time()))))
            time.sleep(5)
        pool = multiprocessing.Pool(processes=16)
        pool.starmap(for_multi, zip(primary_list, [user] * 45, [wechat_SCKEY] * 45))
        pool.close()
        if user.check_in():
            notification.wechat_send("签到成功!", str(time.strftime('%H:%M:%S', time.localtime(time.time()))), wechat_SCKEY)
        # if int(time.strftime('%H', time.localtime(time.time()))) % 3 == 0 and have_reported == 0:
        try:
            print(user.get_gold())
        except:
            user = User(VPGame_account)
            notification.wechat_send("对话状态更新成功！", str(time.strftime('%H:%M:%S', time.localtime(time.time()))),
                                     wechat_SCKEY)
        #         have_reported = 1
        # elif int(time.strftime('%H', time.localtime(time.time()))) % 3 == 1 and have_reported == 1:
        #     have_reported = 0
