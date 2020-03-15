package collectors

import (
	"errors"

	"github.com/gocolly/colly"
)

// Post stores information about a craigslist post
type Post struct {
	Title       string
	Description string
	Location    string
	Price       string
	Url         string
	PostedAt    string
}

// CraigslistCrawler is a crawler for the Craigslist classifiedss site
type CraigslistCrawler struct{}

func NewCraigslistCrawler() CraigslistCrawler {
	craigslistCrawler := CraigslistCrawler{}
	return craigslistCrawler
}

// Crawl crawls postings pages for Craigslist Classifiedss
// Categories and individual keywords can be searched by forming a proper url string
func (CraigslistCrawler) Crawl(url string) error {

	if url == "" {
		return errors.New("No url to start crawl was provided")
	}
	// Instantiate default collector for postings page
	c := colly.NewCollector()

	c.onHTML("a[href]", func())

	// Create another collector to scrape individual posting page
	postCollector = c.Clone()

	c.Visit(url)

	return nil
}
