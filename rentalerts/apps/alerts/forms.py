
from django import forms

from crispy_forms.layout import Layout, Fieldset, Div, Submit
from crispy_forms.bootstrap import FormActions

from rentalerts.apps.helpers.forms import ModelForm
from rentalerts.apps.helpers.forms.fields import GroupedModelMultipleChoiceField
from rentalerts.apps.apartments.models import Area, Apartment
from rentalerts.apps.alerts.models import Search


class SearchForm(ModelForm):

    areas = GroupedModelMultipleChoiceField(
        'city',
        Area.objects.select_related('city').order_by(
            'city', 'name',   
        ),
        required=False,
    )

    num_rooms = forms.TypedChoiceField(
        coerce=int,
        choices=Apartment.ROOM_CHOICES,
        widget=forms.RadioSelect,
        initial=1,
    )

    sauna = forms.TypedChoiceField(
        coerce=int,
        choices=Apartment.SAUNA_CHOICES,
        widget=forms.RadioSelect,
        initial=Apartment.SAUNA_NONE,
    )
    

    layout = Layout(
        Fieldset(
            'Alert Settings',
            'email', 

            Div(
                Div(
                    'areas', 'num_rooms', 'sauna',
                    'rent_pcm', 'size', 'non_shared',
                    css_class="span6",
                ),
                Div(
                    'cable', 'broadband', 'balcony',
                    'parking', 'laundry', 'pets', 'smoking',
                    css_class="span6",
                ),
                css_class="row",
            ),
                
        ),

        FormActions(
           Submit('save', 'Save', css_class='btn btn-large btn-primary'),
        ),
        
    )


    class Meta:

        model = Search
        exclude = (
            'user',
        ) 

