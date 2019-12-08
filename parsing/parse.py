from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from collections import defaultdict
from copy import deepcopy
import json
import os
import time
import pickle

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

    # returns all brand tags in a single category 
    # 'homepage_url/brand/<brand_tag>/'
    def _get_brand_tags_in(self, category) -> list:
        url = self._homepage_url + 'categories/' + category
        self._driver.get(url)
        self._scroll_bottom()
        html = BeautifulSoup(self._driver.page_source, 'html.parser')
        brand_tags = [a['href'].split('brand/')[1] for a in html.find_all('a', href=True) if 'brand' in a['href']]
        return brand_tags
    
    # returns all brand tags in all categories (union of all brand tags)
    def get_every_brand_tag(self, categories, sort=False) -> list:
        s = set()
        for category in categories:
            tags_in_category = self._get_brand_tags_in(category)
            while not tags_in_category:
                tags_in_category = self._get_brand_tags_in(category)
            s = s.union(tags_in_category)
        brand_tags = list(s)
        if sort:
            brand_tags.sort()
        return brand_tags

    def _get_brand_website(self, html):
        brand_website = [a['href'].split('?')[0] for a in html.find_all('a', href=True) if 'utm_source=GoodOnYou' in a['href']]
        if brand_website:
            return brand_website[-1]
        return None
    
    def _get_brand_name(self, html):
        brand_name = [h1.text.strip() for h1 in html.find_all('h1')]
        if brand_name:
            return brand_name[-1]
        return None
    
    def _get_brand_rating(self, html):
        brand_rating = [span.text.split('Rated: ')[-1] for span in html.find_all('span') if 'Rated' in span.text]
        if brand_rating:
            return brand_rating[0]
        return None
    
    def _get_brand_price(self, html):
        brand_price = [span.text.split(' ')[-1] for span in html.find_all('span') if 'Price' in span.text]
        if brand_price:
            return brand_price[0]
        return None

    def _get_brand_message(self, html):
        brand_message = [h4.text.strip() for h4 in html.find_all('h4')]
        if brand_message:
            return brand_message[-1]
        return None

    def _get_brand_planet_rating(self, html):
        all_ratings = [span.text[0] for span in html.find_all('span') if 'out of 5' in span.text]
        if len(all_ratings) == 3:
            return all_ratings[0]
        return None

    def _get_brand_people_rating(self, html):
        all_ratings = [span.text[0] for span in html.find_all('span') if 'out of 5' in span.text]
        if len(all_ratings) == 3:
            return all_ratings[1]
        return None

    def _get_brand_animals_rating(self, html):
        all_ratings = [span.text[0] for span in html.find_all('span') if 'out of 5' in span.text]
        if len(all_ratings) == 3:
            return all_ratings[2]
        return None

    # maps brand name to brand data
    # if no brand name is found then brand name becomes 'NA ' + brand_tag
    def _get_brand_name_to_data_mapping(self, brand_tag) -> dict:
        GoodOnYou_url = self._homepage_url + 'brand/' + brand_tag
        self._driver.get(GoodOnYou_url)
        html = BeautifulSoup(self._driver.page_source, 'html.parser')

        brand_name = self._get_brand_name(html)
        if not brand_name:
            brand_name = 'NA ' + brand_tag
        data = {}
        mapping = {brand_name:data} 
        data['rating'] = self._get_brand_rating(html)
        data['price'] = self._get_brand_price(html)
        data['planet_rating'] = self._get_brand_planet_rating(html)
        data['people_rating'] = self._get_brand_people_rating(html)
        data['animals_rating'] = self._get_brand_animals_rating(html)
        data['message'] = self._get_brand_message(html)
        data['GoodOnYou_url'] = GoodOnYou_url
        
        return mapping
    
    # all brand names mapped to their data
    def get_data(self, brand_tags: list) -> dict:
        if not isinstance(brand_tags, list):
            raise ValueError('Brand tags must be provided in a list')
        data = {}
        for brand_tag in brand_tags:
            mapping = self._get_brand_name_to_data_mapping(brand_tag)
            key = next(iter(mapping))
            data[key] = deepcopy(mapping[key])
            # wait 3 seconds to allow a page to load
            time.sleep(3)
        return data

    def brand_url_to_brand_name_mapping(self, brand_names_to_data_mapping) -> dict:
        mapping = {}
        for brand_name in brand_names_to_data_mapping:
            GoodOnYou_url = brand_names_to_data_mapping[brand_name]['GoodOnYou_url']
            self._driver.get(GoodOnYou_url)
            html = BeautifulSoup(self._driver.page_source, 'html.parser')
            key = brand_url = self._get_brand_website(html)
            if not brand_url:
                key = GoodOnYou_url
            mapping[key] = brand_name
            time.sleep(3)
        return mapping



