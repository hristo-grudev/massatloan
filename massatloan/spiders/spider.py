import scrapy

from scrapy.loader import ItemLoader

from ..items import MassatloanItem
from itemloaders.processors import TakeFirst


class MassatloanSpider(scrapy.Spider):
	name = 'massatloan'
	start_urls = ['https://www.massatloan.org/blog/']

	def parse(self, response):
		post_links = response.xpath('//article')
		for post in post_links:
			url = post.xpath('.//a[@class="elementor-post__read-more"]/@href').get()
			date = post.xpath('.//span[@class="elementor-post-date"]/text()').get()
			yield response.follow(url, self.parse_post, cb_kwargs={'date': date})

	def parse_post(self, response, date):
		title = response.xpath('//h1//text()[normalize-space()]').get()
		description = response.xpath('//div[contains(@class,"elementor-widget-theme-post-content")]//text()[normalize-space() and not(ancestor::div[@class="yasr-auto-insert-visitor"] | ancestor::span | ancestor::div[@class="lwptoc_header"] | ancestor::h1)]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()

		item = ItemLoader(item=MassatloanItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
