from datetime import date
from django import forms
from .models import Produto, Venda, Cliente
from django.forms.widgets import TextInput, NumberInput, Select, FileInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'telefone', 'endereco', 'meio_de_contato']
        widgets = {
            'nome': TextInput(attrs={'class': 'form-control'}),
            'telefone': TextInput(attrs={'class': 'form-control'}),
            'endereco': TextInput(attrs={'class': 'form-control'}),
            'meio_de_contato': Select(attrs={'class': 'custom-select col-12'}),
        }

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'foto',
            'nome', 
            'preco_riscado', 
            'preco',
            'descricao',
            'estoque', 
            'arquivado',
            #'cor', 
        ]
        widgets = {
            'estoque': Select(attrs={
                'class': 'custom-select col-12'
            }),
            'nome': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ovos...'
            }),
            'preco_riscado': NumberInput(attrs={
                'class': 'form-control',
                'value': '20.00'
            }),
            'preco': NumberInput(attrs={
                'class': 'form-control',
                'value': '17.00'
            }),
            'cor': TextInput(attrs={
                'class': 'form-control',
                'value': '#563d7c',
                'type': 'color'
            }),
            'foto': FileInput(attrs={'class': 'form-control-file form-control height-auto'}),
            'descricao': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ovos Caipira...'
            }),
        }

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = [
            #'vendedor',
            'cliente',
            'produto',
            'quantidade',
            'meio_de_pagamento',
            'desconto',
            #'data_pedido',
            'data_entrega',
        ]
        widgets = {
            'cliente': forms.Select(attrs={'class': 'custom-select col-12'}),
            'produto': forms.Select(attrs={'class': 'custom-select col-12'}),
            'quantidade': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'meio_de_pagamento': forms.Select(attrs={'class': 'custom-select col-12'}),
            'desconto': forms.Select(attrs={'class': 'custom-select col-12'}),
            
            'data_entrega': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and instance.data_entrega:
            self.initial['data_entrega'] = instance.data_entrega.strftime('%Y-%m-%d')
        if not self.instance.pk:  
            self.fields['data_entrega'].initial = date.today().isoformat()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
