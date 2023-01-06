from django.db import models

class Wcapi(models.Model):
    user_id = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    time_create = models.DateTimeField(auto_now_add=True)
    is_parser = models.BooleanField(default=True)
    is_online = models.BooleanField(default=False)
    last_online = models.CharField(max_length=255,default='off')

    def __str__(self):
        return self.number