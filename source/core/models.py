from django.db import models


class Publication(models.Model):

    # [publications] Definindo os campos no banco de dados
    # para a tabela Publications
    title = models.CharField(max_length=200)
    overview = models.TextField()
    upload = models.FileField(upload_to='publications', max_length=100)
    download = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    published = models.DateField(auto_now=False, auto_now_add=False)

    # [publications] Ordenando a lista do post do mais recente ao mais antigo
    # Vá para: core/admin.py
    class Meta:
        ordering = ["-published"]
