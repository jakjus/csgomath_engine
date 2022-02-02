import time
import requests
import math
import pickle
from tqdm import tqdm


class Scraper:
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/39.0.2171.95 Safari/537.36'}
    sleep_time = 12  # between GET requests, in seconds
    max_retries = 15

    def __init__(self):
        self.all_items = []
        self.last_query_timestamp = 0

    def save_to_pickle(self, pickle_name):
        with open(pickle_name+'.pickle', 'wb') as handle:
            pickle.dump(
                self.all_items,
                handle,
                protocol=pickle.HIGHEST_PROTOCOL)

    def items_search_url(self, page):
        return f'https://steamcommunity.com/market/search/render/\
                ?query=&start={str(page*100)}&count=100&appid=730&norender=1'

    def scrape_page(self, url, current_retries=0):
        if current_retries == self.max_retries:
            raise Exception('Max retries exceeded.')
        while (time.time() - self.sleep_time) < self.last_query_timestamp:
            time.sleep(0.5)
        page = requests.get(url, headers=self.headers)
        self.last_query_timestamp = time.time()
        if page.status_code != 200:
            print('Error: ', page.status_code, 'Retrying...')
            return self.scrape_page(url, current_retries+1)
        return page

    def get_csgo_items(self):
        self.all_items = []
        # Get total_pages first to init tqdm(for loop)
        url = self.items_search_url(0)
        page = self.scrape_page(url)
        d = page.json()
        total_pages = math.floor(int(d['total_count'])/100)

        print('Scraping started...')
        for i in tqdm(range(total_pages)):
            url = self.items_search_url(i)
            page = self.scrape_page(url)
            d = page.json()
            for el in d['results']:
                el['timestamp'] = time.time()
            self.all_items += d['results']
