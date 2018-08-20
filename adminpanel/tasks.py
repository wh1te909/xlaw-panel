import subprocess
from xlawpanel.celery import app

script = "/home/steam/xlawpanel/xlaw-panel/adminpanel/sync.sh"
scriptpw = "/home/steam/xlawpanel/xlaw-panel/adminpanel/copy-pw.sh"

@app.task
def pushAdmins():
    subprocess.call(script, shell=False)

@app.task
def pushHT():
    subprocess.call(scriptpw, shell=False)
