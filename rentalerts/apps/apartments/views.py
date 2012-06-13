from django.http import HttpResponseRedirect
from django.views.generic import RedirectView

from django.views.generic.detail import (
    DetailView, 
    SingleObjectMixin
)

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

from rentalerts.apps.accounts.decorators import login_required
from rentalerts.apps.bookmarks.models import Bookmark
from rentalerts.apps.apartments.models import Apartment
from rentalerts.apps.apartments.forms import ApartmentForm


class ApartmentList(ListView):

    def get_queryset(self):
        return Apartment.objects.available().order_by('-added_on')


class SearchApartments(ListView):

    template_name = "apartments/search.html"

    def get(self, request, *args, **kwargs):

        self.search = request.GET.get('search', '').strip()

        return super(SearchApartments, self).get(request, *args, **kwargs)

    def get_queryset(self):

        if not self.search:
            return Apartment.objects.none()

        return Apartment.objects.search(self.search).available()

    def get_context_data(self, **kwargs):

        context = super(SearchApartments, self).get_context_data(**kwargs)
        context['search'] = self.search
        return context


class ApartmentDetail(DetailView):

    model = Apartment
    template_object_name = "apartment"

    def get_bookmark(self):

        if not self.request.user.is_authenticated():
            return

        try:
            return Bookmark.objects.get(
                apartment=self.object,
                user=self.request.user
            )
        except Bookmark.DoesNotExist:
            pass

    def get_context_data(self, **kwargs):

        context = super(ApartmentDetail, self).get_context_data(**kwargs)

        is_owner = self.request.user.id == self.object.tenant_id

        context.update({
            'is_owner' : is_owner,
            'is_editable' : is_owner or self.request.user.is_staff,
            'bookmark' : self.get_bookmark(),
        })

        return context


@login_required
class CreateApartment(CreateView):

    model = Apartment
    form_class = ApartmentForm

    def form_valid(self, form):

        obj = form.save(commit=False)
        obj.tenant = self.request.user
        obj.save()

        # message/email

        return HttpResponseRedirect(obj.get_absolute_url())


class ApartmentEditableMixin(object):

    def get_queryset(self):

        if self.request.user.is_staff:
            return Apartment.objects.all()
        else:
            return self.request.user.apartment_set.all()


@login_required
class UpdateApartment(ApartmentEditableMixin, UpdateView):

    form_class = ApartmentForm


@login_required
class RemoveApartment(ApartmentEditableMixin, SingleObjectMixin, RedirectView):

    """
    Makes the apartment unavailable.
    """

    def get_redirect_url(self, **kwargs):

        return self.object.get_absolute_url()

    def get(self, request, *args, **kwargs):

        self.object = self.get_object()
        self.object.is_available = False
        self.object.save()

        return super(RemoveApartment, self).get(request, *args, **kwargs)


@login_required
class AddApartment(ApartmentEditableMixin, SingleObjectMixin, RedirectView):

    """
    Makes the apartment available again.
    """

    def get_redirect_url(self, **kwargs):

        return self.object.get_absolute_url()

    def get(self, request, *args, **kwargs):

        self.object = self.get_object()
        self.object.is_available = True
        self.object.save()

        return super(AddApartment, self).get(request, *args, **kwargs)





    


    
