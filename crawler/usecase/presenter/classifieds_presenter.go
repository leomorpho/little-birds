package presenter

import "gitlab.com/crawler/domain/model"

type classifiedsPresenter struct{}
type ClassifiedsPresenter interface {
	ResponseClassifieds(c []*model.Classifieds) []*model.Classifieds
}

func NewClassifiedsPresenter() ClassifiedsPresenter {
	return &classifiedsPresenter{}
}

func (cp *classifiedsPresenter) ResponseClassifieds(c []*model.Classifieds) []*model.Classifieds {
	return c
}
