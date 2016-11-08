from django.contrib import admin
from django.contrib.admin.sites import AdminSite

from .forms import PageDescriptionForm, PublicationForm
from .models import Publication, PageDescription


AdminSite.site_header = "Sfair.org"
AdminSite.site_title = "Sfair.org"

admin.site.disable_action('delete_selected')


class PageDescriptionModelAdmin(admin.ModelAdmin):

    form = PageDescriptionForm

    # Não permite a adição de novos objetos no admin
    def has_add_permission(self, request):
        return True

    # Não permite a remoção de objetos no admin
    def has_delete_permission(self, request, obj=PageDescription):
        return False

    # list_display = ['title', 'pk']

    # class Meta:
    #     abstract = True


# class ResearchPageDescriptionModelAdmin(PageDescriptionModelAdmin):
# 
#     form = ResearchPageDescriptionForm
# 
#     # Não permite a remoção de objetos no admin
#     def has_delete_permission(self, request, obj=ResearchPageDescription):
#         return False
# 
# 
# class TeachingPageDescriptionModelAdmin(PageDescriptionModelAdmin):
# 
#     form = TeachingPageDescriptionForm
# 
#     # Não permite a remoção de objetos no admin
#     def has_delete_permission(self, request, obj=TeachingPageDescription):
#         return False
# 
# 
# class ClusterPageDescriptionModelAdmin(PageDescriptionModelAdmin):
# 
#     form = ClusterPageDescriptionForm
# 
#     # Não permite a remoção de objetos no admin
#     def has_delete_permission(self, request, obj=ClusterPageDescription):
#         return False
# 
# 
# class FormationPageDescriptionModelAdmin(PageDescriptionModelAdmin):
# 
#     form = FormationPageDescriptionForm
# 
#     # Não permite a remoção de objetos no admin
#     def has_delete_permission(self, request, obj=FormationPageDescription):
#         return False


class PublicationModelAdmin(admin.ModelAdmin):

    form = PublicationForm

    # [publications] Exibe os campos em colunas
    list_display = ['title', 'author', 'journal','year', 'download']

    # [publications] Não permite a edição dos campos
    readonly_fields = ['download', ]

    # [publications] Implementa um campo de filtro à esquerda da página
    list_filter = ['author', 'journal']

    # [publications] Implementa um campo de busca
    search_fields = ['title', 'author', 'journal', 'year', 'abstract']

    # [publications] Implementa a opção de exclusão
    actions = ['delete_selected']

    # class Meta:
    #     # [publications] Atribui a tabela Publication para ser exibido
    #     # na página de Administrador
    #     model = Publication


# [publications] Registra o modelo Publication
# Vá para: core/views.py
admin.site.register(Publication, PublicationModelAdmin)
admin.site.register(PageDescription, PageDescriptionModelAdmin)
# admin.site.register(ResearchPageDescription, ResearchPageDescriptionModelAdmin)
# admin.site.register(TeachingPageDescription, TeachingPageDescriptionModelAdmin)
# admin.site.register(ClusterPageDescription, ClusterPageDescriptionModelAdmin)
# admin.site.register(FormationPageDescription, FormationPageDescriptionModelAdmin)
