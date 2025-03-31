"""
Needs html data to first have been scraped

Convert Scraped HTML content into our documents of our own data structure
{
    title: <main title>
    content: [
        { type: <img | h2 | text>, text: <text if any>, src: <src if any> }
    ]
}
"""
from typing import Tuple
from collections.abc import Iterable
import os
from bs4 import BeautifulSoup
import constants
import json


def convert_alvinology() -> None:
    for (slug, soup) in _read_pages(constants.SITE_NAME_ALVINOLOGY):
        print(
            "Converting {}: {}".format(constants.SITE_NAME_ALVINOLOGY, slug))
        title_h1 = soup.find(
            "h1", class_="cs-entry__title")
        title = title_h1.find("span").text
        content_div = soup.find("div", class_="entry-content")
        content = []
        for para in content_div.find_all("p"):
            if para.find("img"):
                img = para.find("img")
                content.append({"type": "img", "src": img.get("src")})
            elif para.find("h2"):
                h2 = para.find("h2")
                content.append({"type": "h2", "text": h2.get_text()})
            else:
                content.append({"type": "text", "text": para.get_text()})
        doc = {"title": title, "content": content}
        _save_json(constants.SITE_NAME_ALVINOLOGY, slug, doc)

    print("Converting done for alvinology")


def _read_pages(domain_name: str) -> Iterable[Tuple[str, BeautifulSoup]]:
    """
    Common function
    Will read all in data/html/<domain_name>
    """
    for filename in os.listdir("{}/{}".format(
        constants.DIR_HTML, domain_name
    )):
        yield (
            filename.replace(".html", ""),
            _read_scraped_page(domain_name, filename))


def _read_scraped_page(domain_name: str, filename: str) -> BeautifulSoup:
    """
    Common function
    Will read from data/html/<domain_name>/<filename>
    """
    parent_dir = "{}/{}".format(constants.DIR_HTML, domain_name)
    os.makedirs(parent_dir, exist_ok=True)
    path = "{}/{}".format(parent_dir, filename)
    with open(path, 'r', encoding='utf-8') as f:
        return BeautifulSoup(f, "html.parser")


def _save_json(
    domain_name: str, slug: str, doc: dict
) -> None:
    """
    Common function
    Will save to data/json/<domain_name>/<slug>.json
    """
    parent_dir = "{}/{}".format(constants.DIR_JSON, domain_name)
    os.makedirs(parent_dir, exist_ok=True)
    path = "{}/{}".format(parent_dir, slug + ".json")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(doc))


if __name__ == "__main__":
    # Comment and uncomment
    # convert_travelerfolio()
    # convert_thesmartlocal()
    convert_alvinology()
    # convert_theoccasionaltraveller()
