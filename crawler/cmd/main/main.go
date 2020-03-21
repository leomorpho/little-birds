package main

import (
	"fmt"

	"github.com/labstack/echo"
	log "github.com/sirupsen/logrus"
	"gitlab.com/crawler/collectors"
	"gitlab.com/crawler/config"
	"gitlab.com/crawler/infrastructure/datastore"
	"gitlab.com/crawler/infrastructure/router"
	"gitlab.com/crawler/registry"
)

func main() {
	url := ""
	craigslistCrawler := collectors.NewCraigslistCrawler()
	err := craigslistCrawler.Crawl(url)
	if err != nil {
		log.Error(fmt.Sprintf("Error while scraping %v", url))
	}

	config.ReadConfig()

	db := datastore.NewDB()
	db.LogMode(true)
	defer db.Close()

	r := registry.NewRegistry(db)

	e := echo.New()
	e = router.NewRouter(e, r.NewAppController())

	fmt.Println("Server listen at http://localhost" + ":" + config.C.Server.Address)
	if err := e.Start(":" + config.C.Server.Address); err != nil {
		log.Fatalln(err)
	}
}
