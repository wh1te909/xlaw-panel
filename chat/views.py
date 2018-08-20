from django.shortcuts import render
from .models import Chatlogs
from steam import SteamID
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
import validators

@login_required
def search(request):
    if request.method == 'POST' and request.POST['chatquery']:
        q = request.POST['chatquery']
        if validators.url(q):
            try:
                steamid64 = SteamID.from_url(q)
                steamid2 = steamid64.as_steam2
            except AttributeError:
                error = "Please enter a valid steam url"
                return render(request, 'chat/chat.html', {'error':error})
        elif q.startswith("STEAM_") or q.isdigit():
            try:
                steamid64 = SteamID(q)
                steamid2 = steamid64.as_steam2
            except (TypeError, ValueError) as e:
                error = "Player not in database"
                return render(request, 'chat/chat.html', {'error':error})
        else:
            error = """
            Invalid input. Enter a steamid or steam community link
            Some examples of valid input:
            http://steamcommunity.com/id/wh1te909/
            http://steamcommunity.com/profiles/76561198041802416
            STEAM_1:0:12345678
            76561198041802416
            """
            return render(request, 'chat/chat.html', {'error':error})

        results = Chatlogs.objects.using('Chatlogs').filter(steamid=steamid2).order_by('-date')

        if not results.exists():
            error = "Player not in database"
            return render(request, 'chat/chat.html', {'error':error})
        else:
            return render(request, 'chat/chat.html', {'results':results, 'steamid2':steamid2})
    else:
        return render(request, 'chat/chat.html')

    