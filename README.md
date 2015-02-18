# TwitterUserMetaScraper
- Twitter scraper to obtain public user meta-data.
- Currently collects full name and screen name.
- Note: official API for bulk lookup is probably a much more efficient option!

## Usage
1. Install Beautiful Soup: `pip install beautifulsoup4`.
2. Add user ids to `input/user_id_list.txt`, one per line.
3. Run scrape.py

## Output
- A file containing a list of user data in the form: `user_id, screen_name, full_name`
- See the example output file for more info.
