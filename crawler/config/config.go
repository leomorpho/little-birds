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
	General  General
	Database Database
	Server   Server
}

func (c config) Validate() error {
	return validation.ValidateStruct(&c,
		validation.Field(&c.Database, validation.Required),
		validation.Field(&c.Server, validation.Required))
}

// Database represents all database related configs for the running app
type Database struct {
	Host     string
	Port     int
	User     string
	Password string
	DBName   string
	SSL      string
	LogLevel string
}

func (p Database) Validate() error {
	return validation.ValidateStruct(&p,
		validation.Field(&p.Host, validation.Required),
		validation.Field(&p.Port, validation.Required),
		validation.Field(&p.User, validation.Required),
		validation.Field(&p.Password, validation.Required),
		validation.Field(&p.DBName, validation.Required),
		validation.Field(&p.SSL, validation.Required, validation.In("disable", "enable")))
}

// Server represents all server related configs for the running app
type Server struct {
	Port string
}

func (s Server) Validate() error {
	return validation.ValidateStruct(&s,
		validation.Field(&s.Port, validation.Required))
}

type General struct {
	LogLevel    string
	Environment string
}

func (g General) Validate() error {
	return validation.ValidateStruct(&g,
		validation.Field(&g.LogLevel, validation.Required, validation.In("info", "error", "warning", "debug")))
}

var C config

// ReadConfig uses VIPER to read the proper configuration file or environment
// variables into the configuration structs
func ReadConfig() {
	Config := &C

	viper.SetConfigName("config")
	if os.Getenv("ENVIRONMENT") == "integration_env" {
		log.Info("Loading production environment config")
		viper.AutomaticEnv()
		Config.Database.Host = viper.GetString("postgres_host")
		Config.Database.Port = viper.GetInt("postgres_port")
		Config.Database.User = viper.GetString("postgres_user")
		Config.Database.Password = viper.GetString("postgres_password")
		Config.Database.DBName = viper.GetString("postgres_db")
		Config.Database.SSL = viper.GetString("postgres_ssl")
		Config.Server.Port = viper.GetString("server_port")
		Config.General.LogLevel = viper.GetString("log_level")
		Config.General.Environment = "integration"
	} else {
		log.Info("Loading development environment config")
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

	// Set log level in LOGRUS
	switch Config.General.LogLevel {
	case "debug":
		log.SetLevel(log.DebugLevel)
	case "warning":
		log.SetLevel(log.WarnLevel)
	case "error":
		log.SetLevel(log.ErrorLevel)
	case "info":
		log.SetLevel(log.InfoLevel)
	}

	spew.Dump(C)
}
