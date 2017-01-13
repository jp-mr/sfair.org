from django import forms
from django.db import models
from django.utils.safestring import mark_safe

from markdown_deux import markdown
import datetime
#import magic


def year_choices():
    year_choices = [(r, r) for r in range(1984, datetime.date.today().year+1)]
    return year_choices


# def validate_file(value):
# 
#     supported_types = ['application/pdf',]
#     supported_files = ['PDF document',]
# 
#     mime_type = magic.from_file(value, mime=True)
#     if mime_type not in supported_types:
#         raise forms.ValidationError('Unsupported file type.')
# 
#     file_type = magic.from_file(value)
#     for s in supported_files:
#         if s not in file_type:
#             raise forms.ValidationError('Unsupported file type.')


class PageDescription(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()

    def __str__(self):
         return self.title

    def get_markdown(self):
        description = self.description
        markdown_text = markdown(description)
        return mark_safe(markdown_text)


class Publication(models.Model):

    # [publications] Definindo os campos no banco de dados
    # para a tabela Publications
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=1000)
    journal = models.CharField(max_length=500)
    year = models.IntegerField(
                choices=year_choices(),
                default=datetime.datetime.now().year)
    abstract = models.TextField()
    upload = models.FileField(
            #validators=[validate_file],
            upload_to='publications',
            max_length=300,
            blank=True
            )
    download = models.IntegerField(default=0)

    def __str__(self):
         return self.title

    def get_markdown(self):
        abstract = self.abstract
        markdown_text = markdown(abstract)
        return mark_safe(markdown_text)

    # [publications] Ordenando a lista do post do mais recente ao mais antigo
    # Vá para: core/admin.py
    class Meta:
        ordering = ['-year', 'id']
