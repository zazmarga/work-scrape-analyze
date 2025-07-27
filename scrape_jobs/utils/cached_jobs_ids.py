import os
import json

import logging
logger = logging.getLogger("scrapy")


def cached_jobs_ids() -> set:
    cached_jobs_path = os.path.abspath(
		os.path.join(os.path.dirname(__file__), "..", "..", "data", "cached_job_ids.json")
	)

    cached_job_ids = set()

    if os.path.exists(cached_jobs_path):
        with open(cached_jobs_path, encoding="utf-8") as f:
            cached_job_ids = set(json.load(f))
            logger.info(f"Uploaded {len(cached_job_ids)} job_id from cached_job_ids.json")
            print(f"Uploaded {len(cached_job_ids)=} job_ids from cached_job_ids.json")

    return cached_job_ids
