import scrapy
import os
import openpyxl
from urllib.parse import urlparse

class ImageSpider(scrapy.Spider):
    name = 'image_spider'

    def start_requests(self):
        wb = openpyxl.load_workbook('/home/turing/outsource/web-schrapper/Properties.xlsx')
        ws = wb.active
        for row in ws.iter_rows(min_row=2):
            url = row[0].value
            subdir = os.path.splitext(os.path.basename(urlparse(url).path))[0]  # use the page slug as subdir name
            yield scrapy.Request(url=url, meta={'subdir': subdir}, callback=self.parse)

    def parse(self, response):
        subdir = response.meta['subdir']
        directory_path = os.path.join('dataset', subdir)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        image_urls = response.css('img::attr(src)').getall()
        for url in image_urls:
            yield scrapy.Request(url=url, meta={'subdir': subdir}, callback=self.parse_image)

    def parse_image(self, response):
        url_path = urlparse(response.url).path
        filename = os.path.basename(url_path)  # extract filename from URL path
        subdir = response.meta['subdir']
        directory_path = os.path.join('dataset', subdir)
        filepath = os.path.join(directory_path, filename)
        if os.path.exists(filepath):
            self.log('Skipping duplicate file %s' % filepath)
        else:
            with open(filepath, 'wb') as f:
                f.write(response.body)
            self.log('Saved file %s' % filepath)
