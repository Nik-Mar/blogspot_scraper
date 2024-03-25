import scrapy
import time
from Blogspot.items import BlogspotItem


class BlogspotSpider(scrapy.Spider):
    name = 'blogspotspider'
    #allowed_domains = ['blogspot.com']
    start_urls = ["http://iheartcookingclubs.blogspot.com/"] #whatever url 
    file_name=start_urls[0].split('/')[2].split(".")[0] #unelegant but it works
      
    custom_settings = {
		'FEEDS': { '%(file_name)s.json': { 'format': 'json',}}
		}

    def parse(self, response):
        posts = response.css('div.date-outer')
        single_post=BlogspotItem()

        for post in posts:
            
            single_post["title"]=post.css('h3.post-title.entry-title a::text').get()
            single_post["date"]=post.css('h2.date-header span::text').get()
            #single_post["text"]=post.css('div.date-outer div[itemprop*="articleBody"] *::text').extract()
            single_post["text"]=post.css('div.date-outer div.post-body.entry-content *::text').extract()

            yield single_post

        next_page = response.css("a.blog-pager-older-link::attr(href)").get()
        if next_page is not None:
           yield response.follow(next_page, callback=self.parse)
        time.sleep(0.2) #pause so we don't get blocked
