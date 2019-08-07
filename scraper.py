import scrapy
import csv

import requests

class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ['http://brickset.com/sets/year-2016']
    
    
    with open('document.csv','w') as f:
        f = csv.writer(f)
        f.writerow(['Name', 'pieces'])
    
    def parse(self, response):
        SET_SELECTOR = '.set'
        

#        with open('document.csv','a') as f:
##        f = csv.writer(open('brick.csv', 'w'))
#            f = csv.writer(f)
#            f.writerow(['Name', 'pieces'])
        
        for brickset in response.css(SET_SELECTOR):
            
        
        
            NAME_SELECTOR = 'h1 ::text'
            PIECES_SELECTOR = './/dl[dt/text() = "Pieces"]/dd/a/text()'
            MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
            IMAGE_SELECTOR = 'img ::attr(src)'
            
            names = brickset.css(NAME_SELECTOR).extract_first()
            pieces = brickset.xpath(PIECES_SELECTOR).extract_first()
            imageUrl = brickset.css(IMAGE_SELECTOR).extract_first()
            

            
            try:

                with open('document.csv','a') as f:
                    write = csv.writer(f)
                    write.writerow([names, pieces])
            except Exception:
                pass
            
            try:
                
                r = requests.get(imageUrl, allow_redirects=True)
                open(names+'.jpg', 'wb').write(r.content)
                
            except:
                pass
            
            
            
            
            
            
            yield {
                'name': brickset.css(NAME_SELECTOR).extract_first(),
                'pieces': brickset.xpath(PIECES_SELECTOR).extract_first(),
                'minifigs': brickset.xpath(MINIFIGS_SELECTOR).extract_first(),
                'image': brickset.css(IMAGE_SELECTOR).extract_first(),

            }
        
        NEXT_PAGE_SELECTOR = '.next a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
                )
        
            
