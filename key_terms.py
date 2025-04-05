"""
Extract the important terms within all the 'text' paragraphs and place push
them into a top-level array field with name `constants.DOC_KEY_KEY_TERMS`

New files saved into another data directory
"""
import os
from collections.abc import Iterable
import json
import re
from typing import List, Set
import constants
from constants import (
    DOC_KEY_TITLE,
    DOC_KEY_CONTENT,
    DOC_KEY_KEY_TERMS,

    DOC_CONTENT_ITEM_KEY_TYPE,
    DOC_CONTENT_ITEM_KEY_TEXT,

    DOC_CONTENT_ITEM_TYPE_H2,
    DOC_CONTENT_ITEM_TYPE_H3,
    DOC_CONTENT_ITEM_TYPE_TEXT,
    NLTK_STOPWORDS
)


TF_IDF_THRESHOLD = 0.2


def add_key_terms() -> None:
    doc_index = 0
    for doc in _read_files():
        doc_index += 1
        print("[Key Terms] Processing doc {}".format(str(doc_index)))
        # Terms are sets but we can only json serialise lists
        doc[DOC_KEY_KEY_TERMS] = [
            list(term_set) for term_set in _key_terms_from_doc(doc)]
        _save_doc(str(doc_index), doc)
        print("[Key Terms] Doc {} saved".format(str(doc_index)))
    print("[Key Terms] Done")


def _key_terms_from_doc(doc: dict) -> List[Set[str]]:
    # TODO: change data structure of freqs if needed
    freqs = {}
    for term in _all_terms_from_doc(doc):
        key = _dict_key_for_term(term)
        if key not in freqs:
            freqs[key] = 0
        freqs[key] = freqs[key] + 1

    max_freq = max([freqs[key] for key in freqs])

    key_terms = []
    for key in freqs:
        tf_idf = freqs[key] / max_freq
        if tf_idf > TF_IDF_THRESHOLD:
            key_terms.append(_term_from_dict_key(key))
    return key_terms


def _dict_key_for_term(s: Set[str]) -> str:
    """Modify if needed"""
    return ",".join(list(s))


def _term_from_dict_key(key: str) -> Set[str]:
    return key.split(",")


def _all_terms_from_doc(doc: dict) -> Iterable[Set[str]]:
    # TODO: Perhaps shingles

    title = doc.get(DOC_KEY_TITLE)
    for title_word in _filter_stopwords(_text_to_words(title)):
        yield {title_word}

    for para in doc.get(DOC_KEY_CONTENT):
        if para.get(DOC_CONTENT_ITEM_KEY_TYPE) in [
            DOC_CONTENT_ITEM_TYPE_H2,
            DOC_CONTENT_ITEM_TYPE_H3,
            DOC_CONTENT_ITEM_TYPE_TEXT
        ]:
            for word in _filter_stopwords(
                _text_to_words(para.get(DOC_CONTENT_ITEM_KEY_TEXT))
            ):
                yield {word}


def _filter_stopwords(words: Iterable[str]) -> Iterable[str]:
    return filter(lambda word: word not in NLTK_STOPWORDS, words)


def _text_to_words(text: str) -> Iterable[str]:
    return [word for word in re.split(r'\W+', text.lower()) if word.isalpha()]


def _read_files() -> Iterable[dict]:
    for filepath in _get_filepaths():
        with open(filepath, 'r', encoding='utf-8') as f:
            yield json.loads(f.read())


def _get_filepaths() -> Iterable[os.PathLike]:
    for root, dirs, files in os.walk(constants.DIR_JSON):
        for name in files:
            yield os.path.join(root, name)


def _save_doc(name: str, doc: dict) -> None:
    """`name` should not have extensions e.g. .json"""
    os.makedirs(constants.DIR_KEY_TERMS, exist_ok=True)
    path = "{}/{}".format(constants.DIR_KEY_TERMS, name + ".json")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(doc))


if __name__ == "__main__":
    add_key_terms()
