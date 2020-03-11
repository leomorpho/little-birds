package presenter

import "gitlab.com/crawler/domain/model"

type ClassifiedPresenter interface {
	ResponseClassified(c []*model.Classified) []*model.Classified
}
