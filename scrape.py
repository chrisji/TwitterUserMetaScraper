from bs4 import BeautifulSoup
from datetime import datetime
import requests
import time
import json
import re
import os


class TwitterMetaScraper():
    def __init__(self, time_between_reqs=0, output_dir='output', input_dir='input', input_filename='id_list.txt'):
        self.time_between_reqs = time_between_reqs  # Number of seconds between user requests.

        # Paths for I/O
        output_filename = 'scrape_' + time.strftime('%H-%M-%S_%d%b%Y') + '.txt'
        self.output_path = os.path.join(os.path.dirname(__file__), output_dir, output_filename)
        self.input_path = os.path.join(os.path.dirname(__file__), input_dir, input_filename)

        self.user_ids = self.load_users()  # Load in user ids to process.

    def run(self):
        number_processed = 0  # Keep track of the number of scraped users
        num_of_users = len(self.user_ids)  # Store the number of users to scrape

        print 'Starting scraper:', datetime.now()
        for user_id in self.user_ids:
            self.scrape_user(user_id)
            number_processed += 1
            print datetime.now(), user_id, 'processed.', number_processed, 'of', num_of_users
            time.sleep(self.time_between_reqs)
        print 'Scraping finished:', datetime.now()

    def scrape_user(self, user_id):
        req = requests.get('https://twitter.com/intent/user?user_id=' + user_id)

        # Construct user attributes.
        attribute_dict = {
            "id": user_id,
            "http_status_code": req.status_code
        }

        # Extract and add useful attributes if status OK.
        if req.status_code == 200:
            attribute_dict["screen_name"] = TwitterMetaScraper.extract_screen_name(req)
            attribute_dict["full_name"] = TwitterMetaScraper.extract_full_name(req)
            attribute_dict["description"] = TwitterMetaScraper.extract_description(req)
            attribute_dict["follower_count"] = TwitterMetaScraper.extract_follower_count(req)
            attribute_dict["friend_count"] = TwitterMetaScraper.extract_friend_count(req)

        # Write extracted attributes to file.
        with open(self.output_path, 'a') as f:
            f.write(json.dumps(attribute_dict) + '\n')

    def load_users(self):
        user_ids = []
        with open(self.input_path, 'r') as f:
            for line in f.readlines():
                user_id = line.split(',')[0].strip()
                if user_id != '':
                    user_ids.append(user_id)
        return user_ids

    @staticmethod
    def extract_screen_name(req):
        data = BeautifulSoup(req.content).find('title').string
        screen_match = re.search('\((@.*)\)', data)
        if screen_match:
            return screen_match.group(1).encode('utf-8')
        else:
            return None

    @staticmethod
    def extract_full_name(req):
        data = BeautifulSoup(req.content).find('title').string
        name_match = re.search('(.*)\(@', data)  # Match for full name
        if name_match:
            return name_match.group(1).strip().encode('utf-8')
        else:
            return None

    @staticmethod
    def extract_description(req):
        return BeautifulSoup(req.content).find('p', attrs={'class': 'note'}).getText()

    @staticmethod
    def extract_follower_count(req):
        followers_dd = BeautifulSoup(req.content).find_all('dd', attrs={'class': 'count'})[0]
        return int(followers_dd.a.getText().replace(',', ''))

    @staticmethod
    def extract_friend_count(req):
        friends_dd = BeautifulSoup(req.content).find_all('dd', attrs={'class': 'count'})[1]
        return int(friends_dd.a.getText().replace(',', ''))

if __name__ == "__main__":
    scraper = TwitterMetaScraper(input_filename="ids.txt")
    scraper.run()
