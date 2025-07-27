# Work Scrape Analyze

### Project description

### Scraping & analysis IT vacancies on www.work.ua

The project consists of 3 parts:
 - Part 1: collects information about vacancies positioned as IT vacancies on the website: work.ua
 - Part 2: collecting detailed information about the candidate's requirements in these vacancies
 - Part 3: preparation of the received information for analysis and its analysis

### Project structure 
```
work-scrape-analyze/
├── analysis/             # scripts and reports for analytics
├── data/                 # saved data: here 'words.json' + scraping results
├── scrape_jobs/          # Scrapy spiders and collection logic
│   └── spiders/
│   └── utils.py          # additional utilities for scraping
├── scrapy.cfg            # configurations Scrapy
├── scrapy_output.log     # logging
├── requirements.txt      # projects requirements
├── README.md             # description of project
├── .gitignore            
└── venv/                 # virtual environment (you must create it)
```
### Before start of project
* `python -m venv venv`
* `venv/Scripts/activate`
* `pip install -r requirements.txt`


## Part 1. Run the first spider 'jobs.py'

### Put focused words into data/words.json. 

Before the spider starts working, enter the words to focus the search, file: data/words.json. 

_1-3 words recommended._

`This is because not all vacancies have clearly defined requirements, many requirements are simply 
listed in the text of the vacancy. Therefore, several keywords allow the spider to focus attention 
on these words, later this will be used as additional information for the second spider and in the analysis.
If you write "Python", then not a single vacancy that requires knowledge of Python will be missed.`

> For example, it could be: ["Python"]   or  ["JavaScript", "CSS", "HTML"]
### Run the spider 'jobs.py'
Run the first spider 'jobs.py' in the 'scrape_jobs' from the root directory of the project.


* `scrapy crawl jobs -o data/it_jobs.jl`


### How does it work?
1. When you first launch the spider: view and collect all job IDs from the initial URL: https://www.work.ua/jobs-it/  
    (At this stage, around 5,000 and more IDs vacancies may be collected)
2. After successful completion of this part of the procedure, all IDs are saved to the file: 
     data/cached_job_ids.json
3. All subsequent runs will check for the presence of cached IDs, and if they exist, 
     they will be used for further spider operation.
4. The next step in the process is collecting information about each vacancy from the list of cached IDs.
 For this, information is read from:  https://www.work.ua/jobs/<jobs ID>/
 The data is written to the data/it_jobs.jl,  line by line.
At this point, the process can be rerun as many times as necessary to collect 
the vacancy. At each run, the cached IDs are compared with the saved vacancies,
these statistics are displayed, and the collection process continues for 
the remaining IDs.
5. After the first spider has completed, the following files should be in the data/ folder:

`data/cached_job_ids.json`

`data/it_jobs.jl`

`data/words.json`
     _(you saved it before)_

6. While the spider is running, DO NOT close the Firefox browser window that opens.
7. The execution logs can be viewed in the file: scrapy_output.log

##  Tech

* Scrapy FW
* selenium, webdriver.Firefox
* beautifulsoup4






