package interactor

import (
	"gitlab.com/crawler/domain/model"
	"gitlab.com/crawler/usecase/presenter"
	"gitlab.com/crawler/usecase/repository"
)

type classifiedInteractor struct {
	ClassifiedRepository repository.ClassifiedRepository
	ClassifiedPresenter  presenter.ClassifiedPresenter
}

type ClassifiedInteractor interface {
	Get(c []*model.Classified) ([]*model.Classified, error)
}

func NewClassifiedInteractor(r repository.ClassifiedRepository, p presenter.ClassifiedPresenter) ClassifiedInteractor {
	return &classifiedInteractor{r, p}
}

func (ci *classifiedInteractor) Get(c []*model.Classified) ([]*model.Classified, error) {
	c, err := ci.ClassifiedRepository.FindAll(c)
	if err != nil {
		return nil, err
	}

	return ci.ClassifiedPresenter.ResponseClassified(c), nil
}
