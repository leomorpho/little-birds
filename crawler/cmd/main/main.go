package main

import (
	"fmt"

	log "github.com/sirupsen/logrus"
)

func main() {
	url := ""
	craigslistCrawler := collectors.NewCraigslistCrawler()
	err := craigslistCrawler.Crawl(url)
	if err != nil {
		log.Error(fmt.Sprintf("Error while scraping %v", url))
	}
}
