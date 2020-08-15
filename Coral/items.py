# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GameItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    href = scrapy.Field()
    cover = scrapy.Field()
    score = scrapy.Field()
    name = scrapy.Field()
    platform = scrapy.Field()
    date = scrapy.Field()
    tags = scrapy.Field()
    desc = scrapy.Field()


class GameDetailItem(scrapy.Item):
    # url = scrapy.Field()
    cover = scrapy.Field()
    platforms = scrapy.Field()
    name = scrapy.Field()
    origin_name = scrapy.Field()
    nicknames = scrapy.Field()
    date = scrapy.Field()
    tags = scrapy.Field()
    score = scrapy.Field()
    features = scrapy.Field()
    images = scrapy.Field()
    description = scrapy.Field()
    company = scrapy.Field()
    staffs = scrapy.Field()
    languages = scrapy.Field()
    systems = scrapy.Field()
    # sub_platforms = scrapy.Field()
    minimal_config = scrapy.Field()
    recommend_config = scrapy.Field()