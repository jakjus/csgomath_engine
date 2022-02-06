import time
import os
from components.scraper import Scraper
from components.extractor import Extractor
from components.uploader import Uploader


cooldown = int(os.environ['SC_EX_MINUTES_COOLDOWN'])
root_pass = os.environ['MARIADB_ROOT_PASSWORD']


def cron():
    lastrun = 0
    while True:
        timenow = time.time()
        if timenow > lastrun + 60*cooldown:
            # subtract modulo, so that lastrun will not
            # progress extra seconds with each run
            lastrun = timenow - timenow % 60
            # Scrape
            scraper = Scraper()
            scraper.get_csgo_items()
            scraper.save_to_pickle('steam_market_items')
            # Extract
            extractor = Extractor(pickle_name='steam_market_items')
            extractor.extract_full()
            cases = extractor.cases
            # Upload
            uploader = Uploader(cases)
            uploader.upload()
        time.sleep(60)


if __name__ == "__main__":
    cron()
