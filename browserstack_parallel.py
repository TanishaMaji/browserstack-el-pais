import os
import time
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

BROWSERSTACK_USERNAME = os.getenv("BROWSERSTACK_USERNAME")
BROWSERSTACK_ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")

bstack_url = f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

capabilities_list = [
    {
        "browser": "Chrome",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "11",
            "sessionName": "El Pais - Chrome",
            "buildName": "El Pais Parallel Build"
        }
    },
    {
        "browser": "Firefox",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "10",
            "sessionName": "El Pais - Firefox",
            "buildName": "El Pais Parallel Build"
        }
    },
    {
        "browser": "Safari",
        "bstack:options": {
            "os": "OS X",
            "osVersion": "Ventura",
            "sessionName": "El Pais - Safari",
            "buildName": "El Pais Parallel Build"
        }
    },
    {
        "browser": "iPhone",
        "bstack:options": {
            "deviceName": "iPhone 14",
            "realMobile": "true",
            "osVersion": "16",
            "sessionName": "El Pais - iPhone",
            "buildName": "El Pais Parallel Build"
        }
    },
    {
        "browser": "Android",
        "bstack:options": {
            "deviceName": "Samsung Galaxy S23",
            "realMobile": "true",
            "osVersion": "13",
            "sessionName": "El Pais - Android",
            "buildName": "El Pais Parallel Build"
        }
    }
]

def run_test(cap):
    try:
        options = ChromeOptions()
        options.set_capability("browserName", cap["browser"])
        options.set_capability("bstack:options", cap["bstack:options"])

        driver = webdriver.Remote(
            command_executor=bstack_url,
            options=options
        )
        driver.get("https://elpais.com")
        time.sleep(5)
        driver.quit()
        print("✅ Session completed:", cap["browser"])
    except Exception as e:
        print("❌ Session failed:", cap["browser"], "|", e)

threads = []
for cap in capabilities_list:
    t = Thread(target=run_test, args=(cap,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("🎉 BrowserStack parallel run completed")
