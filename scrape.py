import requests
import urllib
import os
from bs4 import BeautifulSoup


def scrape_travelerfolio() -> None:
    URL_BASE = "https://travelerfolio.com/blog/page/"
    for i in range(67):  # 67 listing pages found
        pagenum = i + 1
        listings_page_url = URL_BASE + str(pagenum)
        listings_page = requests.get(listings_page_url)
        listings_page_soup = BeautifulSoup(listings_page.content, "html.parser")

        # each listing page has snippets of full articles with a 'Read More' link
        detail_links = listings_page_soup.find_all("a", class_="more-link")
        for link in detail_links:
            detail_page_url = link.get("href")
            print("Scraping {}".format(detail_page_url))
            filename = _travelerfolio_filename_for_detail_page_url(detail_page_url)
            details_page = requests.get(detail_page_url)
            details_page_soup = BeautifulSoup(details_page.content, "html.parser")
            _save_scraped_page("travelerfolio", filename, details_page_soup)


def _travelerfolio_filename_for_detail_page_url(full_url:str) -> str:
    """ Example url: https://travelerfolio.com/family-friendly-penang-trip/
    """
    url_parsed = urllib.parse.urlparse(full_url)
    return url_parsed.path.replace("/","") + ".html"


def _save_scraped_page(domain_name:str, filename:str, soup:BeautifulSoup) -> None:
    parent_dir = "data/{}".format(domain_name)
    os.makedirs(parent_dir, exist_ok=True)
    path = "{}/{}".format(parent_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(soup))


if __name__ == "__main__":
    # Comment and uncomment
    scrape_travelerfolio()
