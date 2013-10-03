from hashlib import md5
from urllib import urlencode

from django import template

from knowledge import settings

if settings.DJANGO_KNOWLEDGE_MARKUP == 'Markdown':
    import markdown
elif settings.DJANGO_KNOWLEDGE_MARKUP == 'Textile':
    import textile

register = template.Library()


@register.simple_tag
def get_gravatar(email, size=60, rating='g', default=None):
    """ Return url for a Gravatar. From Zinnia blog. """
    url = 'https://secure.gravatar.com/avatar/{0}.jpg'.format(
        md5(email.strip().lower()).hexdigest()
    )
    options = {'s': size, 'r': rating}
    if default:
        options['d'] = default

    url = '%s?%s' % (url, urlencode(options))
    return url.replace('&', '&amp;')


@register.simple_tag
def page_query(request, page_num):
    qs = request.GET.copy()
    qs['page'] = page_num
    return qs.urlencode().replace('&', '&amp;')

@register.simple_tag
def render_markup(bodyblock):
    """
    Based on setting value, convert body text using
    the correct renderer, else just return string
    """
    if settings.DJANGO_KNOWLEDGE_MARKUP == 'Markdown':
        return markdown.markdown(bodyblock)
    elif settings.DJANGO_KNOWLEDGE_MARKUP == 'Textile':
        return textile.textile(bodyblock)
    else:
        return bodyblock
