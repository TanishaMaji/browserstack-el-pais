import os
from selenium import webdriver
from threading import Thread
import time

BROWSERSTACK_USERNAME = os.getenv("BROWSERSTACK_USERNAME")
BROWSERSTACK_ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")

bstack_url = f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

caps = [
    {"browserName": "Chrome", "os": "Windows", "osVersion": "11"},
    {"browserName": "Firefox", "os": "Windows", "osVersion": "10"},
    {"browserName": "Safari", "os": "OS X", "osVersion": "Ventura"},
    {"device": "iPhone 14", "realMobile": True, "os_version": "16"},
    {"device": "Samsung Galaxy S23", "realMobile": True, "os_version": "13"}
]

def run_test(cap):
    cap["name"] = "El Pais Parallel Test"
    driver = webdriver.Remote(
        command_executor=bstack_url,
        desired_capabilities=cap
    )
    driver.get("https://elpais.com")
    time.sleep(5)
    driver.quit()

threads = []
for cap in caps:
    t = Thread(target=run_test, args=(cap,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("✅ BrowserStack parallel run completed")
