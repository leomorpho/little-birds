package datastore

import (
	"fmt"
	"strconv"

	_ "github.com/jinzhu/gorm/dialects/postgres"
	_ "github.com/jinzhu/gorm/dialects/sqlite"

	log "github.com/sirupsen/logrus"

	"github.com/jinzhu/gorm"
	"gitlab.com/crawler/config"
)

func NewDB() *gorm.DB {

	if config.C.General.Environment == "integration" {
		log.Info("Creating new postgres database connection")
		postgresURI := fmt.Sprintf("host=%s port= %s user=%s dbname=%s password=%s sslmode=%s",
			config.C.Database.Host,
			strconv.Itoa(config.C.Database.Port),
			config.C.Database.User,
			config.C.Database.DBName,
			config.C.Database.Password,
			config.C.Database.SSL)

		log.Info(postgresURI)
		db, err := gorm.Open("postgres", postgresURI)
		defer db.Close()

		if err != nil {
			log.Fatalln(err)
		}

		db.LogMode(true)
		return db
	}

	log.Info("Creating new sqlite database instance")
	db, err := gorm.Open("sqlite3", "/tmp/gorm.db")
	if err != nil {
		log.Fatalln(err)
	}
	defer db.Close()
	return db
}
