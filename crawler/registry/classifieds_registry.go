package registry

import (
	controller "gitlab.com/crawler/interface/controllers"
	"gitlab.com/crawler/interface/repository"
	"gitlab.com/crawler/usecase/interactor"
	"gitlab.com/crawler/usecase/presenter"
)

func (r *registry) NewClassifiedsController() controller.ClassifiedsController {
	return controller.NewClassifiedsController(r.NewClassifiedsInteractor())
}

func (r *registry) NewClassifiedsInteractor() interactor.ClassifiedsInteractor {
	return interactor.NewClassifiedsInteractor(r.NewClassifiedsRepository(), r.NewClassifiedsPresenter())
}

func (r *registry) NewClassifiedsRepository() repository.ClassifiedsRepository {
	return repository.NewClassifiedsRepository(r.db)
}

func (r *registry) NewClassifiedsPresenter() presenter.ClassifiedsPresenter {
	return presenter.NewClassifiedsPresenter()
}
