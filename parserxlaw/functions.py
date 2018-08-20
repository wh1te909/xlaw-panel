import httplib2, xmltodict
from steam import SteamID

def xmlGetInfo(steamid, query):
    steamid64 = str(SteamID(steamid))
    try:
        h = httplib2.Http()
        resp, content = h.request("http://steamcommunity.com/profiles/{}/?xml=1".format(steamid64), "GET")
        data = xmltodict.parse(content)
        return data["profile"][query]
    except KeyError:
        return "-"

def xmlGetVac(steamid):
    steamid64 = str(SteamID(steamid))
    try:
        h = httplib2.Http()
        resp, content = h.request("http://steamcommunity.com/profiles/{}/?xml=1".format(steamid64), "GET")
        data = xmltodict.parse(content)
        return int(data["profile"]["vacBanned"])
    except KeyError:
        return "-"
