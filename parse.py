from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
import time

class GoodOnYou:
    def __init__(self):
        self._driver = webdriver.Firefox(executable_path=os.environ['gecko_path'])
        self._driver.implicitly_wait(30)
        self._homepage_url = 'https://directory.goodonyou.eco/'
        # values to the given keys are names of radio buttons
        # if the names change on the website, only update the values
        self._valid_filters = {'Women':'Womenswear', 'Men':'Menswear', 'Kids':'Kids'}

    # returns homepage HTML (3 different pages can 
    # be returned based on which radio button is selected)
    # f must be one of the keys in valid_filters
    def _get_homepage_HTML(self, f) -> str:
        if f not in self._valid_filters:
            raise ValueError('Invalid filter')
        self._driver.get(self._homepage_url)
        self._driver.find_element_by_css_selector("input[type='radio'][name={}]".format(self._valid_filters[f])).click()
        return self._driver.page_source

    # returns categories belonging to filter f (one of Men, Women or Kids)
    # [activewear, Tops, ...]
    def _get_categories_of(self, f) -> list:
        if f not in self._valid_filters:
            raise ValueError('Invalid filter')
        html = BeautifulSoup(self._get_homepage_HTML(f), 'html.parser')
        categories = [a['href'].split('categories/')[1] for a in html.find_all('a', href=True) if 'categories' in a['href']]
        return categories

    # returns all categories: 
    # union of Men, Women and Kids
    def get_categories(self) -> list:
        s = set()
        return list(s.union(self._get_categories_of('Women'), self._get_categories_of('Men'), self._get_categories_of('Kids')))

    # solving the problem of infinite scroll
    # keep scroling down until page length stops increasing
    # SOURCE -> https://michaeljsanders.com/2017/05/12/scrapin-and-scrollin.html
    def _scroll_bottom(self) -> None:
        page_length = self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var page_length=document.body.scrollHeight;return page_length;")
        match=False
        while(match==False):
                last_count = page_length
                time.sleep(2)
                page_length = self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var page_length=document.body.scrollHeight;return page_length;")
                if last_count==page_length:
                    match=True

    # returns all brands in a single category 
    def _get_brands_of(self, category) -> list:
        url = self._homepage_url + 'categories/' + category
        self._driver.get(url)
        self._scroll_bottom()
        html = BeautifulSoup(self._driver.page_source, 'html.parser')
        brands = [a['href'].split('brand/')[1] for a in html.find_all('a', href=True) if 'brand' in a['href']]
        # todo: delete the print statement
        print('size of', category, 'is', len(brands))
        return brands
    
    # returns all brands in all categories (union of all brands)
    def get_brands(self, categories, sort=False) -> list:
        s = set()
        for category in categories:
            brands_in_category = self._get_brands_of(category)
            while not brands_in_category:
                brands_in_category = self._get_brands_of(category)
            s = s.union(brands_in_category)
        brands = list(s)
        if sort:
            brands.sort()
        return brands



# website = GoodOnYou()
# categories = website.get_categories()
# print(categories)

# brands = website.get_brands(categories)
# print('total brands =', len(brands))
# print(brands)

# 1121 brands in total
