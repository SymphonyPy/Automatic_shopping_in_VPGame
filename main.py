import func
import requests
import time
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
    request_discount = float(input('最高折扣限制（最高为10）：'))
    auto_browser = input("自动打开浏览器（'Y/N'）：")
    notification_by_email = input("通过邮件推送提醒（'Y/N'）:")
    print()
    while (True):
        aimed_item = []
        item_info = func.get_items_info()
        aimed_item = func.judge(item_info, request_discount, ignored_item_id_list, user_info, session)
        func.notification(auto_browser, notification_by_email, aimed_item, personal_account_info.qq_email_account)
        time.sleep(5)
