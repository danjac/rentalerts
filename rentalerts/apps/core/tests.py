from django import forms
from django.db import models
from django.test import TestCase
from django.test.client import RequestFactory
from django.template import Context
from django.core import mail
from django.core.urlresolvers import NoReverseMatch
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User

from rentalerts.apps.core.forms import LayoutMixin, Form, ModelForm

from rentalerts.apps.core.forms.fields import (
    GroupedModelChoiceField, 
    GroupedModelMultipleChoiceField
)

from rentalerts.apps.core.templatetags.core_tags import (
    activetab,
    absoluteuri,
)

from rentalerts.apps.core.utils.email import send_email_from_template


class SomeModel(models.Model):

    name = models.CharField(max_length=30)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.name


class EmailTests(TestCase):

    def test_send_email_from_template(self):

        send_email_from_template(
            subject="Just testing",
            recipient_list=["danjac@helsinkirentalerts.fi"],
            template="test_message.txt",
            context=Context({}),
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assert_("[Helsinki RentAlerts] Just testing" == mail.outbox[0].subject)
        self.assert_("Just testing" in mail.outbox[0].body)


class FormTests(TestCase):

    def test_layout_mixin(self):

        class MyForm(LayoutMixin, forms.Form):

            name = forms.CharField()

        form = MyForm()
        self.assert_(form.helper)
        self.assert_(form.helper.layout)

    def test_form(self):

        class MyForm(Form):

            name = forms.CharField()

        form = MyForm()
        self.assert_(form.helper)
        self.assert_(form.helper.layout)

    def test_model_form(self):

        class MyForm(ModelForm):

            name = forms.CharField()
        
            class Meta:
                model = User

        form = MyForm()
        self.assert_(form.helper)
        self.assert_(form.helper.layout)

    def test_grouped_model_choice_field(self):

        valid_obj_ids = []

        for i in xrange(3):
            user = User.objects.create_user(
                "tester--%d" % i,
                "tester-%d@gmail.com" % i,
                "test"
            )

            for j in xrange(3):

                obj = SomeModel.objects.create(
                    name="test-%d" % j,
                    user=user
                )
                valid_obj_ids.append(obj.id)
            
        class MyForm(forms.Form):

            obj = GroupedModelChoiceField(
                grouper='user',
                queryset=SomeModel.objects.all()
            )

        form = MyForm()
        self.assert_('<optgroup label="tester--0">' in unicode(form))

        form = MyForm({'obj' : valid_obj_ids[0]}) 
        self.assert_(form.is_valid())

        form = MyForm({'obj' : 2000})
        self.assert_(not form.is_valid())
        self.assert_("Select a valid choice" in unicode(form.errors))


    def test_grouped_model_multiple_choice_field(self):

        valid_obj_ids = []

        for i in xrange(3):
            user = User.objects.create_user(
                "tester--%d" % i,
                "tester-%d@gmail.com" % i,
                "test"
            )

            for j in xrange(3):

                obj = SomeModel.objects.create(
                    name="test-%d" % j,
                    user=user
                )
                valid_obj_ids.append(obj.id)
            
        class MyForm(forms.Form):

            objects = GroupedModelMultipleChoiceField(
                grouper='user',
                queryset=SomeModel.objects.all()
            )

        form = MyForm()
        self.assert_('<optgroup label="tester--0">' in unicode(form))

        form = MyForm({'objects' : valid_obj_ids}) 
        self.assert_(form.is_valid())

        form = MyForm({'objects' : [2000]})
        self.assert_(not form.is_valid())
        self.assert_("Select a valid choice" in unicode(form.errors))



class TemplateTagTests(TestCase):

    def _make_request(self, url="/", **kwargs):
        return RequestFactory().get(url, **kwargs)

    def test_absoluteuri_if_request_context(self):

        req = self._make_request()
        content = absoluteuri({'request' : req}, '/')
        self.assertEqual(content, 'http://testserver/')

    def test_absoluteuri_if_no_request_context(self):

        # should fall back on site
        content = absoluteuri({}, '/')
        self.assertEqual(content, 'http://example.com/')

    def test_absoluteuri_if_https_and_no_request(self):
        with self.settings(SITE_PROTOCOL='https'):
            content = absoluteuri({}, '/')
        self.assertEqual(content, 'https://example.com/')

    def test_absoluteuri_if_bad_url(self):

        self.assertRaises(
            NoReverseMatch,
            absoluteuri,
            {},
            "jkjd",
        )


    def test_activetab_if_missing_request(self):

        self.assertRaises(
            ImproperlyConfigured,
            activetab,
            {},
            'site', 'home',
        )
    
    def test_activetab_if_not_correct_url(self):

        content = activetab(
            {'request' : self._make_request()},
            'foo', 'bar',
        )

        self.assertEqual(content, '')

    def test_activetab_if_not_current_url(self):

        content = activetab(
            {'request' : self._make_request('/foo/')},
            'site', 'home',
        )

        self.assertEqual(content, '')


    def test_activetab_if_not_namespace(self):

        req = self._make_request()
        req.path = "/"

        content = activetab({'request' : req}, 'site')

        self.assertEqual(content, ' class="active"')

    def test_activetab_if_not_correct_namespace(self):
        
        req = self._make_request()
        req.path = "/"

        content = activetab({'request' : req}, 'foo')

        self.assertEqual(content, '')




    def test_activetab_if_current_url(self):

        req = self._make_request()
        req.path = "/"

        content = activetab(
            {'request' : req},
            'site', 'home',
        )

        self.assertEqual(content, ' class="active"')
