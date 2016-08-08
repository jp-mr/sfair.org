from django.contrib import admin
from django.contrib.admin.sites import AdminSite

from .models import Publication, PageDescription


AdminSite.site_header = "Sfair.org"
AdminSite.site_title = "Sfair.org"

class PageDescriptionModelAdmin(admin.ModelAdmin):
    class Meta:
        model = PageDescription


class PublicationModelAdmin(admin.ModelAdmin):

    # [publications] Exibe os campos em colunas
    list_display = ['title', 'author', 'journal','year', 'download']

    # [publications] Não permite a edição dos campos
    readonly_fields = ['download', ]

    # [publications] Implementa um campo de filtro à esquerda da página
    list_filter = ['author', 'journal']

    # [publications] Implementa um campo de busca
    search_fields = ['title', 'author', 'journal', 'year', 'abstract']

    class Meta:
        # [publications] Atribui a tabela Publication para ser exibido
        # na página de Administrador
        model = Publication


# [publications] Registra o modelo Publication
# Vá para: core/views.py
admin.site.register(Publication, PublicationModelAdmin)
admin.site.register(PageDescription, PageDescriptionModelAdmin)
