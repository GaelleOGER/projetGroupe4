from django.contrib.auth.models import Group
from django import template


register = template.Library()


@register.simple_tag
def is_group(user, group_name):
    group = Group.objects.get(name=group_name)
    if group in user.groups.all():
        return True
    return False


@register.filter(name='is_group_filter')
def is_group_filter(user, group_name):
    group = Group.objects.get(name=group_name)
    return group in user.groups.all()