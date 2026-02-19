from dotenv import load_dotenv
load_dotenv()
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import os
import requests
import re
from collections import Counter

# CONFIGURING (RapidAPI)
RAPID_API_KEY = os.getenv("RAPID_API_KEY")  # Set this in your environment
RAPIDAPI_HOST = "rapid-translate-multi-traduction.p.rapidapi.com"

if not RAPID_API_KEY:
    raise Exception("RAPID_API_KEY not found. Please set it as an environment variable.")

# SETUP SELENIUM
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 20)
translated_titles = []

# TRANSLATION FUNCTION
def translate_to_english(text):
    url = "https://rapid-translate-multi-traduction.p.rapidapi.com/t"
    payload = {
        "from": "es",
        "to": "en",
        "q": [text]
    }
    headers = {
        "Content-Type": "application/json",
        "X-RapidAPI-Host": RAPIDAPI_HOST,
        "X-RapidAPI-Key": RAPID_API_KEY
    }

    res = requests.post(url, json=payload, headers=headers, timeout=30)
    res.raise_for_status()
    data = res.json()
    return data[0]

# OPEN EL PAÍS
driver.get("https://elpais.com")

# Accept cookies if popup appears
try:
    accept_btn = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//button[contains(., 'Aceptar') or contains(., 'Aceptar todo') or contains(., 'Aceptar y continuar') or contains(., 'Accept')]"
    )))
    accept_btn.click()
    time.sleep(2)
except:
    pass

# Click "Opinión"
opinion_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Opinión')]")))
driver.execute_script("arguments[0].click();", opinion_link)
time.sleep(5)

# Ensure images folder exists
os.makedirs("images", exist_ok=True)

print("\n--- First 5 Opinion Articles (Spanish) ---\n")

# SCRAPE FIRST 5 ARTICLES
for idx in range(1, 6):
    try:
        # Refetch links each loop to avoid stale elements
        links = wait.until(EC.presence_of_all_elements_located((
            By.XPATH, "//article//h2//a | //article//h3//a"
        )))
        link = links[idx - 1]

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
        wait.until(EC.element_to_be_clickable(link))
        driver.execute_script("arguments[0].click();", link)

        # Get title and content
        title_es = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1"))).text
        paragraphs = driver.find_elements(By.XPATH, "//p")
        content_es = "\n".join([p.text for p in paragraphs[:5]])

        print(f"\nArticle {idx} Title (ES): {title_es}")
        print(f"Content (ES):\n{content_es}\n")

        # Download cover image (Only if available)
        try:
            img = driver.find_element(By.XPATH, "//figure//img")
            img_url = img.get_attribute("src")
            img_data = requests.get(img_url, timeout=15).content
            with open(f"images/article_{idx}.jpg", "wb") as f:
                f.write(img_data)
            print(f"Saved image: images/article_{idx}.jpg")
        except:
            print("No cover image found for this article.")

        # Translate title
        translated = translate_to_english(title_es)
        translated_titles.append(translated)
        print(f"Translated Title (EN): {translated}")

        # Go back to opinion page
        driver.back()
        wait.until(EC.presence_of_element_located((By.XPATH, "//article")))
        time.sleep(2)

    except Exception as e:
        print(f"Error processing article {idx}: {e}")
        driver.back()
        time.sleep(2)

driver.quit()

# ANALYZE REPEATED WORDS
all_words = []
for t in translated_titles:
    words = re.findall(r"[a-zA-Z]+", t.lower())
    all_words.extend(words)

counts = Counter(all_words)

print("\n--- Repeated Words (>2 times) in Translated Headers ---\n")
for word, cnt in counts.items():
    if cnt > 2:
        print(f"{word} -> {cnt}")
