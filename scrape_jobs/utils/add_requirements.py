import re

from bs4 import BeautifulSoup

import logging

logger = logging.getLogger("scrapy")


def additional_reqs(html, skills) -> set:
	soup = BeautifulSoup(html, "html.parser")

	add_reqs = set()
	try:
		job_card = soup.find("div", id="job-description").get_text().lower()
	except Exception:
		return add_reqs

	for skill in skills:
		if re.search(rf'\b{re.escape(skill.lower())}\b', job_card):
			add_reqs.add(skill)
			logger.info(f"add '{skill}' to requirements")

	return add_reqs
