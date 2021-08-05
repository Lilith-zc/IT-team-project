from django import template
from django import template
from rango.models import Author, Category

register = template.Library()

@register.inclusion_tag('rango/categories.html')
def get_category_list(current_category=None):
    return {'categories': Category.objects.all(),'current_category':current_category}

@register.inclusion_tag('rango/authors.html')
def get_author_list(current_author=None):
    return {'authors': Author.objects.all(), 'current_author': current_author}