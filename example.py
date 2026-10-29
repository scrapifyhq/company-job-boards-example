import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

ats = client.actor("scrapefy/ats-jobs-scraper").call(run_input={
    "companies": [
        "https://boards.greenhouse.io/stripe",
        "https://jobs.ashbyhq.com/ramp",
        "https://jobs.lever.co/spotify",
    ],
    "keywords": ["engineer"],
    "maxAgeDays": 14,
    "maxItems": 100,
})

wd = client.actor("scrapefy/workday-jobs-scraper").call(run_input={
    "careerSiteUrls": [
        "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite",
        "https://jobs.smartrecruiters.com/ServiceNow",
    ],
    "keywords": ["data engineer"],
    "postedSinceDays": 14,
    "maxJobsPerCompany": 50,
})

jobs = []
for run in (ats, wd):
    jobs += list(client.dataset(run["defaultDatasetId"]).iterate_items())

jobs = [j for j in jobs if j.get("title")]          # drop any error rows
jobs.sort(key=lambda j: j.get("postedAt") or "", reverse=True)
for j in jobs[:20]:
    print(j["platform"], "|", j["companyName"] or j["company"], "|", j["title"], "|", j["location"])
