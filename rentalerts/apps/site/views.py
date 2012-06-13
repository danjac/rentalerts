# top-level views for the project, which don't belong in any specific app

from django.shortcuts import redirect
from django.views.generic.base import TemplateView

from rentalerts.apps.accounts.decorators import login_required

class HomePage(TemplateView):

    template_name = "index.html"

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated():
            return redirect("site:dashboard")

        return super(HomePage, self).get(request, *args, **kwargs)


class AboutPage(TemplateView):

    template_name = "about.html"


@login_required
class Dashboard(TemplateView):

    template_name = "dashboard.html"




    


