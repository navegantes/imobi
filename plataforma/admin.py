from django.contrib import admin
from .models import DiasVisita, Cidade, Imagem, Horario, Imovel, Visitas

# Personalização da area admin


@admin.register(Imovel)
class ImovelAdmin(admin.ModelAdmin):
    list_display = ('rua', 'valor', 'quartos', 'tamanho', 'cidade', 'tipo')
    list_editable = ('valor', 'quartos', 'tamanho', 'cidade', 'tipo')
    list_filter = ('cidade', 'tipo')


admin.site.register(DiasVisita)
admin.site.register(Cidade)
admin.site.register(Imagem)
admin.site.register(Horario)
# admin.site.register(Imovel)
admin.site.register(Visitas)
