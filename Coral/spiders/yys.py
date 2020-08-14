import scrapy

from Coral.items import GameItem, GameDetailItem


class YysSpider(scrapy.Spider):
    name = 'yys'
    allowed_domains = ['www.yystv.cn']
    # start_urls = ['http://www.yystv.cn/']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page = 1
        self.base_url = 'https://www.yystv.cn'

    def start_requests(self):
        urls = [
            # 'https://www.yystv.cn/games/game_tags/1?order=score',
            # 'https://www.yystv.cn/games/game_tags/1',
            # 'https://www.yystv.cn/games/game_tags/3',
            # 'https://www.yystv.cn/games/game_tags/5',
            # 'https://www.yystv.cn/games/game_tags/4',
            'https://www.yystv.cn/g/4282',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        platforms = {
            '1': 'PC',
            '3': 'PS4',
            '5': 'NS',
            '4': 'XBOX ONE'
        }
        filename = platforms[response.url.split("/")[-1][0]]+'.json'
        for htmlItem in response.css('.game-list>li'):

            item = GameItem()

            item['href'] = ''.join([self.base_url, htmlItem.css('li>a::attr(href)').get()])
            item['cover'] = htmlItem.css('.game-cover-wrapper>img:first-child::attr(src)').get()
            item['score'] = htmlItem.css('.game-score::text').get()
            item['platform'] = htmlItem.css('.cover-platform::text').get()
            item['date'] = htmlItem.css('.cover-date::text').get()
            item['name'] = htmlItem.css('h3.game-name::text').get()
            item['tags'] = htmlItem.css('.game-tag-list li::text').getall()
            item['desc'] = htmlItem.css('.game-desc::text').get()

            yield scrapy.Request(item['href'], callback=self.parse_game_detail)

            yield item

        next_page = response.css('.next-page')
        if next_page is not None and self.page <= 2:
            self.page += 1
            next_page = response.url.split("?")[0] + '?page=' + str(self.page)
            yield scrapy.Request(next_page, callback=self.parse)
            # print(next_page)
        else:
            self.page = 1

    def parse_game_detail(self, response):
        item = GameDetailItem()

        print(response)

        # game_info = response.css('.game-cover-info-section')

        item['cover'] = response.css('.game-cover-image::attr(src)').get()
        item['platforms'] = response.css('.game-platform-tag-list>li::text').getall()
        item['name'] = response.css('.game-info-title::text').get()
        item['origin_name'] = response.css('.game-info-nickname::text').get()
        item['nicknames'] = response.css('[data-render="nicknames"]::text').get()
        item['date'] = response.css('[data-render="pubdate"]::text').get()
        item['tags'] = response.css('[data-render="tags"]>a::text').getall()
        item['score'] = response.css('.game-info-rank-score::text').get()
        item['features'] = response.css('.game-info-rank-tags-list>a::text').getall()
        item['images'] = response.css('.game-capture::attr(src)').getall()
        item['description'] = response.css('.game-brief::text').get()
        item['company'] = response.css('[data-render="production"]>a::text').get()
        item['staffs'] = response.css('[data-render="producer"]>a::text').get()
        item['languages'] = response.css('[data-render="language"]>a::text').get()
        item['systems'] = response.css('[data-render="system"]>a::text').getall()
        # item['sub_platforms'] = response.css('[data-render="sub_platform"]>a::text').get()
        item['minimal_config'] = response.css('[data-render="min_configuration"]::text').get()
        item['recommend_config'] = response.css('[data-render="max_configuration"]::text').get()

        yield item
