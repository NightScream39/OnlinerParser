
import requests
from time import sleep
import json


class Parser:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0',
            'Accept-Language': 'ru',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

        self.result = {}
        self.url = 'https://catalog.onliner.by/sdapi/catalog.api/search/mobile?mfr[0]=samsung&group=1&order=reviews_rating:desc'

    def json_to_dict(self):
        response = self.session.get(url=self.url)
        return response.json()

    def get_codes(self):
        data = self.json_to_dict()
        coding_names = [data['products'][i]['key'] for i in range(0, len(data['products']))]
        return coding_names

    def get_views(self):
        for code in self.get_codes():
            self.url = f'https://catalog.onliner.by/sdapi/catalog.api/products/{code}/reviews?order=created_at:desc'
            data = self.json_to_dict()
            self.result[code] = [data['reviews'][i]['text'] for i in range(len(data['reviews']))]
            sleep(0.5)
        return self.result

    def save_result(self):
        with open('data.json', 'w') as f:
            json.dump(self.result, f, ensure_ascii=False)

    def run(self):
        self.get_views()
        self.save_result()


if __name__ == '__main__':
    parser = Parser()
    parser.run()
