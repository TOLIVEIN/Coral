# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
from Coral.items import GameItem, GameDetailItem
import pymongo


class CoralPipeline:
    def __init__(self):
        self.game = open('yys_game.json', 'w', encoding='utf8')
        self.game_detail = open('yys_game_detail.json', 'w', encoding='utf8')

    def process_item(self, item, spider):
        text = json.dumps(dict(item), ensure_ascii=False)
        if isinstance(item, GameItem):
            # print(text)
            self.game.write(text)
        elif isinstance(item, GameDetailItem):
            self.game_detail.write(text)
        print('-----------------------------------------------')
        # return item

    def close_spider(self, spider):
        self.game.close()
        self.game_detail.close()


class MongoPipeline:
    @classmethod
    def from_crawler(cls, crawler):
        cls.DB_URL = crawler.settings.get('MONGO_DB_URL', 'mongodb://localhost:27017')
        cls.DB_NAME = crawler.settings.get('MONGO_DB_NAME', 'scrapy_data')
        return cls()

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.DB_URL)
        self.db = self.client[self.DB_NAME]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, GameItem):
            collection = self.db['yys_game']
        elif isinstance(item, GameDetailItem):
            collection = self.db['yys_game_detail']
        post = ItemAdapter(item).asdict()
        collection.insert_one(post)
        return item
