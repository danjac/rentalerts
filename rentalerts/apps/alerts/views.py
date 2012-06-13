from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.views.generic import RedirectView
from django.views.generic.edit import UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import ListView
from django.contrib import messages

from rentalerts.apps.accounts.decorators import login_required
from rentalerts.apps.alerts.models import Search
from rentalerts.apps.alerts.forms import SearchForm


@login_required
class AlertList(ListView):

    def get_queryset(self):
        return self.request.user.alert_set.select_related(
            'apartment',
        ).available()


@login_required
class DeleteAlert(SingleObjectMixin, RedirectView):

    def get_queryset(self):

        return self.request.user.alert_set

    def get_redirect_url(self, **kwargs):

        return reverse('alerts:list')

    def get(self, request, *args, **kwargs):

        alert = self.get_object()
        alert.is_deleted = True
        alert.save()

        messages.success(self.request, "Your alert has been deleted")

        return super(DeleteAlert, self).get(request, *args, **kwargs)


@login_required
class EditSearch(UpdateView):

    form_class = SearchForm

    def get_object(self):

        obj, created = Search.objects.get_or_create(user=self.request.user)

        return obj

    def form_valid(self, form):

        search = form.save()
        search.create_alerts()

        messages.success(self.request, "Your alert settings have been updated")

        return redirect("alerts:list")


