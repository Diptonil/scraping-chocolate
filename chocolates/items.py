import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose


def clean_price(price: str) -> str:
    if "From" in price:
        return price[5:]
    return price[1:]


class ChocolateItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()


class ChocolateItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    price_in = MapCompose(clean_price)
