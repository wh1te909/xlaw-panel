from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework import status
from django.db.models import Sum, Count
from parserxlaw.models import Usertrack
from dashboard.models import PlayerAnalytics
from chat.models import Chatlogs
from steam import SteamID
from collections import defaultdict
import urllib.request
import xmltodict

def player_name(steamid64):
    try:
        file = urllib.request.urlopen("http://steamcommunity.com/profiles/{}/?xml=1".format(steamid64))
        data = file.read()
        file.close()
        data = xmltodict.parse(data)
        return data["profile"]["steamID"]
    except ExpatError:
        return "N/A"

class TwentyPerMin(UserRateThrottle):
        rate = '20/min'

class TwoPerMin(UserRateThrottle):
        rate = '2/min'

@api_view()
def uniquePlayers(request):
    unique = Usertrack.objects.using('Usertrack').count()
    return Response({"uniquePlayers":(format(unique, ',d'))})

@api_view()
def totalHours(request):
    totalhours = int(PlayerAnalytics.objects.using('Analytics').aggregate(Sum('duration'))['duration__sum'] / 3600)
    return Response({"totalHoursPlayed":(format(totalhours, ',d'))})

@api_view()
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
@throttle_classes([TwentyPerMin])
def playerStats(request, steamid):
    if steamid.startswith("STEAM_") or steamid.isdigit():
        try:
            steamid64 = SteamID(steamid)
            steamid2 = steamid64.as_steam2
        except TypeError:
            content = {'error': 'Please enter a valid steamid or steamid64'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                connections = Usertrack.objects.using('Usertrack').filter(steamid=steamid2).aggregate(Sum('connections'))['connections__sum']
                if not connections:
                    content = {'error': 'Player not in database'}
                    return Response(content, status=status.HTTP_404_NOT_FOUND)
            except TypeError:
                content = {'error': 'Player not in database'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
            else:
                try:
                    country = PlayerAnalytics.objects.using('Analytics').only('country_code3').filter(auth=steamid2).last().country_code3
                    hours = int(PlayerAnalytics.objects.using('Analytics').filter(auth=steamid2).aggregate(Sum('duration'))['duration__sum'] / 3600)
                except AttributeError:
                    country = "N/A"
                    hours = "N/A"
                name = player_name(steamid64)
                
                return Response(
                    {
                    "stats":{   
                        "name":name,
                        "steamID":steamid2,
                        "steamID64": steamid64,
                        "totalHours": hours,
                        "connections":connections,
                        "country":country}})
    else:
        content = {'error': 'Please enter a valid steamid or steamid64'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)

@api_view()
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
@throttle_classes([TwoPerMin])
def chatHistory(request, steamid):
    if steamid.startswith("STEAM_") or steamid.isdigit():
        try:
            steamid64 = SteamID(steamid)
            steamid2 = steamid64.as_steam2
        except (TypeError, ValueError) as e:
            content = {'error': 'Please enter a valid steamid or steamid64'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                chats = Chatlogs.objects.using('Chatlogs').filter(steamid=steamid2).order_by('-date')
                if not chats:
                    content = {'error': 'Player not in database'}
                    return Response(content, status=status.HTTP_404_NOT_FOUND)
            except TypeError:
                content = {'error': 'Please enter a valid steamid or steamid64'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
            else:
                chat = []
                for x in chats:
                    chat.append(x.text)
                return Response({"chatHistory":chat})
    else:
        content = {'error': 'Please enter a valid steamid or steamid64'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)

@api_view()
def topServer(request):
    top_server = PlayerAnalytics.objects.using('Analytics').values('server_ip').annotate(Count('server_ip')).order_by('-server_ip__count')[:1].get()
    return Response({"topServer":top_server['server_ip']})

@api_view()
def topMap(request):
    top_map = PlayerAnalytics.objects.using('Analytics').values('map').annotate(Count('map')).order_by('-map__count')[:1].get()
    return Response({"topMap":top_map['map']})

@api_view()
def topTen(request):
    sql = "SELECT id, auth, SUM(duration) duration FROM player_analytics GROUP BY auth ORDER BY duration DESC LIMIT 10"
    top_players = PlayerAnalytics.objects.using('Analytics').raw(sql)
    top_ten = defaultdict(dict)
    i = 0
    for x in top_players:
        i += 1
        steamid64 = SteamID(x.auth)
        steamid2 = steamid64.as_steam2
        top_ten[i]['hours'] = int(PlayerAnalytics.objects.using('Analytics').filter(auth=steamid2).aggregate(Sum('duration'))['duration__sum'] / 3600)
        top_ten[i]['profile'] = "http://steamcommunity.com/profiles/{}".format(steamid64)
        top_ten[i]['steamid2'] = steamid2

        file = urllib.request.urlopen("http://steamcommunity.com/profiles/{}/?xml=1".format(steamid64))
        data = file.read()
        file.close()
        data = xmltodict.parse(data)

        top_ten[i]['picture'] = data["profile"]["avatarIcon"]
        top_ten[i]['name'] = data["profile"]["steamID"]
    
    return Response({'topten':top_ten})