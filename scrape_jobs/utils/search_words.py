import os
import json

import logging
logger = logging.getLogger("scrapy")


def get_search_words() -> list:
    search_words_path = os.path.abspath(
		os.path.join(os.path.dirname(__file__), "..", "..", "data", "words.json")
	)

    search_words = []

    if os.path.exists(search_words_path):
        with open(search_words_path, encoding="utf-8") as f:
            search_words = list(json.load(f))
            if len(search_words) > 0:
                logger.info("Additional words to focus the search "
							f"(from file data/words.json): {search_words}")
                print("Search will be focused using words: "
					  f"{search_words}  (from file data/words.json)")

    return search_words
