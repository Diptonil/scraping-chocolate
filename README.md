# Scraping Chocolate

- This is a general web scraping solution for a website with special focus on techniques to bypass 403s.
- There are also pipelines to push data to databases, format outputs, transform data based on currency rate, etc.
- Item loaders to validate scraped data to bring it all to a uniformity has also been implemented.


## User Agents

- This is the "fingerprint" that states the user OS, browser, etc. details about the machine from which a request originates.
- Repeated requests from the same user agent shall result in a ban.
- With the use of `scrapy-user-agents`, everytime we send a request, we use a different user-agent from a set of predefined agents from this package. So this issue is taken care of.


## Proxies

- In addition to user agents, we also have our IP address that gets tracked. Same IP sending a flurry of requests also shall result in a ban.
- To prevent this, we use proxies. A list of proxies can be found [here](https://scrapeops.io/proxy-providers/) for comparison.
- We have as an example rigged up the functions to use the ScrapeOps Proxies in the `proxies.py` file. We can use that by obtaining an API key from their services.
- Paid proxies give us multiple benefits such as maximum dependability, higher concurrency, low ban rate, etc. 
