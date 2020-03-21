package router

import (
	"github.com/labstack/echo"
	"github.com/labstack/echo/middleware"
	controller "gitlab.com/crawler/interface/controllers"
)

func NewRouter(e *echo.Echo, c controller.AppController) *echo.Echo {
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	e.GET("/classifieds", func(context echo.Context) error { return c.GetClassifieds(context) })

	return e
}
