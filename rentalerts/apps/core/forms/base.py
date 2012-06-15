from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout


class LayoutMixin(object):

    layout = Layout()

    form_method = 'POST'
    form_action = None
    form_class = "form-horizontal"

    def __init__(self, *args, **kwargs):

        form_method = kwargs.pop('form_method', self.form_method)
        form_action = kwargs.pop('form_action', self.form_action)
        form_class = kwargs.pop('form_class', self.form_class)
        layout = kwargs.pop('layout', self.layout)

        self.helper = FormHelper()
        self.helper.form_method = form_method
        self.helper.form_action = form_action or '.'
        self.helper.form_class = form_class

        self.helper.layout = layout

        super(LayoutMixin, self).__init__(*args, **kwargs)


class Form(LayoutMixin, forms.Form):
    pass



class ModelForm(LayoutMixin, forms.ModelForm):
    pass




