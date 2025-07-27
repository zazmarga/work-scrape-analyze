import os
import json

import logging

logger = logging.getLogger("scrapy")


def parsed_job_ids() -> set:
	jobs_path = os.path.abspath(
		os.path.join(os.path.dirname(__file__), "..", "..", "data", "it_jobs.jl")
	)

	parsed_jobs_ids = set()

	if os.path.exists(jobs_path):
		with open(jobs_path, encoding="utf-8") as f:
			for line in f:
				try:
					item = json.loads(line)
					parsed_jobs_ids.add(item["job_id"])
				except Exception:
					pass
			logger.info(f"EXISTING {len(parsed_jobs_ids)=} jobs loaded from it_jobs.jl")
			print(f"Upload earlier {len(parsed_jobs_ids)=} jobs")
	else:
		logger.warning("File it_jobs.jl not found. This set still is empty.")

	return parsed_jobs_ids
