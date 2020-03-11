package repository

import "gitlab.com/crawler/domain/model"

type ClassifiedRepository interface {
	FindAll(p []*model.Classified) ([]*model.Classified, error)
}
