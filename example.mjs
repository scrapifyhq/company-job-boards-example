import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const [ats, wd] = await Promise.all([
    client.actor('scrapefy/ats-jobs-scraper').call({
        companies: ['https://boards.greenhouse.io/stripe', 'https://jobs.lever.co/spotify'],
        keywords: ['engineer'],
        maxItems: 100,
    }),
    client.actor('scrapefy/workday-jobs-scraper').call({
        careerSiteUrls: ['https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite'],
        keywords: ['data engineer'],
        maxJobsPerCompany: 50,
    }),
]);

const jobs = [];
for (const run of [ats, wd]) {
    const { items } = await client.dataset(run.defaultDatasetId).listItems();
    jobs.push(...items.filter((j) => j.title));
}
console.log(jobs.length, 'jobs from', new Set(jobs.map((j) => j.platform)).size, 'platforms');
