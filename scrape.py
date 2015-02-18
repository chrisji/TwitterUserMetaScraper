from bs4 import BeautifulSoup
import requests
import time
import datetime
import re

# Location of scrape output.
output_filename = 'scrape_' + time.strftime('%H-%M-%S_%d%b%Y') + '.txt'

# Number of seconds to wait before sending next user request.
time_between_requests = 0

# Get a list of user ids to process.
user_ids = []
with open('input/user_id_list.txt', 'r') as f:
    for line in f.readlines():
        user_id = line.split(',')[0].strip()
        if user_id != '':
            user_ids.append(user_id)

# Keep track of number processed
number_processed = 0

# Store number of users to process
num_of_users = len(user_ids)

print 'Starting scraper:', datetime.datetime.now()
for user_id in user_ids:
    r = requests.get('https://twitter.com/intent/user?user_id=' + user_id)
    with open('output/' + output_filename, 'a') as f:
        if r.status_code == 200:
            data = BeautifulSoup(r.content).find('title').string
            screen_match = re.search('\((@.*)\)', data)  # Match for screen name
            name_match = re.search('(.*)\(@', data)  # Match for full name
            if screen_match and name_match:
                screen_name = screen_match.group(1).encode('utf-8')
                full_name = name_match.group(1).strip().encode('utf-8')
                f.write(user_id + ', ' + screen_name + ', ' + full_name + '\n')
            else:
                f.write(user_id + ', N/A, N/A\n')
        else:
            f.write(user_id + ', HTTP-CODE:' + str(r.status_code) + ', ' + 'HTTP-CODE:' + str(r.status_code) + '\n')
    number_processed += 1
    print datetime.datetime.now(), user_id, 'processed.', number_processed, 'of', num_of_users
    time.sleep(time_between_requests)
print 'Scraping finished:', datetime.datetime.now()
