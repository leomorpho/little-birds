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
	GetClassifieds(c Context) error
}

func NewClassifiedsController(cc interactor.ClassifiedsInteractor) ClassifiedsController {
	return &classifiedsController{cc}
	c
}

func (cc *classifiedsController) GetClassifieds(c Context) error {
	var c []*model.Classifieds

	u, err := cc.classifiedsInteractor.Get(c)
	if err != nil {
		return err
	}

	return c.JSON(http.StatusOK, u)
}
