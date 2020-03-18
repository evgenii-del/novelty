from django import template
from blog.models import News

register = template.Library()

@register.simple_tag()
def get_news():
    return News.objects.order_by("-date")[:3]
