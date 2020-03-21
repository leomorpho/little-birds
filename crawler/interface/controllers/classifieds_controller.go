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
}

func (cc *classifiedsController) GetClassifieds(co Context) error {
	var cl []*model.Classifieds

	cl, err := cc.classifiedsInteractor.Get(cl)
	if err != nil {
		return err
	}

	return co.JSON(http.StatusOK, cl)
}
