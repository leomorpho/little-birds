package datastore

import (
	"errors"
	"fmt"
	"strconv"
	"time"

	// "github.com/jinzhu/gorm/dialects/postgres" is the dependency for gorm postgres
	_ "github.com/jinzhu/gorm/dialects/postgres"
	_ "github.com/jinzhu/gorm/dialects/sqlite"

	log "github.com/sirupsen/logrus"

	"github.com/jinzhu/gorm"
	"gitlab.com/crawler/config"
)

// DbConnTimeout is the connection timeout for connecting to the gorm database
const DbConnTimeout = 30

// NewDB creates a new database using GORM
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
		db, err := connectWithRetry("postgres", postgresURI)
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

func connectWithRetry(dbType, uri string) (*gorm.DB, error) {

	err := errors.New("No DB connection")

	ch := make(chan string, 1)
	go func() {
		for err != nil {
			_, err = gorm.Open(dbType, uri)
		}
		ch <- "Connection made"
	}()

	select {
	case _ = <-ch:
		db, err := gorm.Open(dbType, uri)
		return db, err
	case <-time.After(DbConnTimeout * time.Second):
		db, err := gorm.Open(dbType, uri)
		return db, err
	}
}
