from bs4 import BeautifulSoup
from selenium  import webdriver
import pandas as pd


class CrawlBlinkit:

    def __init__(self, URL, executable_path):
        self.URL = URL
        self.executable_path = executable_path

    def get_data(self):

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(executable_path=self.executable_path, chrome_options=options)
        driver.get(url=self.URL)
        soup = BeautifulSoup(driver.page_source,"lxml")
        
        items_list = []  
        items_grid = soup.find('div', attrs = {'class':'products products--grid'})
        for row in items_grid.findAll('a', attrs = {'class':'product__wrapper'}):            
            name = row.find('div', attrs = {'class':'plp-product__name--box'})
            price = row.find('span', attrs = {'class':'plp-product__price--new'})

            items_list.append({
                "Item name": name.text,
                "Price": str(price.text).replace('₹', 'Rs. ')
            })

        driver.quit()
        items_df = pd.DataFrame(items_list)
        items_df.to_csv('items.csv', index=False)            


if __name__ == '__main__':
    # Paste any blinkit category URL
    URL = "https://blinkit.com/cn/bakery-biscuits/cookies/cid/888/28"
    
    # Chrome driver to support selenium driver https://sites.google.com/chromium.org/driver/downloads?authuser=0
    executable_path = "C:\chromedriver_win32\chromedriver.exe"

    blinkit_crawl = CrawlBlinkit(URL, executable_path)
    blinkit_crawl.get_data()

