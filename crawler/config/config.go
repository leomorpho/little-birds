package config

import (
	"fmt"
	"os"

	validation "github.com/go-ozzo/ozzo-validation"
	log "github.com/sirupsen/logrus"

	"github.com/davecgh/go-spew/spew"
	"github.com/spf13/viper"
)

type config struct {
	Database Database
	Server   Server
}

func (c config) Validate() error {
	return validation.ValidateStruct(&c,
		validation.Field(&c.Database, validation.Required),
		validation.Field(&c.Server, validation.Required))
}

type Database struct {
	Host     string
	User     string
	Password string
	DBName   string
	SSL      string
}

func (p Database) Validate() error {
	return validation.ValidateStruct(&p,
		validation.Field(&p.Host, validation.Required),
		validation.Field(&p.User, validation.Required),
		validation.Field(&p.Password, validation.Required),
		validation.Field(&p.DBName, validation.Required),
		validation.Field(&p.SSL, validation.Required, validation.In("disable", "enable")))
}

type Server struct {
	Port string
}

func (s Server) Validate() error {
	return validation.ValidateStruct(&s,
		validation.Field(&s.Port, validation.Required))
}

var C config

func ReadConfig() {
	Config := &C

	if os.Getenv("ENVIRONMENT") == "PROD" {
		log.Info("Loading production environment config")
		viper.AutomaticEnv()
		Config.Database.Host = viper.GetString("postgres_host")
		Config.Database.User = viper.GetString("postgres_user")
		Config.Database.Password = viper.GetString("postgres_password")
		Config.Database.DBName = viper.GetString("postgres_db")
		Config.Database.SSL = viper.GetString("postgres_ssl")
		Config.Server.Port = viper.GetString("server_port")
	} else {
		log.Info("Loading development environment config")
		viper.SetConfigName("config")
		viper.SetConfigType("yaml")
		viper.AddConfigPath("./config/")

		if err := viper.ReadInConfig(); err == nil {
			fmt.Println("Using config file:", viper.ConfigFileUsed())
		} else {
			fmt.Println(err)
			log.Fatalln(err)
		}
	}

	if err := viper.Unmarshal(&Config); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	spew.Dump(C)
}
