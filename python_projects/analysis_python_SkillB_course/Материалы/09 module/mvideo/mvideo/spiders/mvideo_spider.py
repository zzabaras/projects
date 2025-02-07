import numpy as np
import scrapy
import re


class MvideoSpider(scrapy.Spider):


	custom_settings = {'FEED_URI' : 'results/mvideo.csv'}

	name = 'mvideo'

	""" Составляем корректный список страниц. """
	allowed_domains = ['https://www.mvideo.ru/']
	first_page = ['https://www.mvideo.ru/smartfony-i-svyaz/smartfony-205'] 
	all_others = ['https://www.mvideo.ru/smartfony-i-svyaz/smartfony-205/f/page='+str(x) for x in range(2,77)]
	
	""" Вставлем на 1 меcто (0 индекс) нашу первую страницу. """
	start_urls = first_page+all_others
    
	def refine(self, string, field):
		compiled = re.compile('<.*?>')
		clean = re.sub(compiled, '|', string)
		clean = clean.strip('').replace('\t','').replace('\n', '').replace('\xa0', '')
		amount = abs(int(clean.split('|')[field]))
		return amount


	def parse(self, response):


		imgs = response.xpath("//div[@class='c-product-tile-picture__link']//@data-original").extract()
		titles = response.xpath("//div[@class='c-product-tile__description-wrapper']//h4/@title").extract()
		prices = response.xpath("//div[@class='c-product-tile__checkout-section']//div[@class='c-pdp-price__current']/text()").extract()
		discounts = response.xpath(".//div[@class='c-product-tile__checkout-section']//div[@class='c-pdp-price']//div[@class='c-pdp-price__sale']").extract()                           

		imgs = ['https:'+img for img in imgs]
        
		clean_titles = [title.split('Смартфон ')[1] for title in titles]

		prices = [price.replace("\n", "") for price in response.xpath("//div[@class='c-product-tile__checkout-section']//div[@class='c-pdp-price__current']/text()").extract()]
		prices = [price.strip() for price in prices] #  удаляем лишние пробелы (удаляет и /n и /t)
		prices = [price.replace("¤", "").replace("\xa0", "") for price in prices] # очищаем от остальных символов
		clean_prices = [int(price) for price in prices if price] # преводим к int


		clean_old_prices  = [self.refine(discount, 2) if 'c-pdp-price__discount' in discount else np.nan for discount in discounts]

		clean_discounts  = [self.refine(discount, 4) if 'c-pdp-price__discount' in discount else 0 for discount in discounts]

		for item in zip(clean_titles, clean_prices, clean_old_prices, clean_discounts, imgs):
				scraped_info = {
					'title' : item[0],
					'price' : item[1],
					'old_price' : item[2],
					'discount_offer': item[3],
					'image_urls' : [item[4]]}
				yield scraped_info