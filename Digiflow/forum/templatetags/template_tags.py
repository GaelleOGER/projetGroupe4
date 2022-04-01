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


@register.simple_tag
def comparator_profile(user, friend):
    lister = user.userprofile.friendlist.all()
    print(lister)
    for each in lister:
        if friend.user == each.friend:
            if each.is_accepted:
                return mark_safe(f'<a href="/forum/remove-friend/{each.pk}" class="btn btn-danger"> Supprimer amis</a>')
            else:
                return mark_safe(f'<button class="btn btn-info"> en attente </button>')


    return mark_safe(f'<a href="/forum/add-friend/{friend.user.userprofile.pk}" class="btn btn-success"> Ajouter amis</a>')