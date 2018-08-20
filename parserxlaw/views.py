from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
import validators
from steam import SteamID
from .models import Usertrack
from .functions import xmlGetInfo, xmlGetVac
from django.db.models import Q

@login_required
def parser(request):
    total = Usertrack.objects.using('Usertrack').count()
    if request.method == 'POST' and request.POST['query']:
        q = request.POST['query']
        if validators.url(q):
            try:
                steamid64 = SteamID.from_url(q)
                steamid2 = steamid64.as_steam2
            except AttributeError:
                error = "Please enter a valid steam url"
                return render(request, 'parserxlaw/parser.html', {'error':error})
        elif q.startswith("STEAM_") or q.isdigit():
            try:
                steamid64 = SteamID(q)
                steamid2 = steamid64.as_steam2
            except (TypeError, ValueError) as e:
                error = "Player not in database"
                return render(request, 'parserxlaw/parser.html', {'error':error})
        elif validators.ip_address.ipv4(q):
            results = Usertrack.objects.using('Usertrack').filter(ip = q).order_by('-lastupdated')

            if not results.exists():
                error = "IP address not in database"
                return render(request, 'parserxlaw/parser.html', {'error':error})
            else:
                icons = {}
                names = {}
                vacs = {}
                steamid_list = []

                for x in results:
                    steamid_list.append(x.steamid)

                steamid_list = set(steamid_list)

                for i in steamid_list:
                    icons[i] = xmlGetInfo(i, "avatarIcon")
                    names[i] = xmlGetInfo(i, "steamID")
                    vacs[i] = xmlGetVac(i)
                
                return render(request, 'parserxlaw/parser.html', {'results':results, 'icons':icons, 'names':names, 'vacs':vacs, 'q':q, 'total':total})

        else:
            error = """
            Invalid input. Enter a steamid, steam community link or IP address
            Some examples of valid input:
            http://steamcommunity.com/id/wh1te909/
            http://steamcommunity.com/profiles/76561198041802416
            72.19.25.123
            STEAM_1:0:12345678
            76561198041802416
            """
            return render(request, 'parserxlaw/parser.html', {'error':error})

        # get all the IP addresses for the steamid and put them in list
        # then grab all steamids for each ip to get alt accounts
        allips = Usertrack.objects.using('Usertrack').only('ip').filter(steamid = steamid2)
        if allips:
            ip_array = []
            for ip in allips:
                ip_array.append(ip.ip)

            # remove duplicates
            values = set(ip_array)

            queries = [Q(ip=value) for value in values]

            query = queries.pop()

            for item in queries:
                query |= item

            # if client is searching for alt accounts
            if request.POST['type'] == 'alt':
                results = Usertrack.objects.using('Usertrack').filter(query).order_by('-lastupdated')
            # if client is searching for just ip addresses
            elif request.POST['type'] == 'ipaddr':
                results = Usertrack.objects.using('Usertrack').filter(steamid = steamid2).order_by('-lastupdated')
            else:
                pass
        else:
            error = "Player not in database"
            return render(request, 'parserxlaw/parser.html', {'error':error})

        icons = {}
        names = {}
        vacs = {}
        steamid_list = []

        for x in results:
            steamid_list.append(x.steamid)

        steamid_list = set(steamid_list)

        for i in steamid_list:
            icons[i] = xmlGetInfo(i, "avatarIcon")
            names[i] = xmlGetInfo(i, "steamID")
            vacs[i] = xmlGetVac(i)

        return render(request, 'parserxlaw/parser.html', {'results':results, 'icons':icons, 'names':names, 'vacs':vacs, 'q':q, 'total':total})

    else:
        return render(request, 'parserxlaw/parser.html', {'total': total})