from django import template
from steam import SteamID
from django.contrib.auth.models import Group 

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.simple_tag
def convert_64(steamid):
    return str(SteamID(steamid))

@register.filter(name='has_group') 
def has_group(user, group_name):
    group =  Group.objects.get(name=group_name) 
    return group in user.groups.all() 
