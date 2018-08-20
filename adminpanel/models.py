from django.db import models

class Admin(models.Model):
    name = models.CharField(max_length=50)
    steamid = models.CharField(max_length=50)
    flags = models.CharField(max_length=40, default="bcdfjgoe")
    immunity = models.IntegerField(default=1)
    ht_name = models.CharField(max_length=100)
    ht_passwd = models.CharField(max_length=100)
    kicks = models.IntegerField(default=0)
    bans = models.IntegerField(default=0)
    map_changes = models.IntegerField(default=0)
    sm_chats = models.IntegerField(default=0)
    sm_says = models.IntegerField(default=0)

    def __str__(self):
        return self.name