package registry

import (
	"github.com/jinzhu/gorm"
	log "github.com/sirupsen/logrus"
	controller "gitlab.com/crawler/interface/controllers"
)

type registry struct {
	db *gorm.DB
}

type Registry interface {
	NewAppController() controller.AppController
}

func NewRegistry(db *gorm.DB) Registry {
	return &registry{db}
}

func (r *registry) NewAppController() controller.AppController {
	log.Debug("Create app controller")
	var appController controller.AppController
	return appController
}
