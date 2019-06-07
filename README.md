USAGE
-----

To use the script, untar the code and run "scrapy crawl webspider" (the real magic happens in /webcrawler/webcrawler/spiders/webcrawler_spider.py, pipelines.py, items.py, middlewares.py)

The code will run a set of urls from the mongodb (this time not recursive just yet, will only crawl the main url without following links),
crawl results stored into /tmp/webcrawler.log

Unfortunately no UI this time for adding urls to the database so will have to do it manually; regexps and the urls for crawling are stored there.

