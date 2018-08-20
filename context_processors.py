from django.contrib.auth.models import User

def totalusers(request):
    try:
        request.user.username
    except AttributeError:
        return {}
    else:
        return {'name': request.user.username}