from django.db import models


class Member(models.Model):
    gaijin_id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=1)
    join_date = models.CharField(max_length=64)
    landforce = models.CharField(max_length=32)
    airforce = models.CharField(max_length=32)
    navy = models.CharField(max_length=32)

    class Meta:
        db_table = 'members'
        managed = False

    def __str__(self):
        return f"{self.name} ({self.gaijin_id})"
