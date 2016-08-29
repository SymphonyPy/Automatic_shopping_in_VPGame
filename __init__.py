import func
import requests
import time

session = requests.session()
while (not func.login(session)):
    continue
while (True):
    item_info = func.get_items_info()
    func.submit_order(item_info)
    time.sleep(5)
