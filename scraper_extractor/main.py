import argparse
import os
import pprint
from components.scraper import Scraper
from components.extractor import Extractor
from components.uploader import Uploader

parser = argparse.ArgumentParser(description='Define script options.')
parser.add_argument("-s", "--scrape", help="Scrape.",
                    action="store_true", default=False)
parser.add_argument("-e", "--extract", help="Extract.",
                    action="store_true", default=False)
parser.add_argument("-u", "--upload", help="Upload.",
                    action="store_true", default=False)
parser.add_argument("-d", "--debug", help="Debug mode.",
                    action="store_true")
args = parser.parse_args()
pp = pprint.PrettyPrinter()


def main():
    if args.scrape:
        scraper = Scraper()
        scraper.get_csgo_items()
        scraper.save_to_pickle('steam_market_items')
    if args.extract:
        extractor = Extractor(pickle_name='steam_market_items')
        extractor.extract_full()
        cases = extractor.cases
        if args.debug:
            pp.pprint(cases)
    if args.upload:
        if 'cases' not in locals():
            extractor = Extractor(pickle_name='steam_market_items')
            extractor.extract_full()
            cases = extractor.cases
        uploader = Uploader(cases)
        uploader.upload()

if __name__ == "__main__":
    main()
