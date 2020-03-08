# TODO
* Add error logging if scraped field returns nothing. That may be a change in the site that needs to be reflected in the app
* Add search interface for Craigslist: search(keywords, location, category, maxprice, minprice)
* Add scraper for craigslist sitemap and categories. Populate/update database. This will be used by frontend to display categories.
    * Connect database from pipeline.py
* Add scraped items to items.py
* Add spider to test for proxy ip and user agent in header

## Handling of failed scraping events
Every pair of [domain, pageType] should have a scraping policy.
The query parameters should be used from most successful to least succesfull. If one fails, the page with the accompanying failed query parameter or parameters is added to a list in order to be later updated.
If the query parameters are updated and the search job is still in the future (such as for planned delivery of scraped data), the original client job should be notified or the associated failed urls should be crawledd with the updated policies and subsequently delivered to the client.

### Example of scraping policy
```
{
"craigslist": {
    "homePage": {...},
    "productPage": {
        "title": {
            {
                "xpath": "xpath1", 
                "sucessRuns": 39,
                "failedRuns": 12,
                "lastSeen": datetime

            },
            {
                "xpath": "xpath2", 
                "sucessRuns": 12,
                "failedRuns": 1,
                "lastSeen": datetime
            },
        },
            "price": {...},
            "locaton": {...},
            "description": {...},
            "createdAt": {...},
            "url": {...}
    }
}
```

A policy could possibly be stored in SQL tables in this manner:
| domain | page type | title | xpath | heuristicScore | failedRuns | successfulRuns | lastSeen |

I think postgres is actually the way to go.

In order to know which xpath query to use, a heuristic such as `(successRuns / failedRuns) * (succesRuns * x)` could be used. The success/failure ratio is important, but so is the prevalence or popularity of the xpath in the data.

### Example of failed scraping event notification
```
{
    {
        "url": "http://vancouver.craigslist.com/something=blah?else=blah",
        "jobId": "379ae629-7b58-4f8a-a65a-4ccbd1cd211f",

    }
}
```

### Example of a job request
This will need to be fleshed out, but for now it is not a priority. TODO: implement fixer for broken scraping policies.
{
    {
        "id": "379ae629-7b58-4f8a-a65a-4ccbd1cd211f",
        "query": {
            "queryAPIVersion": "0.1",
            "searchStr": "junior software engineer",
        }
    }
}