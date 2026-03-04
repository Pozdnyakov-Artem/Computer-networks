import os
import time
import csv

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

MAIL=os.getenv("MAIL")
PASSWORD=os.getenv("PASSWORD")

options = Options()
options.add_argument('--headless')
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomaticonControlled")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59")

driver = webdriver.Edge()
wait = WebDriverWait(driver, 10)

driver.get(r'https://www.podkablukom.ru/catalog1c/men/')

alert_button = wait.until(EC.presence_of_element_located(('xpath', '//a[@class="button-group-btn yes"]')))
alert_button.click()

input_button = wait.until(EC.element_to_be_clickable(('xpath','//span[text()="Войти "]')))
input_button.click()

mail_field = wait.until(EC.element_to_be_clickable(('xpath', '//input[@name="USER_EMAIL"]')))
mail_field.send_keys(MAIL)

password_field = wait.until(EC.element_to_be_clickable(('xpath', '//input[@name="USER_PASSWORD"]')))
password_field.send_keys(PASSWORD)

enter_button = wait.until(EC.element_to_be_clickable(('xpath', '//input[@name="Login"]')))
enter_button.click()

time.sleep(5)

actions = ActionChains(driver)

catalog = wait.until(EC.element_to_be_clickable(('xpath', '//span[@title="Каталог"]')))
actions.move_to_element(catalog).perform()

men_shoes = wait.until(EC.element_to_be_clickable(('xpath', '//a[@href="/catalog1c/men/" and @title="Мужская обувь"]')))
men_shoes.click()

time.sleep(5)

data = {
    "тип":[],
    "бренд":[],
    "цена":[],
    "скидка":[],
    "ссылка":[]
}

number_page = 2

while f"PAGEN_1={number_page+1}" not in driver.current_url:
    array_with_data = driver.find_elements("xpath",'//article')
    for i, data_about_book in enumerate(array_with_data):

        text = data_about_book.text.split('\n')

        data["скидка"].append(text[0][1:] if '%' in text[0] else None)
        data["тип"].append(text[1] if '%' in text[0] else text[0])
        data["бренд"].append(text[2] if '%' in text[0] else text[1])
        data["цена"].append("".join(text[3].split()[-3:-1]) if '%' in text[0] else "".join(text[2].split()[-3:-1]))

        link_element = data_about_book.find_element('xpath', './/a[@class="unproduct-image-link"]')
        url = link_element.get_attribute("href")

        data["ссылка"].append(url)

    button_next_page = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="btn" and contains(@href, "PAGEN")]')))
    driver.execute_script("arguments[0].click();", button_next_page)
    # button.click()
    # actions.move_to_element(button).click()
driver.quit()

with open('1.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(data.keys())
    writer.writerows(zip(*data.values()))
