package presenter

import "gitlab.com/crawler/domain/model"

type ClassifiedsPresenter interface {
	ResponseClassifieds(c []*model.Classifieds) []*model.Classifieds
}
