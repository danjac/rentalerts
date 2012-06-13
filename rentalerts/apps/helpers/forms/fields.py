import operator
import itertools


from django import forms
from django.utils.encoding import smart_unicode
from django.forms.models import ModelChoiceIterator


class GroupedModelChoiceIterator(object):

    def __init__(self, field, grouper):

        self.field = field
        self.grouper = grouper
        self.queryset = self.field.queryset

    def __iter__(self):

        if self.field.empty_label is not None:
            yield (u'', self.field.empty_label)

        for grouper, items in itertools.groupby(
                self.queryset.all(), 
                operator.attrgetter(self.grouper)):

            yield (unicode(grouper), 
                   tuple((obj.pk, unicode(obj)) for obj in items))


class GroupedModelChoiceField(forms.ModelChoiceField):    

    def __init__(self, grouper, *args, **kwargs):

        self.grouper = grouper
        super(GroupedModelChoiceField, self).__init__(*args, **kwargs)

    def _get_choices(self):
        return GroupedModelChoiceIterator(self, self.grouper)

    choices = property(_get_choices, None)

    def clean(self, value):

        value = smart_unicode(value or '')

        valid_values = []

        for choice in self.choices:
            try:
                group_label, group = choice
                valid_values += [str(k) for k, v in group]
            except ValueError:
                pass
        
        if value not in valid_values:
            raise forms.ValidationError("Select a valid choice") # use right msg

        return super(GroupedModelChoiceField, self).clean(value)


class GroupedModelMultipleChoiceField(forms.ModelMultipleChoiceField):    

    def __init__(self, grouper, *args, **kwargs):

        self.grouper = grouper
        super(GroupedModelMultipleChoiceField, self).__init__(*args, **kwargs)

    def _get_choices(self):
        return GroupedModelChoiceIterator(self, self.grouper)

    choices = property(_get_choices, None)

    def clean(self, value):

        value = [smart_unicode(v or '') for v in value]
        valid_values = []

        for group_label, group in self.choices:
            valid_values += [str(k) for k, v in group]

        for v in value:
            if v not in valid_values:
                raise forms.ValidationError(
                    self.error_messages['invalid_choice'])

        return super(GroupedModelMultipleChoiceField, self).clean(value)









