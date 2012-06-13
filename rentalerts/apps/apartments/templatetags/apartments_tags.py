from django import template
from django.core.exceptions import ImproperlyConfigured


from rentalerts.apps.apartments.models import Apartment


register = template.Library()

@register.tag
def get_latest_apartments(parser, token):
    """
    Example:

    {% get_latest_apartments 10 as apts %}
    """

    return _get_apartments_list_node(
        LatestApartmentListNode, parser, token
    )



def _get_apartments_list_node(node_class, parser, token):

    tokens = token.contents.split()[1:]
    num_tokens = len(tokens)

    if num_tokens not in (2, 3):
        raise template.TemplateSyntaxError(
            "Invalid number of args"
        )


    if num_tokens == 2:
        as_, varname = tokens
        limit = None
    elif num_tokens == 3:
        limit, as_, varname = tokens


    return node_class(limit, varname)



class ApartmentListNode(template.Node):

    def get_queryset(self, context):

        raise NotImplementedError

    def __init__(self, limit, varname):

        self.limit = limit
        self.varname = varname

    def render(self, context):

        qs = self.get_queryset(context)
        if self.limit:
            qs = qs[:self.limit]

        context[self.varname] = qs

        return ''


class LatestApartmentListNode(ApartmentListNode):

    def get_queryset(self, context):

        return Apartment.objects.available().order_by('available_from')


class MyApartmentListNode(ApartmentListNode):

    def get_queryset(self, context):

        try:

            request = context['request']

        except KeyError:
            raise ImproperlyConfigured(
                "You must include django.core.context_processors.request"
                " in TEMPLATE_CONTEXT_PROCESSORS"
            )
        
        if request.user.is_authenticated():
            return request.user.apartment_set.all()

        return Apartment.objects.none()
 

    
            




