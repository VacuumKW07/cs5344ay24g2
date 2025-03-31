"""
Sites we want to try to scrape:
    - https://travelerfolio.com/
    - https://thesmartlocal.com/
    - https://alvinology.com/
    - https://iwandered.net/

We might not need to scrape all, but if it's not too hard we should get as much as possible

Aim to save individual pages that have the full content for what to do at destination(s)
in html for .e.g.
data/travelerfolio/kuala-lumpur-malaysia-travel.html
Also, aim for travel articles

"""
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
    print("Scraping done for travelerfolio")


def _travelerfolio_filename_for_detail_page_url(full_url:str) -> str:
    """ Example url: https://travelerfolio.com/family-friendly-penang-trip/
    """
    url_parsed = urllib.parse.urlparse(full_url)
    return url_parsed.path.replace("/","") + ".html"


def scrape_thesmartlocal() -> None:
    URL_BASE = "https://thesmartlocal.com/category/travel/southeast-asia/page/"
    for i in range(67):  # 67 listing pages found
        pagenum = i + 1
        listings_page_url = URL_BASE + str(pagenum)
        listings_page = requests.get(listings_page_url)
        listings_page_soup = BeautifulSoup(listings_page.content, "html.parser")
        # each listing page has snippets of full articles with a 'Read More' link
        detail_links = listings_page_soup.find_all("a", class_="link-secondary")
        for link in detail_links:
            detail_page_url = link.get("href")
            print("Scraping {}".format(detail_page_url))
            filename = _travelerfolio_filename_for_detail_page_url(detail_page_url)
            details_page = requests.get(detail_page_url)
            details_page_soup = BeautifulSoup(details_page.content, "html.parser")
            _save_scraped_page("thesmartlocal", filename, details_page_soup)
    print("Scraping done for thesmartlocal")


def _thesmartlocal_filename_for_detail_page_url(full_url:str) -> str:
    """ Example url: https://thesmartlocal.com/read/bangkok-to-khao-yai/
    """
    url_parsed = urllib.parse.urlparse(full_url)
    return url_parsed.path.replace("read/", "").replace("/","") + ".html"


def scrape_alvinology() -> None:
    URL_BASE = "https://alvinology.com/category/all-travel/page/"
    for i in range(208):  # 208 listing pages found
        pagenum = i + 1
        listings_page_url = URL_BASE + str(pagenum)
        listings_page = requests.get(listings_page_url)
        listings_page_soup = BeautifulSoup(listings_page.content, "html.parser")

        # the read-more link is a little trickier to find, can't search globally based on class
        # Need to target the content area
        listings_page_content = listings_page_soup.find("div", class_="cs-posts-area cs-posts-area-posts")

        # each listing page has snippets of full articles with a 'Read More' link, they are hidden in the title
        titles = listings_page_content.find_all("h2", class_="cs-entry__title")
        detail_links = listings_page_content.find_all("a", class_="link-secondary")
        for title in titles:
            link = title.find("a")
            detail_page_url = link.get("href")
            print("Scraping {}".format(detail_page_url))
            filename = _alvinology_filename_for_detail_page_url(detail_page_url)
            details_page = requests.get(detail_page_url)
            details_page_soup = BeautifulSoup(details_page.content, "html.parser")
            _save_scraped_page("alvinology", filename, details_page_soup)
    print("Scraping done for alvinology")


def _alvinology_filename_for_detail_page_url(full_url:str) -> str:
    """ Example url: https://thesmartlocal.com/read/bangkok-to-khao-yai/
    """
    url_parsed = urllib.parse.urlparse(full_url)
    return url_parsed.path.split("/")[4] + ".html"



def scrape_iwandered() -> None:
    # TODO
    pass


def _save_scraped_page(domain_name:str, filename:str, soup:BeautifulSoup) -> None:
    """
    Common function
    Will save to data/<domain_name>/<filename>
    """
    parent_dir = "data/{}".format(domain_name)
    os.makedirs(parent_dir, exist_ok=True)
    path = "{}/{}".format(parent_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(soup))


if __name__ == "__main__":
    # Comment and uncomment
    scrape_travelerfolio()
    scrape_thesmartlocal()
    scrape_alvinology()
    scrape_iwandered()
