from django.db import models

class PlayerAnalytics(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)
    server_ip = models.CharField(max_length=32)
    name = models.CharField(max_length=32, blank=True, null=True)
    auth = models.CharField(max_length=32, blank=True, null=True)
    connect_time = models.IntegerField()
    connect_date = models.DateField()
    connect_method = models.CharField(max_length=64, blank=True, null=True)
    numplayers = models.IntegerField()
    map = models.CharField(max_length=64)
    duration = models.IntegerField(blank=True, null=True)
    flags = models.CharField(max_length=32)
    ip = models.CharField(max_length=32)
    city = models.CharField(max_length=45, blank=True, null=True)
    region = models.CharField(max_length=45, blank=True, null=True)
    country = models.CharField(max_length=45, blank=True, null=True)
    country_code = models.CharField(max_length=2, blank=True, null=True)
    country_code3 = models.CharField(max_length=3, blank=True, null=True)
    premium = models.IntegerField(blank=True, null=True)
    html_motd_disabled = models.IntegerField(blank=True, null=True)
    os = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'player_analytics'
