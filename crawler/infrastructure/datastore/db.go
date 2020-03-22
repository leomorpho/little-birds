package datastore

import (
	"fmt"

	_ "github.com/jinzhu/gorm/dialects/postgres"
	log "github.com/sirupsen/logrus"

	"github.com/jinzhu/gorm"
	"gitlab.com/crawler/config"
)

func NewDB() *gorm.DB {
	postgresURI := fmt.Sprintf("host=%s user=%s dbname=%s sslmode=%s password=%s",
		config.C.Database.Host,
		config.C.Database.User,
		config.C.Database.DBName,
		config.C.Database.SSL,
		config.C.Database.Password)

	db, err := gorm.Open("postgres", postgresURI)

	if err != nil {
		log.Fatalln(err)
	}

	return db
}
