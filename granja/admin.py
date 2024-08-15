from django.contrib import admin
from django.utils.translation import gettext as _

from .models import (
    Cliente,
    Estoque,
    Produto,
    Venda,
    Vendedor,
    Desconto,
    AppUser,
    Empresa
)

admin.site.register(Cliente)
admin.site.register(Estoque)
admin.site.register(Vendedor)
admin.site.register(Desconto)
admin.site.register(AppUser)
admin.site.register(Empresa)

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao', 'preco_valor', 'estoque_dinamico']

    def preco_valor(self, obj):
        return f'R${obj.preco:0.2f}'
    preco_valor.short_description = 'Preço' 

    def estoque_dinamico(self, obj):
        return f'{obj.estoque.quantidade} Itens'
    estoque_dinamico.short_description = 'Estoque' 

admin.site.register(Produto, ProdutoAdmin)


class VendaAdmin(admin.ModelAdmin):
    fields = (
        #'vendedor',
         'cliente', 'produto', 'quantidade', 'desconto', 'data_entrega')
    required_fields = [
        #'vendedor', 
        'cliente', 'produto', 'quantidade' , 'data_entrega']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'produto':
            # Obtém o ID do produto selecionado na tela de criação
            produto_id = request.GET.get('produto', None)
            if produto_id:
                # Obtém o preço do produto e define o valor do campo preco_produto
                produto = Produto.objects.get(pk=produto_id)
                kwargs['initial'] = {'quantidade': produto.estoque.quantidade}
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        if obj is not None and obj.desconto_id is None and 'desconto' in self.required_fields:
            self.required_fields.remove('desconto')
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['desconto'].required = 'desconto' in self.required_fields
        return form

    list_display = [
        #'vendedor', 
        'cliente', 
        'quantidade', 
        'valor_venda', 
        'deconto', 
        'dia_da_semana',
        'data_entrega'
        ]

    def deconto(self, obj):
        if obj.desconto:
            return f'-R${obj.desconto_aplicado:0.2f}'
        return 'Sem Desconto'
    deconto.short_description = 'Desconto' 

    def valor_venda(self, obj):
        if obj.valor_total:
            return f'R${obj.valor_total:0.2f}'
        return f'Salve novamente'
    valor_venda.short_description = 'Valor da Venda' 

admin.site.register(Venda, VendaAdmin)
