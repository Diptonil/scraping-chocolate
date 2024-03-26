import json

from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter


class P4ChocolatescraperPipeline:
    def process_item(self, item, spider):
        return item


class PriceConversionPipeline:
    conversion_rate = 1.3

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        price = adapter.get("price")
        if price:
            price = float(price)
            adapter["price"] = price * self.conversion_rate
            return item
        else:
            raise DropItem(f"Price missing in {item}.")
        

class DuplicatePipeline:
    encountered_names = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        name = adapter["name"]
        if name in self.encountered_names:
            raise DropItem(f"Duplicate item found for {item}.")
        else:
            self.encountered_names.add(name)
            return item
        

class JSONPrettifyPipeline:
    def open_spider(self, spider):
        self.file = open('output.json', 'w')
        self.file.write("[\n")

    def close_spider(self, spider):
        self.file.write("\n]")
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), indent=4) + ",\n"
        self.file.write(line)
        return item
