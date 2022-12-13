#!pip install scrapy
import scrapy
from scrapy.crawler import CrawlerProcess
import re

#Define the variable where we will store the titles of articles we are interested in
titles_interest = []

#We define our spider, which will scrape MetalSucks website to get articles related to my favorite groups.
class MetalSucksSpider(scrapy.Spider):
  name="metal_sucks_spider"

  #define the webpages we are going to crawl and what method we will apply to parse the HTML document of this website
  def start_requests(self):
    #scrape the first 5 pages of MetalSucks news
    urls = ["https://www.metalsucks.net/", 'https://www.metalsucks.net/page/2/', 'https://www.metalsucks.net/page/3/', 'https://www.metalsucks.net/page/4/', 'https://www.metalsucks.net/page/5/']
    #for each of the urls defined in the previous steps, this passes the HTML document to the parse_titles method within this class 
    for url in urls:
      yield scrapy.Request(url = url, callback = self.parse_titles)

  #this method exctracts article titles of a specific URL
  def parse_titles(self, response):
    #get titles of all articles in this page
    titles = response.xpath('//a[@itemprop="url"]/text()').extract()
    #filter titles related to my favorite bands
    global titles_interest
    titles_interest.extend([title for title in titles if re.search(fav_bands, title)])
    
#List of my favorite bands
fav_bands_list = ['Machine Head', 'Metallica', 'Spiritbox', 'Gojira', 'Trivium', 'Slipknot', 'ACDC', 'DevilDriver']
#create a simple regex to detect whether a title contains ANY of this bands
fav_bands = r'|'.join(fav_bands_list)

#Now it's time to run the spider
#initialize Crawler process
process = CrawlerProcess()
#specify the spider we are using to crawl the web
process.crawl(MetalSucksSpider)
#start crawling
process.start()

#Let's take a look into the titles of articles we might be interested in
for title in titles_interest:
  print(title,'\n')
