from django.db import models


class Publication(models.Model):
    
    # TODO: Adicionar um campo para a data da publicação do paper.
    # Procurar no projeto trydjango19
    
    title = models.CharField(max_length=200)
    overview = models.TextField()
    upload = models.FileField(upload_to='publications', max_length=100)
    counter = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
