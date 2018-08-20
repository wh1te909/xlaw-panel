from django import template

register = template.Library()

@register.filter
def get_server(server):
    if str(server) == 'dallasserver1':
        return "Dallas #1"
    elif str(server) == 'dallasserver2':
        return "Dallas #2"
    elif str(server) == 'xlawserver1':
        return "Xlaw #1"
    elif str(server) == 'xlawserver2':
        return "Xlaw #2"
    elif str(server) == 'xeastserver1':
        return "Xlaw #3"
    elif str(server) == 'xeastserver2':
        return "Xlaw #4"
    elif str(server) == 'xchiserver1':
        return "Xlaw #5"
    elif str(server) == 'xchiserver2':
        return "Xlaw #6"
    elif str(server) == 'xatlaserver1':
        return "Xlaw #7"
    elif str(server) == 'xatlaserver2':
        return "Xlaw #8"
    elif str(server) == 'xatlaserver3':
        return "Xlaw #9"
    elif str(server) == 'xatlaserver4':
        return "Xlaw #10"
    elif str(server) == 'xnewserver1':
        return "Xlaw #11"
    elif str(server) == 'xnewserver2':
        return "Xlaw #12"
    elif str(server) == 'xnewserver3':
        return "Xlaw #13"
    elif str(server) == 'xnewserver4':
        return "Xlaw #14"
    elif str(server) == 'xfrankserver1':
        return "Xlaw #15"
    elif str(server) == 'xfrankserver2':
        return "Xlaw #16"
    elif str(server) == 'xlatwoserver1':
        return "Xlaw #17"
    elif str(server) == 'xlatwoserver2':
        return "Xlaw #18"
    elif str(server) == 'xfranktwoserver1':
        return "Xlaw #19"
    elif str(server) == 'xfranktwoserver2':
        return "Xlaw #20"
    elif str(server) == 'xpistolserver1':
        return "Xlaw #21"
    elif str(server) == 'xpistolserver2':
        return "Xlaw #22"
    else:
        return "n/a"


