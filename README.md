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
- Used TF.IDF for finding key terms within documents
  - Text from headings and titles treated the same as normal text; TF.IDF robust enough to find significance of words even when hierarchy is lost.

- Tried using a threshold to only accept terms with a TF.IDF above some threshold, but does not produce a good balance of terms per document
  - TF.IDF Threshold: 0.5, Total terms: 1930585, Avg / doc: 488.8794631552292, Min / doc: 2, Max / doc: 2466
  - Switched to taking the top n terms based on TF.IDF for each document instead

### Taking the top n terms with the highest TF.IDF
See `TF_IDF_SAMPLES.md`
Analysis: n=200 seems the sweet spot because at around n=300 some articles start returning non-travel-activity related words to do with their promotions

## Problems:
- Articles sometimes reference some other location
  - Ex: article about Phuket, "Quiet beach is definitely a far cry from Patong"
- Many Ad Articles: articles which content are mainly not relevant to what one does in a country
  - Perhaps Clustering can help: discard very small clusters
  - Perhaps the recommendation / frequent items would not find the content of these articles frequent anyway

## TODO:
- Similar documents: Use the minhashing and LSH of terms to find jaccard similarity between documents
- Clustering: Use document similarity to do hierarchical clustering
- Frequent Itemsets: find association rules based on terms
- Images:
  - Downloading and transforming
  - Tagging with the terms from the same document
    - Or even better, with the terms nearest to its position in the document
- Change code to using mapreduce


# Data Sources:
- Stopwords from Python NLTK library: https://www.nltk.org/
- Scraped sites:
    - https://travelerfolio.com/
    - https://thesmartlocal.com/
    - https://alvinology.com/
    - https://theoccasionaltraveller.net/

---
data will be scraped/generated into `data/`
