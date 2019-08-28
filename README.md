# DeviantArtScraper

Python-powered automated data scraper and image downloader for DeviantArt.
Alpha v0.1

# Features
* Download a whole gallery of an author
* Download a whole collection or a folder
* Download all search results for a given query
* Download pretty much any bunch of images, if they can be viewed in the same feed
* Download images in highest resolution available. 
  That is, if the artist has published full-sized image (there's a "Download" button at the page), it'll be the one downloaded.
  Otherwise the scraper will download the largest thumbnail available
* Download "Mature Content" images

# Requirements:
* Python 3.7+
* Scrapy 1.7+
* Selenium 3.141+

# Installation and usage
* Download the source code, install the requirements (`pip install -r requirements.txt`)
* Run `update_cookies.py` script
* Edit `deviant/config.py` file: place your target gallery urls into URLS list
* Run `scrapy crawl deviant` command from the root DeviantArtScraper folder
* When the download is complete, the [output] folder will be created containing all the retrieved images 
