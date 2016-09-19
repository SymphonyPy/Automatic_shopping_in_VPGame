import func
import requests
import time
import msvcrt
import multiprocessing
import personal_account_info

if __name__ == '__main__':
    session = requests.session()
    ignored_item_id_list = []
    aimed_item = []
    user_info = {}
    while (True):
        user_info = func.login(session, personal_account_info.VPGame_account)
        if user_info == False:
            continue
        else:
            break
    while(True):
        request_discount = float(input('最高折扣限制（最高为10）：'))
        auto_browser = input("自动打开浏览器（'Y/N'）：")
        notification_by_email = input("通过邮件推送提醒（'Y/N'）:")
        print()
        while (True):
            aimed_item = []
            pool = multiprocessing.Pool()
            try:
                item_info = func.get_items_info()
                data = func.zip_arguments(item_info, ignored_item_id_list, request_discount, user_info, session)
                item_info = pool.starmap(func.judge_and_submit_order, data)
                for item in item_info:
                    if item != None:
                        ignored_item_id_list.append(item['id'])
                        aimed_item.append(item)
                func.notification(auto_browser, notification_by_email, aimed_item, personal_account_info.qq_email_account)
                pool.close()
            except:
                print("网络连接异常")
                print('当前时间：' + str(time.strftime('%H:%M:%S', time.localtime(time.time()))) + '\n')
            stop = 0
            if (msvcrt.kbhit()):
                if(msvcrt.getch==b'\x1b'):
                    stop = 1
                break
            if(stop == 1):
                break
            time.sleep(5)
