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
Requires scraped html data
```
source venv/bin/activate
python3 html_to_json.py
```

# Extracting and saving key terms
Requires scraped and converted json data
```
source venv/bin/activate
python3 key_terms.py
```

# Notes:
- Articles scraped: `3949`
## Terms
- 1-shingle, 2-shingle and 3-shingle used for terms
  - Reason: attraction names are sometimes up to 3 words
- Used TF.IDF for finding key terms within normal text paragraphs in documents
  - TF.IDF not applied to headings as we consider all terms from headings important
- Stats:
  - When TF.IDF threshold 0.5
    - Avg terms per doc: 87.10939478348949
## Problems:
- Articles sometimes reference some other location
  - Ex: article about Phuket, "Quiet beach is definitely a far cry from Patong"


# Data Sources:
- Stopwords from Python NLTK library: https://www.nltk.org/
- Scraped sites:
    - https://travelerfolio.com/
    - https://thesmartlocal.com/
    - https://alvinology.com/
    - https://theoccasionaltraveller.net/

---
data will be scraped/generated into `data/`
