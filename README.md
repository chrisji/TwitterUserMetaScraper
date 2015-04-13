# TwitterUserMetaScraper
- Twitter scraper to obtain public user meta-data using "https://twitter.com/intent/user?user_id=" endpoint.
- Note: official API for bulk lookup is (probably) a much more efficient option!

## What does it scrape?
- [X] Screen name
- [X] Full name
- [X] Follower count
- [X] Friend (following) count
- [X] Description field 
- [ ] Location field
- [ ] External link
- [X] Verified account status
- [ ] Most recent tweets sample
- [ ] 5 follower sample
- [ ] 5 friend (following) sample

## Usage
1. Install Beautiful Soup: `pip install beautifulsoup4`.
2. Add user ids to `input/user_id_list.txt`, one per line.
3. Run scrape.py

## Output
- A file containing a list of user attributes represented in json
- See the output directory for more details

###Example entry for a user:
```json
{
  "id": "783214", 
  "full_name": "Twitter", 
  "screen_name": "twitter",
  "description": "Your official source for news, updates and tips from Twitter, Inc.", 
  "friend_count": 102, 
  "follower_count": 37002665, 
  "verified": true,
  "friend_sample": ["kellyshalk", "MagicRecs", "TwitterData", "TwitterFashion", "TwitterMovies"],
  "follower_sample": ["preciousmeh", "zai00", "azzaul", "PanCarlos", "tafr"],
  "http_status_code": 200
}
```
