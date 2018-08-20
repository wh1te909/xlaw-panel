import urllib.request
from steam import SteamID
import xmltodict

def xmlGetInfo(steamid64, query):
    try:
        file = urllib.request.urlopen("http://steamcommunity.com/profiles/{}/?xml=1".format(steamid64))
        data = file.read()
        file.close()
        data = xmltodict.parse(data)
        return data["profile"][query]
    except KeyError:
        return "-"