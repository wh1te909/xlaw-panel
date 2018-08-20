import subprocess
from secret_cron import *
from adminpanel.models import Admin

sm_log_dir = "/home/steam/xlawpanel/xlaw-panel/adminpanel/admin_files/sm_logs"
results = Admin.objects.all()

grep = "/usr/bin/grep"

if __name__ == '__main__':
    for admin in results:
        # get end of steamid
        cut = admin.steamid.rsplit(':')[-1]

        kicks = subprocess.Popen("{} '{}' {}/*.log | {} 'basecommands.smx' | {} 'kicked' | {} 'reason' | wc -l".format(
            grep, cut, sm_log_dir, grep, grep, grep),
            stdout=subprocess.PIPE, shell=True).communicate()[0].decode("utf-8")

        bans = subprocess.Popen("{} '{}' {}/*.log | {} 'sbpp_main.smx' | {} 'banned' | {} 'reason' | wc -l".format(
            grep, cut, sm_log_dir, grep, grep, grep),
            stdout=subprocess.PIPE, shell=True).communicate()[0].decode("utf-8")
        
        map_change = subprocess.Popen("{} '{}' {}/*.log | {} 'basecommands.smx' | {} 'changed map to' | wc -l".format(
            grep, cut, sm_log_dir, grep, grep),
            stdout=subprocess.PIPE, shell=True).communicate()[0].decode("utf-8")
        
        sm_chat = subprocess.Popen("{} '{}' {}/*.log | {} 'basechat.smx' | {} 'triggered sm_chat' | wc -l".format(
            grep, cut, sm_log_dir, grep, grep),
            stdout=subprocess.PIPE, shell=True).communicate()[0].decode("utf-8")
        
        sm_say = subprocess.Popen("{} '{}' {}/*.log | {} 'basechat.smx' | {} 'triggered sm_say' | wc -l".format(
            grep, cut, sm_log_dir, grep, grep),
            stdout=subprocess.PIPE, shell=True).communicate()[0].decode("utf-8")
        
        admin.kicks = int(kicks)
        admin.bans = int(bans)
        admin.map_changes = int(map_change)
        admin.sm_chats = int(sm_chat)
        admin.sm_says = int(sm_say)
        admin.save()