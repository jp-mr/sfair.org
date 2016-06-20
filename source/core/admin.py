from django.contrib import admin

from .models import Publication


class PublicationModelAdmin(admin.ModelAdmin):

    # [publications] Exibe os campos em colunas
    list_display = ['title', 'updated', 'timestamp', 'published', 'counter']

    # [publications] Implementa um campo de filtro à esquerda da página
    list_filter = ['title']

    # [publications] Implementa um campo de busca
    search_fields = ['title', 'overview']

    class Meta:
        # [publications] Atribui a tabela Publication para ser exibido
        # na página de Administrador
        model = Publication

# [publications] Registra o modelo Publication
# Vá para: core/views.py
admin.site.register(Publication, PublicationModelAdmin)
