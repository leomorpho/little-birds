### Crawlers

A map of sites is represented in a single DB. However, different crawlers will update it differently. A supercrawler could also bring all this logic together.

* URL crawler
  * Create map of relevant URLs. Site Object form nodes, and links are directed links that point from one website to another.
  * Depth of crawl per site is shallow and random.

### Logic

* If a site is new, create a very shallow profile
* For every successesful search, increase website score in DB
* A site profile in InternetMap should not store whole pages by the 100s



```json
{
  "http://crawler.com": {
    "keywords": { // semantics?
      "crawler": 0.98,
      "search engine": 0.73,
      "furniture": 0.65,
      "buying": 0.61
    },
    "average depth": 4,
    "category": { // Choose among X (100? 1000? 10,000?)
      "physics": 0.98,
      "math": 0.97,
      "colleges and university": 0.94,
      "astronomy": 0.86
    },
    "content": {
      "online marketplace": 0.42,
      "informative": 0.03
    },
    "syntax": {
      "posts": 0.87,
      "text": 0.83,
      "hyperlinks": 0.19,
      "equations": 0.21,
      "graphs": 0.15,
      "images": 0.09,
      "videos": 0,
      "sounds": 0,
      "animations": 0,
      "tables": 0,
      "lists": 0
    }
  }
}
```

The sorting in categories must be done unsupervised. 



### Deep site crawler



