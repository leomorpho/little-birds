package controller

import (
	"net/http"

	"gitlab.com/crawler/domain/model"
	"gitlab.com/crawler/usecase/interactor"
)

type classifiedController struct {
	classifiedInteractor interactor.ClassifiedInteractor
}

type ClassifiedController interface {
	GetClassifieds(c Context) error
}

func NewClassifiedController(cc interactor.ClassifiedInteractor) ClassifiedController {
	return &classifiedController{cc}
}

func (cc *classifiedController) GetClassifieds(c Context) error {
	var c []*model.Classified

	u, err := cc.classifiedInteractor.Get(c)
	if err != nil {
		return err
	}

	return c.JSON(http.StatusOK, u)
}
