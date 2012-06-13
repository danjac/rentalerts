
from django.views.generic import RedirectView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import ListView
from django.contrib import messages


from rentalerts.apps.apartments.models import Apartment
from rentalerts.apps.accounts.decorators import login_required
from rentalerts.apps.bookmarks.models import Bookmark


@login_required
class BookmarkList(ListView):

    def get_queryset(self):

        return self.request.user.bookmark_set.select_related(
            'apartment',
            'apartment__area',
            'apartment__area__city',
        )


@login_required
class DeleteBookmark(SingleObjectMixin, RedirectView):

    def get_queryset(self):

        return self.request.user.bookmark_set

    def get_redirect_url(self, **kwargs):

        return self.object.get_absolute_url()

    def get(self, request, *args, **kwargs):

        self.object = self.get_object()
        self.object.delete()

        messages.success(
            request,
            "Your bookmark has been deleted"
        )

        return super(DeleteBookmark, self).get(request, *args, **kwargs)

        
@login_required
class CreateBookmark(SingleObjectMixin, RedirectView):

    model = Apartment

    def get_redirect_url(self, **kwargs):

        return self.object.get_absolute_url()

    def get(self, request, *args, **kwargs):

        self.object = self.get_object()

        if Bookmark.objects.filter(
            user=self.request.user,
            apartment=self.object).exists():

            messages.error(
                request,
                "You've already bookmarked this apartment"
            )
 
        else:

            bookmark = Bookmark.objects.create(
                user=self.request.user,
                apartment=self.object,
            )

            messages.success(
                self.request,
                "You've added a bookmark to %s" % self.object
            )
        
        return super(CreateBookmark, self).get(request, *args, **kwargs)
        

