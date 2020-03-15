package controller

import (
	"net/http"

	"gitlab.com/crawler/domain/model"
	"gitlab.com/crawler/usecase/interactor"
)

type classifiedsController struct {
	classifiedsInteractor interactor.ClassifiedsInteractor
}

type ClassifiedsController interface {
	GetClassifiedss(c Context) error
}

func NewClassifiedsController(cc interactor.ClassifiedsInteractor) ClassifiedsController {
	return &classifiedsController{cc}
}

func (cc *classifiedsController) GetClassifiedss(c Context) error {
	var c []*model.Classifieds

	u, err := cc.classifiedsInteractor.Get(c)
	if err != nil {
		return err
	}

	return c.JSON(http.StatusOK, u)
}
