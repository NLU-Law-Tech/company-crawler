import scrapy
from loguru import logger
from urllib.parse import urljoin
import wget
import os

class CompanySpider(scrapy.Spider):
    name = "company"

    def start_requests(self):
        urls = [
            'http://ronnywang-twcompany.s3-website-ap-northeast-1.amazonaws.com/files/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def _download_file(self,url,f_name):
        os.makedirs('../company_data',exist_ok=True)
        wget.download(url,os.path.join('../company_data',f_name))

    def parse(self, response):
        current_url = response._get_url()
        logger.info(f"current_url:{current_url}")
        logger.debug(response)
        table = response.css('table>tr')
        for i,tr in enumerate(table):
            if i == 0: continue; # title

            td = tr.css('td')
            f_name = td.css('a::text').get()
            link = urljoin(current_url,f_name)
            logger.info(link)
            self._download_file(link,f_name)

            
        