import os
import json
import random
import re

from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options

import logging


class JobsUtils:
	def __init__(self):
		self.data_path = os.path.abspath(
			os.path.join(os.path.dirname(__file__), "..", "data")
		)
		self.logger = logging.getLogger("scrapy")

	def user_agent_options(self):
		options = Options()
		options.headless = False
		# User-Agent to options
		user_agents = [
			"Mozilla/5.0 (X11; Linux x86_64) Firefox/100.0",
			"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
				"(KHTML, like Gecko) Version/16.0 Safari/605.1.15 Edg/138.0.0.0"
		]
		selected_agent = random.choice(user_agents)

		options.set_preference(
			"general.useragent.override",
			selected_agent
		)
		options.set_preference("intl.accept_languages", "uk-UA,uk,en-US")

		return options

	def cached_jobs_ids(self) -> set:
		cached_jobs_path = os.path.join(self.data_path, "cached_job_ids.json")

		cached_job_ids = set()

		if os.path.exists(cached_jobs_path):
			with open(cached_jobs_path, encoding="utf-8") as f:
				cached_job_ids = set(json.load(f))
				self.logger.info(f"Uploaded {len(cached_job_ids)} job_id from cached_job_ids.json")
				print(f"Uploaded {len(cached_job_ids)=} job_ids from cached_job_ids.json")

		return cached_job_ids

	def parsed_job_ids(self) -> set:
		jobs_path = os.path.join(self.data_path, "it_jobs.jl")

		parsed_jobs_ids = set()

		if os.path.exists(jobs_path):
			with open(jobs_path, encoding="utf-8") as f:
				for line in f:
					try:
						item = json.loads(line)
						parsed_jobs_ids.add(item["job_id"])
					except Exception:
						pass
				self.logger.info(f"EXISTING {len(parsed_jobs_ids)=} jobs loaded from it_jobs.jl")
				print(f"Upload earlier {len(parsed_jobs_ids)=} jobs")
		else:
			self.logger.warning("File it_jobs.jl not found. This set still is empty.")

		return parsed_jobs_ids

	def additional_reqs(self, html, skills) -> set:
		soup = BeautifulSoup(html, "html.parser")

		add_reqs = set()
		try:
			job_card = soup.find("div", id="job-description").get_text().lower()
		except Exception:
			return add_reqs

		for skill in skills:
			if re.search(rf'\b{re.escape(skill.lower())}\b', job_card):
				add_reqs.add(skill)
				self.logger.info(f"add '{skill}' to requirements")

		return add_reqs

	def get_search_words(self) -> list:
		search_words_path = os.path.join(self.data_path, "words.json")

		search_words = []

		if os.path.exists(search_words_path):
			with open(search_words_path, encoding="utf-8") as f:
				search_words = list(json.load(f))
				if len(search_words) > 0:
					self.logger.info("Additional words to focus the search "
								f"(from file data/words.json): {search_words}")
					print("Search will be focused using words: "
						  f"{search_words}  (from file data/words.json)")

		return search_words

	def refine_skills(self) -> tuple[set, set]:
		jobs_path = os.path.join(self.data_path, "it_jobs.jl")

		re_jobs = set()
		all_skills = set()

		words = self.get_search_words()

		if os.path.exists(jobs_path):
			with open(jobs_path, encoding="utf-8") as f:
				for line in f:
					try:
						item = json.loads(line)
						all_skills.update(item["requirements"])
						for word in words:
							if word in item["requirements"]:
								re_jobs.add(item["job_id"])
					except Exception:
						pass
				self.logger.info(
					f"In total {len(all_skills)} skills were allocated from "
					"requirements of jobs loaded from it_jobs.jl"
				)
				print(f"In total {len(all_skills)} skills were found in requirements")
		else:
			self.logger.warning(
				"File it_jobs.jl not found. You need to run first part "
				"(scrapy crawl jobs -o data/it_jobs.jl)."
			)

		self.logger.warning(
			f"Requirements for an additional {len(re_jobs)} jobs "
			f"related to words: {words} will be checked"
		)
		print(
			f"Parsing additional (only requirements) for {len(re_jobs)} jobs"
			f" related to words: {words}"
		)

		return re_jobs, all_skills
