package repository

import "gitlab.com/crawler/domain/model"

type ClassifiedsRepository interface {
	FindAll(p []*model.Classifieds) ([]*model.Classifieds, error)
}
