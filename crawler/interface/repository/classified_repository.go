package repository

import (
	"github.com/jinzhu/gorm"
	"gitlab.com/crawler/domain/model"
)

type classifiedRepository struct {
	db *gorm.DB
}

type ClassifiedRepository interface {
	FindAll(c []*model.Classified) ([]*model.Classified, error)
}

func NewClassifiedRepository(db *gorm.DB) ClassifiedRepository {
	return &classifiedRepository{db}
}

func (cr *classifiedRepository) FindAll(c []*model.Classified) ([]*model.Classified, error) {
	err := cr.db.Find(&c).Error
	if err != nil {
		return nil, err
	}

	return c, nil
}
