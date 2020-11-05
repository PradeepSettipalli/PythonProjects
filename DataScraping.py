"""
@author: pradeepsettipalli
"""

import scrapy
import json

filename = 'skinresults.csv' #create csv file to write our results

class EtsySpider(scrapy.Spider): #create spider
    name = "etsy_spider" 
    
    start_urls = [
            'https://www.etsy.com/c/bath-and-beauty/skin-care?ref=catnav-891' #specify start webpage from where to extract data
            ]
    
    with open(filename, 'w') as f:
        f.write('productName, startPrice, rating, ratingCount, numberofSales, seller\n') # give column names to csv file
                
    def parse(self, response):     
        
        #follow all product links and parse the items
        for href in response.xpath("//a/@href[contains(., '/listing/')]"):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_item)
            
        #follow all category links to find items to parse    
        for href in response.xpath("//a/@href[contains(., '/search/')]"):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse)
            
        #create next page selector to extract data from all the next pages   
        next_page = response.xpath('//a[contains(@href,"page")]/span[contains(text(), "\n                            Next page\n")]/../@href').extract_first()
        if next_page:
            yield scrapy.Request(
                    response.urljoin(next_page),
                    callback=self.parse)
            


    def parse_item(self, response):
        with open(filename, 'a') as f:
            thedict = json.loads(response.xpath("//script[@type='application/ld+json']/text()").extract()[0]) #extract data from this json structure
            finaldict = {
                    'name' : thedict['name'].replace(',', ''), #extract name of product
                    'startPrice' : float(thedict['offers']['lowPrice']), #extract start price of product
                    'rating' : float(thedict['aggregateRating']['ratingValue']), #extract rating value of seller
                    'ratingCount' :  float(thedict['aggregateRating']['ratingCount']) #extract rating count of seller
                    }
                    
            numberofSales = response.xpath("//a[@class='wt-text-link-no-underline wt-display-inline-flex-xs wt-align-items-center']/span/text()").extract_first() #extract total number of sales of seller
            seller =  response.xpath("//a[@class='wt-text-link-no-underline']/span/text()").extract_first() #extract name of seller
            
            #write results 
            finalstring = finaldict['name'] + ","
            finalstring += str(finaldict['startPrice']) + ","
            finalstring += str(finaldict['rating']) + ","
            finalstring += str(finaldict['ratingCount']) + ","
            finalstring += str(numberofSales).replace(',', '').replace('sales', '') + ","
            finalstring += str(seller).replace('\n','').replace(' ', '') + "\n"
            
            f.write(finalstring)