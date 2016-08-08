from django.db import models

import datetime


def year_choices():
    year_choices = [(r, r) for r in range(1984, datetime.date.today().year+1)]
    return year_choices


class PageDescription(models.Model):
    research = models.TextField()
    teaching = models.TextField()
    cluster = models.TextField()
    formation = models.TextField()


class Publication(models.Model):

    # [publications] Definindo os campos no banco de dados
    # para a tabela Publications
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=300)
    journal = models.CharField(max_length=500)
    year = models.IntegerField(
                choices=year_choices(),
                default=datetime.datetime.now().year)
    abstract = models.TextField()
    upload = models.FileField(upload_to='publications', max_length=100)
    download = models.IntegerField(default=0)

    # [publications] Ordenando a lista do post do mais recente ao mais antigo
    # Vá para: core/admin.py
    class Meta:
        ordering = ['-year', 'id']
