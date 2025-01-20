import time
import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from loguru import logger


def download_extenison() -> bool:
    parmas = {
        "response": "redirect",
        "acceptformat": "crx2,crx3",
        "prodversion": "132.0",
        "os": "Linux",
        "arch": "x86-64",
        "nacl_arch": "x86-64",
        "os_arch": "x86-64",
        "x": "id=hajiimgolngmlbglaoheacnejbnnmoco&uc"
    }
    url = "https://clients2.google.com/service/update2/crx"

    logger.info("Starting to download extension.")
    try:
        response = requests.get(url, params=parmas)
        response.raise_for_status()
        with open("./extension.crx", "wb") as file:
            file.write(response.content)
        logger.info("Extension downloaded successfully.")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download extension: {e}")
    return False

def add_cookie_to_localstorage(browser: webdriver) -> bool:
    try:
        with open("token.json", "r") as file:
            value = json.load(file)
    except Exception:
        logger.error("Failed to read the token file.")
        return False
   
    browser.execute_script(f"localStorage.setItem('persist:root', JSON.stringify({value}));")
    return True

def main():
    if not download_extenison():
        exit(1)

    logger.info("Starting the browser.")
    chrome_options = Options()
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")
    chrome_options.add_extension("./extension.crx")
    browser = webdriver.Chrome(options=chrome_options)

    logger.info("Navigating to MyGate dashboard.")
    browser.get("https://app.mygate.network/dashboard")
    logger.info("Trying to login.")
    if not add_cookie_to_localstorage(browser):
        exit(1)

    for i in range(3):
        browser.get("https://app.mygate.network/dashboard")
        try:
            WebDriverWait(browser, timeout=5).until(EC.text_to_be_present_in_element((By.TAG_NAME, "h3"), "Node Status"))
            logger.info("Logged in successfully.")
            break
        except:
            if i == 2:
                logger.error("Failed to login.")
                exit(1)
            logger.info("Trying to login again.")

    logger.info("Starting to earn points.")
    browser.get("chrome-extension://hajiimgolngmlbglaoheacnejbnnmoco/index.html")
    time.sleep(5)

    while True:
        try:
            browser.refresh()
            time.sleep(5)
            today_reward = browser.find_element(By.XPATH, "//div[text()=\"Today's Reward\"]/preceding-sibling::label[1]")
            season_reward = browser.find_element(By.XPATH, "//div[text()=\"Season 0 Reward\"]/preceding-sibling::label[1]")
            logger.info(f"Today's reward: {today_reward.text}, Season reward: {season_reward.text}")
        except NoSuchElementException:
            logger.warning("Failed to get the reward info.")
        time.sleep(600)

    browser.quit()


if __name__ == "__main__":
    main()