from django import forms
from django.contrib.localflavor.fi.forms import FIZipCodeField

from crispy_forms.layout import Layout, Fieldset, Div, Submit
from crispy_forms.bootstrap import FormActions

from rentalerts.apps.core.forms import ModelForm
from rentalerts.apps.core.forms.fields import GroupedModelChoiceField
from rentalerts.apps.apartments.models import Apartment, Area


class ApartmentForm(ModelForm):

    area = GroupedModelChoiceField(
        grouper='city',
        queryset=Area.objects.select_related('city').order_by(
            'city', 'name',   
        ),
    )

    num_rooms = forms.TypedChoiceField(
        coerce=int,
        choices=Apartment.ROOM_CHOICES,
        widget=forms.RadioSelect,
        initial=1,
    )


    landlord = forms.TypedChoiceField(
        coerce=int,
        choices=Apartment.LANDLORD_CHOICES,
        widget=forms.RadioSelect,
        initial=Apartment.LANDLORD_PRIVATE,
    )


    sauna = forms.TypedChoiceField(
        coerce=int,
        choices=Apartment.SAUNA_CHOICES,
        widget=forms.RadioSelect,
        initial=Apartment.SAUNA_NONE,
    )

    postcode = FIZipCodeField()

    layout = Layout(
        Fieldset(
            'Location',
            'area', 'address', 'postcode',
        ),

        Fieldset(
            'Basic Details',
            'description',
            Div(
                'num_rooms', 'size', 
                'floor', 'num_floors', 'lift',
                css_class="span6"
            ),
            Div(
                'landlord', 'agency', 'agency_website',
                'is_shared', 'rent_pcm', 'deposit',
                'available_from', 'available_to',  
                css_class="span6"
            ),
                        
            css_class="row"
        ),

        Fieldset(
            "What's allowed",
            'pets', 'smoking',
        ),

        Fieldset(
            'Amenities',
            Div(
                'cable', 'broadband', 'satellite', 
                'balcony', 'laundry', 
                css_class="span6",
            ),
            Div(
                'parking', 'garage',
                'extra_storage', 'bike_storage',
                'gym',
                css_class="span6",
            ),
            
            css_class="row"
        ),

        Fieldset(
            'Other amenities',
            'sauna', 'kitchen_amenities',
            'furnished', 'furniture', 'heating',
            'other_amenities',
        ),

        FormActions(
           Submit('save', 'Save', css_class='btn btn-large btn-primary'),
        ),
        
    )


    class Meta:

        model = Apartment
        exclude = (
            'type', 'tenant', 'is_available', 'garden_size',
            'latitude', 'longitude',
        ) 

