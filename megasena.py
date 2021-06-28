import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import urllib
import json

class MegaSena(scrapy.Spider):
    name = 'megasena'

    base_url = 'https://www.sorteonline.com.br/mega-sena/resultados/'

    headers = {
       'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'

    }

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'qatarliving.csv',

    }


    def start_requests(self):
        # loop over page range
        for page in range(2000, 2384):
            # generate next page URL
            next_page = self.base_url + str(page)

            yield scrapy.Request(url=next_page, headers=self.headers, callback=self.parse)
            

    def parse(self,res):
        '''
        with open('res.html', 'w') as f:
            f.write(res.text)
        '''
        '''
        # local HTML content
        content = ''

        # read local HTML file
        with open('res.html', 'r') as f:
            for line in f.read():
                content += line

        # init scrapy selector
        res = Selector(text=content)
        '''
        for card in res.css('div[class="DIVtableResultado"]'):
            features = {
                'concurso': card.css('span[class="color header-resultados__nro-concurso"]::text')
                                .get(),

                'data': card.css('span[class="color header-resultados__datasorteio"]::text')
                            .get(),

                'resultado': ' '.join(card.css('ul *::text')
                                 .getall())
                                 .replace('\n', '')



            }
            #print(json.dumps(features, indent=2))

            yield features



if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(MegaSena)
    process.start()

    # debug
    #MegaSena.parse(MegaSena, '')
