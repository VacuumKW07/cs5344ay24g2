# cs5344ay24g2
cs5344 ay 24/25 group 2

# Setup
```
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

# Scraping, saves html data

Warning: Scraped data can be huge

```
source venv/bin/activate
python3 scrape.py
```

# Converting scraped html data into json
```
source venv/bin/activate
python3 html_to_json.py
```

---
data will be scraped/generated into `data/`
