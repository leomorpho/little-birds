# TODO
* Add error logging if scraped field returns nothing. That may be a change in the site that needs to be reflected in the app
* Add search interface for Craigslist: search(keywords, location, category, maxprice, minprice)
* Add scraper for craigslist sitemap and categories. Populate/update database. This will be used by frontend to display categories.
    * Connect database from pipeline.py
* Add scaped items to items.py
* Add spider to test for proxy ip and user agent in header
