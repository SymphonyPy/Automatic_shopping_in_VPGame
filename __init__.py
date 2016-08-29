import func
import requests
import time

session = requests.session()
ignored_item_id_list = []
while (not func.login(session)):
    continue
while (True):
    item_info = func.get_items_info()
    func.submit_order(item_info, ignored_item_id_list)
    time.sleep(5)
