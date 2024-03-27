from urllib.parse import urlencode


API_KEY = "your key here"


def get_proxy_url(url):
    payload = {"api_key": API_KEY, "url": url}
    proxy_url = "https://proxy.scrapeops.io/v1/?" + urlencode(payload)
    return proxy_url
