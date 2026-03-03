import time
import csv

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

def get_data_from_web():
    driver = None
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomaticonControlled")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59")

        driver = webdriver.Edge()
        wait = WebDriverWait(driver, 10)

        driver.get(r'https://books.toscrape.com/catalogue/page-1.html')

        array_of_data = []

        # data = {
        #     "название":[],
        #     "наличие":[],
        #     "цена":[],
        #     "ссылка":[]
        # }

        while "page-3" not in driver.current_url:
            array_with_data = driver.find_elements("xpath",'//article[@class="product_pod"]')
            for i, data_about_book in enumerate(array_with_data):
                data = dict()
                text = data_about_book.text.split('\n')
                data["name"] = text[0]
                data["price"] = text[1]
                data["availability"] = text[2]
                link_element = data_about_book.find_element(By.CSS_SELECTOR, "h3 a")
                url = link_element.get_attribute("href")
                data["link"] = url
                array_of_data.append(data)

            button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//a[text()="next"]'))
            )
            button.click()
        driver.quit()

        # print(array_of_data)

        return array_of_data
    except Exception as e:
        print(e)
        raise
    finally:
        driver.quit()