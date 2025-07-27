import scrapy
import json

from scrapy.http import Response
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.common.by import By

from scrape_jobs.items import ScrapeJobsItem
from scrape_jobs.utils.add_requirements import additional_reqs
from scrape_jobs.utils.cached_jobs_ids import cached_jobs_ids
from scrape_jobs.utils.parsed_job_ids import parsed_job_ids
from scrape_jobs.utils.search_words import get_search_words
from scrape_jobs.utils.set_up_user_agent import user_agent_options


class JobsSpider(scrapy.Spider):
	name = "jobs"
	allowed_domains = ["www.work.ua"]
	start_urls = [
		"https://www.work.ua/jobs-it/"
	]
	base_url = "https://www.work.ua/"
	job_ids = set()
	page = 1

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# setting up driver()
		self.driver = webdriver.Firefox(options=user_agent_options())
		# avoid collecting existing jobs
		self.existing_ids = parsed_job_ids()
		# get set of cached jobs_ids
		self.cached_job_ids = cached_jobs_ids()
		# get words to focus the search (file: data/words.json)
		self.search_words = get_search_words()

	def close(self, reason: str):
		if hasattr(self, "driver"):
			try:
				self.driver.quit()
			except Exception:
				pass

	def parse(self, response: Response, **kwargs):
		if self.cached_job_ids:
			self.logger.info("Using cache_job_ids instead parse pagination")
			self.job_ids = self.cached_job_ids
			yield from self.parse_list_job_ids()
			return
		else:
			if response.css(".pagination").get():
				id_links = set(response.css("a::attr(name)").getall())
				self.job_ids.update(id_links)

				self.page += 1
				next_page = urljoin(self.start_urls[0], f"?page={self.page}")
				yield response.follow(next_page, callback=self.parse)
				print(".", end="")
			else:
				with open("data/cached_job_ids.json", "w", encoding="utf-8") as f:
					json.dump(list(self.job_ids), f, ensure_ascii=False)
				yield from self.parse_list_job_ids()

	def parse_list_job_ids(self):
		print(
			f"\n The {len(self.job_ids)} vacancies were found that are positioned "
			f"as vacancies in the IT sector ({self.start_urls[0]}).")
		print("Jobs: ", end="", flush=True)
		self.logger.info(
			f"***** {len(self.job_ids)} vacancies were found that are positioned"
			" as vacancies in the IT sector.")

		for job_id in self.job_ids:
			# do not scrape existing in it_jobs.jl
			if job_id not in self.existing_ids:

				# parse one simple job by ID
				url = urljoin(self.base_url, f"jobs/{job_id}/")

				yield scrapy.Request(
					url=url,
					callback=self.parse_simple_job,
					cb_kwargs={"job_id": job_id}
				)

	def parse_simple_job(self, response: Response, job_id: str):
		print(".", end="", flush=True)
		self.logger.info(f"parse simple job id {job_id}")
		try:
			self.driver.get(response.url)

			# title of job
			title = self.driver.find_element(By.ID, "h1-name").text
			self.logger.info(f"{title=}")

			# data about of job (salary, company, contact,.. )
			job_data = dict()
			ul_elements = self.driver.find_elements(
				By.CSS_SELECTOR, "div.card div.wordwrap ul"
			)
			ul_element = ul_elements[1]
			li_elements = ul_element.find_elements(
				By.CSS_SELECTOR, "li.text-indent"
			)

			for li in li_elements:
				try:
					key = li.find_element(By.TAG_NAME, "span").get_attribute("title")
					self.logger.info(f"{key=}")
					job_data[key] = (
						li.text.strip()
						.replace("\u202f", "")
						.replace("\u2009", "")
						.replace("\xa0", "")
						.replace("   ", "")
						.replace("\n\n", ";")
						.replace("\n", ";")
						.replace("–", "-")
					)
					self.logger.info(f"{job_data[key]=}")
				except Exception as e:
					self.logger.warning(
						f"[Exception]  Parse job_data error {response.url}: "
						f"{type(e).__name__} — {e}"
					)
					continue

			# requirements for the candidate, designated in a special place
			requirements = [
				elem.text.strip()
				for elem in self.driver.find_elements(By.CLASS_NAME, "ellipsis")
				if elem.text.strip()
			]
			# find focused words from data/words.json on this page (additional checking)
			html = self.driver.page_source
			# if these words not in requirements:
			for word in self.search_words:
				if word not in requirements:
					# checking each word in page text one by one
					reqs_from_text = additional_reqs(html, [word])

					if reqs_from_text:
						req_set = set(requirements)
						req_set.update(reqs_from_text)
						requirements = list(req_set)

			yield ScrapeJobsItem(
				job_id=job_id,
				job_url=response.url,
				title=title,
				job_data=job_data,
				requirements=requirements
			)

		except Exception:
			# skip this ID job if error reading/waiting for this page
			self.logger.warning(f"[Exesption] Can not to read: {response.url}")
			return
