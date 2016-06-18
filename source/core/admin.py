from django.contrib import admin

from .models import Publication


class PublicationModelAdmin(admin.ModelAdmin):

    # exibe os campos em colunas
    list_display = ['title', 'updated', 'timestamp','published', 'counter']

    # implementa um campo de filtro à esquerda da página
    list_filter = ['title']

    # implementa um campo de busca
    search_fields = ['title', 'overview']

    class Meta:
        model = Publication


admin.site.register(Publication, PublicationModelAdmin)
