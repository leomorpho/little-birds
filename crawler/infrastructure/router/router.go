package router

import (
	"github.com/labstack/echo"
	"github.com/labstack/echo/middleware"
	log "github.com/sirupsen/logrus"
	controller "gitlab.com/crawler/interface/controllers"
)

func NewRouter(e *echo.Echo, c controller.AppController) *echo.Echo {
	log.Debug("Create app router")
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	e.GET("/classifieds", func(context echo.Context) error { return c.GetClassifieds(context) })

	return e
}
