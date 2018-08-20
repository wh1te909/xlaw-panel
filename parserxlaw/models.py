from django.db import models

class Usertrack(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)
    steamid = models.CharField(max_length=20)
    ip = models.CharField(max_length=20)
    connections = models.IntegerField()
    lastupdated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'usertrack'
