import scrapy

from scrapy.http import Response
from urllib.parse import urljoin

from selenium import webdriver

from scrape_jobs.items import ScrapeRefineReqsItem
from scrape_jobs.utils import JobsUtils


class RefineReqsSpider(scrapy.Spider):
	name = "refine_reqs"
	allowed_domains = ["www.work.ua"]
	start_urls = [
		"https://www.work.ua/jobs/"
	]
	base_url = "https://www.work.ua/jobs/"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.utils = JobsUtils()
		# setting up driver()
		self.driver = webdriver.Firefox(options=self.utils.user_agent_options())
		# get set of refine jobs_ids and all of skills
		self.refine_job_ids, self.all_skills = self.utils.refine_skills()

	def close(self, reason: str):
		if hasattr(self, "driver"):
			try:
				self.driver.quit()
			except Exception:
				pass

	def parse(self, response: Response, **kwargs):
		if self.refine_job_ids:

			for job_id in self.refine_job_ids:
				# parse one simple job by ID
				url = urljoin(self.base_url, f"{job_id}/")

				yield scrapy.Request(
					url=url,
					callback=self.parse_job_requirements,
					cb_kwargs={"job_id": job_id}
				)

	def parse_job_requirements(self, response: Response, job_id: str):
		print(".", end="", flush=True)
		self.logger.info(f"parse simple refine_job id {job_id}")
		try:
			self.driver.get(response.url)

			html = self.driver.page_source

			requirements = list(self.utils.additional_reqs(html, self.all_skills))

			yield ScrapeRefineReqsItem(job_id=job_id, requirements=requirements)

		except Exception:
			# skip position if error reading/waiting for this page
			self.logger.warning(f"[Exception] Can not to read: {response.url}")
			return

