from django.utils.decorators import method_decorator

def make_view_decorator(decorator, *args, **kwargs):
    """
    Creates a class decorator which decorates the 
    dispatch method of the view with a normal view decorator.

    Example:

    login_required = decorate_view(login_required)

    @login_required
    class MyView(TemplateView):

        ....
    """

    def _decorate(view_class):

        view_class.dispatch = method_decorator(
            decorator, *args, **kwargs
        )(view_class.dispatch)

        return view_class

    return _decorate


