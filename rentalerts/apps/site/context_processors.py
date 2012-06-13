from django.conf import settings

def google_api_key(request):
    """
    Gets the Google map key
    """

    return {'GOOGLE_API_KEY' : settings.GOOGLE_API_KEY}
