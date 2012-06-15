from django import forms

from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.bootstrap import FormActions

from rentalerts.apps.core.forms import ModelForm
from rentalerts.apps.pm.models import Message


class MessageForm(ModelForm):

    layout = Layout(
        Fieldset(
            'Send Message',
            'subject',
            'message'
        ),
        FormActions(
            Submit('send', 'Send', css_class='btn btn-primary'),
        )
    )

    class Meta:
        model = Message
        
        fields = ('subject', 'message',)


class ReplyMessageForm(MessageForm):
    layout = Layout(
        Fieldset(
            'Reply to Message',
            'subject',
            'message'
        ),
        FormActions(
            Submit('send', 'Send', css_class='btn btn-primary'),
        )
    )


