import scrapy

from chocolates.items import ChocolateItem, ChocolateItemLoader


class ChocolateSpider(scrapy.Spider):
    name = "chocolate"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all"]

    # def start_requests(self):
    #     """Enable this only in case we are using proxies."""
    #     yield scrapy.Request(url=get_proxy_url(self.start_urls[0]), callback=self.parse)

    def parse(self, response):
        products = response.css("product-item")
        for product in products:
            item = ChocolateItemLoader(item=ChocolateItem(), selector=product)
            item.add_css('name', 'a.product-item-meta__title::text')
            item.add_value('price', product.css("span.price::text").extract()[1])
            item.add_value('url', response.url + product.css("div.product-item-meta a::attr(href)").get())
            yield item.load_item()
        
        next_page = response.css('[rel="next"]::attr(href)').get()
        if next_page is not None:
            # yield response.follow(get_proxy_url("https://www.chocolate.co.uk" + next_page), callback=self.parse)
            yield response.follow("https://www.chocolate.co.uk" + next_page, callback=self.parse)
