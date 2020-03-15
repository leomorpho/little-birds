package repository

import (
	"github.com/jinzhu/gorm"
	"gitlab.com/crawler/domain/model"
)

type classifiedsRepository struct {
	db *gorm.DB
}

type ClassifiedsRepository interface {
	FindAll(c []*model.Classifieds) ([]*model.Classifieds, error)
}

func NewClassifiedsRepository(db *gorm.DB) ClassifiedsRepository {
	return &classifiedsRepository{db}
}

func (cr *classifiedsRepository) FindAll(c []*model.Classifieds) ([]*model.Classifieds, error) {
	err := cr.db.Find(&c).Error
	if err != nil {
		return nil, err
	}

	return c, nil
}
