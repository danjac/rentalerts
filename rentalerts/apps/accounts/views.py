
from django.conf import settings
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView, FormView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

from rentalerts.apps.accounts.forms import RegistrationForm, AccountSettingsForm, LoginForm
from rentalerts.apps.accounts.decorators import login_required


@login_required
class Settings(TemplateView):

    template_name = "accounts/settings.html"


@login_required
class AccountSettings(UpdateView):

    form_class = AccountSettingsForm
    template_name = "accounts/account_settings.html"

    def get_success_url(self):
        return reverse("accounts:settings")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):

        response = super(AccountSettings, self).form_valid(form)
        messages.success(self.request, "Your settings have been updated")
        return response


    
class Register(CreateView):

    model = User 
    form_class = RegistrationForm
    template_name = "accounts/register.html"

    def get_initial(self):
        return {'next' : self.request.GET.get('next')}

    def form_valid(self, form):

        user = form.save()
        login(self.request, user)

        next_url = form.get_next_url()
        
        if next_url:
            return redirect(next_url)

        return redirect('accounts:register_success')


class RegisterSuccess(TemplateView):

    template_name = "accounts/register_success.html"


class Login(FormView):

    form_class = LoginForm
    template_name = "accounts/login.html"

    def dispatch(self, request, *args, **kwargs):

        request.session.set_test_cookie()
        return super(Login, self).dispatch(request, *args, **kwargs)

    def get_next_url(self):

        return self.request.GET.get('next', '')

    def get_initial(self):
        return {'next' : self.get_next_url()}

    def get_form_kwargs(self):

        kwargs = super(Login, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):

        user = form.get_user()
        login(self.request, user)

        username = user.first_name or user.username

        messages.success(self.request, u"Welcome back %s" % username)

        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        self.success_url = form.get_next_url()

        return super(Login, self).form_valid(form)

    def get_context_data(self, **kwargs):

        context = super(Login, self).get_context_data(**kwargs)
        context['next'] = self.get_next_url()
        return context


class Logout(RedirectView):

    def get_redirect_url(self):
        return reverse("site:home")

    def get(self, request):

        logout(request)
        messages.success(request, "Bye for now!")

        return super(Logout, self).get(request)



