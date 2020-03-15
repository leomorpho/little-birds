package interactor

import (
	"gitlab.com/crawler/domain/model"
	"gitlab.com/crawler/usecase/presenter"
	"gitlab.com/crawler/usecase/repository"
)

type classifiedsInteractor struct {
	ClassifiedsRepository repository.ClassifiedsRepository
	ClassifiedsPresenter  presenter.ClassifiedsPresenter
}

type ClassifiedsInteractor interface {
	Get(c []*model.Classifieds) ([]*model.Classifieds, error)
}

func NewClassifiedsInteractor(r repository.ClassifiedsRepository, p presenter.ClassifiedsPresenter) ClassifiedsInteractor {
	return &classifiedsInteractor{r, p}
}

func (ci *classifiedsInteractor) Get(c []*model.Classifieds) ([]*model.Classifieds, error) {
	c, err := ci.ClassifiedsRepository.FindAll(c)
	if err != nil {
		return nil, err
	}

	return ci.ClassifiedsPresenter.ResponseClassifieds(c), nil
}
