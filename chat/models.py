from django.db import models

class Chatlogs(models.Model):
    seqid = models.AutoField(primary_key=True)
    srvid = models.CharField(max_length=255)
    date = models.DateTimeField()
    name = models.CharField(max_length=64)
    steamid = models.CharField(max_length=32)
    text = models.CharField(max_length=192)
    team = models.IntegerField()
    type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'chatlogs'