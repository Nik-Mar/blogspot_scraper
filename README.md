# blogspot_scraper
### Data Science Project

### Libraries needed
* Scrapy
* time
* datetime
* json

  
After installation and downloading the project, run the scraper like this:
* in command line, navigate to the working directory
* type in "scrapy crawl blogspotspider"
* after it finishes, a json file with blog data should appear in your working directory

* if the file is empty or any of the fields title, text, date, the website most likely has a different structure and css selectors would have to be updated. At the moment the css selectors work for these basic blogspot sites with similar structure
