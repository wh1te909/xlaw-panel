from django.shortcuts import render
from django.db.models import Sum
from dashboard.models import PlayerAnalytics
from parserxlaw.models import Usertrack
from xml.parsers.expat import ExpatError
from django.contrib.auth.decorators import login_required
from steam import SteamID
import urllib.request
import xmltodict
import validators

@login_required
def stats(request):
    if request.method == 'POST' and request.POST['statsquery']:
        q = request.POST['statsquery']
        if validators.url(q):
            try:
                steamid64 = SteamID.from_url(q)
                steamid2 = steamid64.as_steam2
            except AttributeError:
                error = "Please enter a valid steam url"
                return render(request, 'stats/stats.html', {'error':error})
        elif q.startswith("STEAM_") or q.isdigit():
            try:
                steamid64 = SteamID(q)
                steamid2 = steamid64.as_steam2
            except (TypeError, ValueError) as e:
                error = "Player not in database"
                return render(request, 'stats/stats.html', {'error':error})
        else:
            error = """
            Invalid input. Enter a steamid or steam community link
            Some examples of valid input:
            http://steamcommunity.com/id/wh1te909/
            http://steamcommunity.com/profiles/76561198041802416
            STEAM_1:0:12345678
            76561198041802416
            """
            return render(request, 'stats/stats.html', {'error':error})

        results = PlayerAnalytics.objects.using('Analytics').filter(auth=steamid2)

        if not results.exists():
            error = "Player not in database"
            return render(request, 'stats/stats.html', {'error':error})
        else:
            try:
                file = urllib.request.urlopen("http://steamcommunity.com/profiles/{}/?xml=1".format(steamid64))
                data = file.read()
                file.close()
                data = xmltodict.parse(data)
                picture = data["profile"]["avatarIcon"]
                player_name = data["profile"]["steamID"]
            except ExpatError:
                error = "Player not in database"
                return render(request, 'stats/stats.html', {'error':error})
            
            playtime = int(PlayerAnalytics.objects.using('Analytics').filter(auth=steamid2).aggregate(Sum('duration'))['duration__sum'] / 3600)

            if playtime == 0:
                playtime = "< 1"

            country = PlayerAnalytics.objects.using('Analytics').only('country_code3').filter(auth=steamid2).last()
            city = PlayerAnalytics.objects.using('Analytics').only('city').filter(auth=steamid2).last()
            region = PlayerAnalytics.objects.using('Analytics').only('region').filter(auth=steamid2).last()
            steam_profile = "http://steamcommunity.com/profiles/{}".format(steamid64)

            connections = Usertrack.objects.using('Usertrack').filter(steamid=steamid2).aggregate(Sum('connections'))['connections__sum']

            top_server = PlayerAnalytics.objects.using('Analytics').raw(
                'select id, server_ip, count(*) as c from player_analytics where auth = %s group by server_ip order by c desc limit 1', [steamid2])
            
            top_map = PlayerAnalytics.objects.using('Analytics').raw(
                'select id, map, count(*) as d from player_analytics where auth = %s group by map order by d desc limit 1', [steamid2])
            
            flags = city = PlayerAnalytics.objects.using('Analytics').only('flags').filter(auth=steamid2).last()

            return render(request, 'stats/stats.html', {'playtime':playtime, 'steamid2':steamid2, 
                                                        'picture':picture, 'player_name':player_name, 'steam_profile':steam_profile,
                                                        'connections':connections, 'country':country, 'city':city, 'region':region,
                                                        'top_server':top_server, 'flags':flags, 'top_map':top_map})
            
    else:
        return render(request, 'stats/stats.html')