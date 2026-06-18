from django.db import models

class Member(models.Model):
    gaijin_id = models.CharField(primary_key=True, max_length=100, db_column='gaijin_id')
    name = models.CharField(max_length=255, db_column='name')
    state = models.CharField(max_length=1, db_column='state', default='N')
    join_date = models.CharField(max_length=20, db_column='join_date')   # 文本日期，建议保持字符串
    landforce = models.CharField(max_length=20, db_column='landforce', default='Uncertified')
    airforce = models.CharField(max_length=20, db_column='airforce', default='Uncertified')
    navy = models.CharField(max_length=20, db_column='navy', default='Uncertified')

    class Meta:
        db_table = 'members'
        managed = False   # 防止 Django 迁移改动已有表