package registry

func (r *registry) NewClassifiedssController() controller.ClassifiedssController {
	return controller.NewClassifiedssController(r.NewClassifiedssInteractor())
}
