from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
import re, random, fileinput, sys, subprocess, datetime, os
from shlex import quote
from steam import SteamID
from .models import Admin
from .tasks import pushAdmins, pushHT

def rand_file(length):
    chars = "abcdefghi453Efa6Hg924D"
    filename = ""
    while len(filename) != length:
        filename += random.choice(chars)
        if len(filename) == length:
            return filename

basedir = "/home/steam/xlawpanel/xlaw-panel"

file = "{}/adminpanel/admin_files/admins_simple.ini".format(basedir)
htpasswd_file = "{}/adminpanel/admin_files/.htpasswd".format(basedir)
passfile = "{}/adminpanel/admin_files/password-display/password_file.txt".format(basedir)
script = "{}/adminpanel/sync.sh".format(basedir)
scriptpw = "{}/adminpanel/copy-pw.sh".format(basedir)
sm_log_dir = "{}/adminpanel/admin_files/sm_logs".format(basedir)
temp_file = "{}/adminpanel/admin_files/sm_logs/".format(basedir) + rand_file(8)

def password_gen(length):
    chars = "ab@cdefghijklmn!opqrstuvwx$yzABCDEF#GHIJKL&MNOPQRSTUVWXYZ1234567890!@#$%&"
    password = ""
    while len(password) != length:
        password += random.choice(chars)
        if len(password) == length:
            return password

@login_required
def index(request):
    if not request.user.groups.filter(name='HeadAdmins').exists():
        raise PermissionDenied
    
    results = Admin.objects.all()
    return render(request, 'adminpanel/adminpanel.html', {'results':results})

@login_required
def addAdmin(request):
    if not request.user.groups.filter(name='HeadAdmins').exists():
        raise PermissionDenied

    results = Admin.objects.all()
    if request.method == 'POST':
        admin = quote(request.POST['steamid'])
        nickname =quote(request.POST['nickname'].replace(' ', ''))
        steamid = re.match(r'STEAM_([01]):([01]):(\d{1,11}$)', admin)
        name = nickname.isalnum()
        if steamid and name:
            steamid64 = SteamID(admin)
            steamid2 = steamid64.as_steam2
            # check if admin already exists and if not, add them
            if not Admin.objects.filter(steamid = steamid2).exists():
                try:
                    htname = nickname.lower()
                    hpasswd = password_gen(18)
                    subprocess.run('/usr/bin/htpasswd -b ' +htpasswd_file + ' ' + htname + ' ' + "'" + hpasswd + "'", shell=True, check=True)
                    print(htname + "\t\t" + hpasswd, file=open(passfile, "a"))
                except subprocess.CalledProcessError:
                    error = "ERROR: Something went wrong. Please contact wh1te909"
                    return render(request, 'adminpanel/adminpanel.html', {'error':error, 'results':results})
                else:
                    # add to database
                    a = Admin(name=nickname, steamid=steamid2, ht_name=htname, ht_passwd=hpasswd).save()
                    new_admin = Admin.objects.get(steamid=steamid2)
                    # add to admins_simple.ini
                    print('"{}" "{}:{}" // {}'.format(steamid2, new_admin.immunity, new_admin.flags, nickname.lower()), file=open(file, "a"))
                    # push the updated files to all servers via celery tasks
                    pushAdmins.delay()
                    pushHT.delay()
                    return render(request, 'adminpanel/adminpanel.html', {'success':"Admin added successfully!", 'results':results})
                
            else:
                return render(request, 'adminpanel/adminpanel.html', {'error':'ERROR: Admin already exists!', 'results':results})

        else:
            error = "ERROR: Enter a valid steamid AND nickname (alphanumeric characters only)"
            return render(request, 'adminpanel/adminpanel.html', {'error':error, 'results':results})

@login_required
def removeAdmin(request):
    if not request.user.groups.filter(name='HeadAdmins').exists():
        raise PermissionDenied
    
    results = Admin.objects.all()
    admin = request.POST['remove-steamid']
    nickname_remove = request.POST['remove-name']

    if admin == 'STEAM_1:0:40768344' or admin == 'STEAM_1:1:8948940' or admin == 'STEAM_1:0:908146':
        error = "ERROR: This person cannot be removed."
        return render(request, 'adminpanel/adminpanel.html', {'error':error, 'results':results})
    
    deleted_admin = Admin.objects.get(steamid=admin)
    
    try:
        # create backup of the file everytime an admin is removed
        date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        subprocess.run("/usr/bin/sed -i.{} /{}/d {}".format(date, admin, file), shell=True, check=True)
        subprocess.run("/usr/bin/sed -i.{} /{}/d {}".format(date, deleted_admin.ht_name, passfile), shell=True, check=True)
        # remove the admin's htpassword
        subprocess.run('/usr/bin/htpasswd -D ' +htpasswd_file + ' ' + deleted_admin.ht_name, shell=True, check=True)
        # push the updated files to all servers
        pushAdmins.delay()
        pushHT.delay()
    except subprocess.CalledProcessError:
        error = "ERROR: Something went wrong. Please contact wh1te909"
        return render(request, 'adminpanel/adminpanel.html', {'error':error, 'results':results})
    else:
        Admin.objects.filter(steamid=admin).delete()
        return render(request, 'adminpanel/adminpanel.html', {'success':"Admin removed!", 'results':results})

@login_required
def adminlogs(request, admin_id):
    if not request.user.groups.filter(name='HeadAdmins').exists():
        raise PermissionDenied
        
    results = Admin.objects.all()
    admin = get_object_or_404(Admin, pk=admin_id)
    grep = "/usr/bin/grep"
    # get end of steamid
    cut = admin.steamid.rsplit(':')[-1]
    try:
        subprocess.run("{} -h '{}' {}/*.log | {} -v slapped > {}".format(grep, cut, sm_log_dir, grep, temp_file), shell=True, check=True)
    except subprocess.CalledProcessError:
        os.remove(temp_file)
        error = "ERROR: no logs for this admin"
        return render(request, 'adminpanel/adminpanel.html', {'error':error, 'results':results})
    else:
        f = open(temp_file, "r", errors="ignore")
        text = f.read()
        f.close()
        os.remove(temp_file)
        return render(request, 'adminpanel/logs.html', {'admin':admin, 'text':text})