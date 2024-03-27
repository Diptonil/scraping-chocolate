import json
import sqlite3

from decouple import config
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter
from psycopg2 import connect


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

    def process_item(self, item, spider):
        line = json.dumps(dict(item), indent=4) + ",\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.write("\n]")
        self.file.close()


class PostgresPipeline:
    def open_spider(self, spider):
        self.conn = connect(
            dbname='chocolate_db',
            user=config("POSTGRES_USER"),
            password=config("POSTGRES_PASSWORD"),
            host='localhost',
            port='5432'
        )
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        self.cur.execute(
            "INSERT INTO chocolates (name, price, url) VALUES (%s, %s, %s)",
            (
                item['name'],
                item['price'],
                item["url"]
            )
        )
        return item


class SQLitePipeline:
    def open_spider(self, spider):
        self.conn = sqlite3.connect('data.db')
        self.cur = self.conn.cursor()
        self.create_table()

    def close_spider(self, spider):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def create_table(self):
        self.cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS chocolates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price FLOAT,
                url TEXT,
            )
            '''
        )

    def process_item(self, item, spider):
        self.cur.execute("INSERT INTO chocolates (name, price, url) VALUES (?, ?, ?)", (item['name'], item['price'], item["url"]))
        return item
