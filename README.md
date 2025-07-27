# Work Scrape Analyze

## 📌 Project Overview
Automated scraping and analysis of IT job vacancies from [work.ua](https://work.ua/jobs-it/). The pipeline consists of:

1. **Scraping job listings** marked as IT-related
2. **Extracting requirements** from vacancy descriptions
3. **Preparing data** for further analysis

## 🗂️ Folders and files Structure
```
work-scrape-analyze/
├── analysis/             # Scripts and reports
├── data/                 # Output files and config (e.g. words.json)
├── scrape_jobs/          # Scrapy spiders and utilities
│   └── spiders/
│   └── utils.py          
├── scrapy.cfg            # Scrapy config file
├── scrapy_output.log     # Spider logs
├── requirements.txt      # Python dependencies
├── README.md             
├── .gitignore            
└── venv/                 # Python virtual environment
```


## 🚀 Getting Started
1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Or venv/Scripts/activate (Windows)
   pip install -r requirements.txt


## 🕷️ Part 1 — Run Spider jobs.py

**Before running**, create a file data/words.json with 1–3 keywords to focus the search. <br>
Examples:

["Python"]   or  ["JavaScript", "CSS", "HTML"]

`These keywords help detect vacancies with relevant skills hidden in the description text.`

### Run the spider 'jobs.py'

* `scrapy crawl jobs -o data/it_jobs.jl`

### ⚙️ What Happens Behind the Scenes

1. Collect job IDs from [work.ua/jobs-it/](https://work.ua/jobs-it)
2. Save cached IDs to `data/cached_job_ids.json`
3. Retrieve full vacancy details via those IDs
    * Hint: The spider can be launched as many times as needed to get 
   information about all vacancies in cached_job_ids.json
4. Save collected vacancies to `data/it_jobs.jl`
5. Compare collected jobs with cache on each run
6. **Leave Firefox window open** while the spider runs!
7. Logs available at `scrapy_output.log`

## 🕷️ Part 2 — Run Spider refine_reqs.py

### Run the spider 'refine_reqs.py'

* `scrapy crawl refine_reqs -O data/refine_reqs.jl`

### ⚙️ What Happens Behind the Scenes

1. Loads job entries from data/it_jobs.jl and selects only those containing the focus keywords from words.json
2. Extracts the full set of requirements from each selected vacancy
3. Scans the requirement text and identifies relevant skills using the focus keywords
4. Saves the refined results into data/refine_reqs.jl — each line includes job ID and matched requirements

##  Tech

* Scrapy FW
* selenium, webdriver.Firefox
* beautifulsoup4






