from django import template
from django.conf import settings
from django.http import Http404
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import resolve, reverse, NoReverseMatch
from django.forms.fields import TypedChoiceField
from django.contrib.sites.models import Site

register = template.Library()



@register.filter
def ischecked(field, choice):
    """
    """

    value = field.value()

    if not isinstance(field.field, TypedChoiceField):
        return value == choice

    try:
        return field.field.coerce(value) == choice
    except (TypeError, ValueError):
        return value == choice

    

@register.simple_tag(takes_context=True)
def absoluteuri(context, path, *args, **kwargs):
    """
    Creates a full site URL.

    If "request" is available will use that;
    otherwise will use current Site to guess the 
    url. 

    As protocol is not included, assumes http - to 
    change this set:

    SITE_PROTOCOL = 'https'

    in settings.

    If path/args is a named URL will use that,
    otherwise will assume path is a string.
    """

    try:
        path = reverse(path, args=args, kwargs=kwargs)
    except NoReverseMatch:
        if '/' not in path and '.' not in path:
            raise

    request = context.get('request', None)
    if request:
        return request.build_absolute_uri(path)

    site = Site.objects.get_current()

    protocol = getattr(settings, 'SITE_PROTOCOL', 'http')

    return "%s://%s%s" % (protocol, site.domain, path)



@register.simple_tag(takes_context=True)
def activetab(context, namespace, name=None, content=None):
    """
    Returns given string if named pattern matches current url.

    You can pass a specific view or a whole namespace, for example:

    {% activetab messages %} - matches if current namespace is 'messages'
    {% activetab messages list %} - matches if current namespace 'messages',
    and current view 'list'.
    """

    try:

        request = context['request']

    except KeyError:
        raise ImproperlyConfigured(
            "You must include django.core.context_processors.request"
            " in TEMPLATE_CONTEXT_PROCESSORS"
        )

   
    try:
        match = resolve(request.path)
    except Http404:
        return ''

    if name: # check view name
        
        if match.url_name != name:
            return ''

    parts = namespace.split(":")
    parts.reverse()

    while parts:
        ns = parts.pop()
        if ns not in match.namespaces:
            return ''

    if content is None:
        content = ' class="active"'

    return content

    


