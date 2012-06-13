from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    UserCreationForm, 
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)


from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.bootstrap import FormActions

from rentalerts.apps.helpers.forms import LayoutMixin, ModelForm


class PasswordChangeForm(LayoutMixin, PasswordChangeForm):
    
    layout = Layout(
        Fieldset(
            'Change your password',
            'old_password', 
            'new_password1', 
            'new_password2',
        ),
        FormActions(
            Submit('save', 'Save', css_class='btn btn-primary')
        )
    )


class SetPasswordForm(LayoutMixin, SetPasswordForm):

    layout = Layout(
        Fieldset(
            'Enter new password',
            'new_password1',
            'new_password2',
        ),
        FormActions(
            Submit('save', 'Change password', css_class="btn btn-primary")
        )
    )


class PasswordResetForm(LayoutMixin, PasswordResetForm):

    layout = Layout(
        Fieldset(
            'Reset your password',
            'email',
        ),
        FormActions(
            Submit('reset', 'Reset', css_class='btn btn-primary')
        )
            
    )


class LoginForm(LayoutMixin, AuthenticationForm):

    next = forms.CharField(widget=forms.HiddenInput, required=False)

    layout = Layout(
        Fieldset(
            'Login',
            'username', 
            'password',
            'next',
        ),
        FormActions(
            Submit('login', 'Login',
                css_class='btn btn-primary'),
        )
    )

    def get_next_url(self):

        return self.cleaned_data['next'] or settings.LOGIN_REDIRECT_URL
    

class AccountSettingsForm(ModelForm):

    first_name = forms.CharField(
        max_length=30,
        required=True,
    )

    last_name = forms.CharField(
        max_length=30,
        required=True,
    )



    layout = Layout(
        Fieldset(
            'Account Settings',
            'first_name',
            'last_name',
            'email',
        ),

        FormActions(
            Submit('save', 'Update', css_class='btn btn-primary')

        )
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_email(self):

        email = self.cleaned_data['email']

        qs = User.objects.filter(email__iexact=email)
        if self.instance and self.instance.id:
            qs = qs.exclude(pk=self.instance.id)

        if qs.exists():
            raise forms.ValidationError(
                'A user with this email address already exists'
            )

        return email


class RegistrationForm(LayoutMixin, UserCreationForm):

    next = forms.CharField(widget=forms.HiddenInput, required=False)
    email = forms.EmailField(label=u'Email address')    

    tandc = forms.BooleanField(
            widget=forms.CheckboxInput(attrs={'class' : 'inline'}),
            label=u'Yes, I have read and agree to the '
                  u'<a target="_blank" href="">Terms and conditions</a>')

    layout = Layout(
        
        Fieldset(
            '',
            'username', 'email', 
            'first_name', 'last_name',
            'password1', 'password2',
            'tandc',
            'next',
        ),
        
        FormActions(
            Submit('save', 'Sign up', 
                   css_class='btn btn-primary'),
        )

    )

    first_name = forms.CharField(
        max_length=30,
        required=True,
    )

    last_name = forms.CharField(
        max_length=30,
        required=True,
    )


    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name',
        )

    def get_next_url(self):

        return self.cleaned_data.get('next', None)
 
    def clean_email(self):

        email = self.cleaned_data['email']

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'A user with this email address already exists'
            )

        return email

    def save(self, commit=True):

        user = super(RegistrationForm, self).save(commit)
        if commit:
            username = self.cleaned_data['username']
            password = self.cleaned_data['password1']

            user = authenticate(username=username, password=password)
        return user







