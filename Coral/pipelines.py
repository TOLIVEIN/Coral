# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
from Coral.items import GameItem, GameDetailItem


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
