from django.db import models
from django.db.models import F
from datetime import date



class Cliente(models.Model):
    GENERO_CHOICES = (
        ('homem', 'Homem'),
        ('mulher', 'Mulher')
    )
    CONTATO_CHOICES = (
        ('whatsapp', 'WhatsApp'),
        ('instagram', 'Instagram')
    )

    nome = models.CharField(max_length=140, blank=True)
    telefone = models.CharField("Telefone:", max_length=12, blank=True)
    meio_de_contato = models.CharField("Meio de Contado:", max_length=20, choices=CONTATO_CHOICES, default=0)
    endereco = models.CharField(max_length=200, blank=True)
    genero = models.CharField("Gênero**:",choices=GENERO_CHOICES, max_length=10)
    idade_min = models.PositiveSmallIntegerField(blank=True, null=True)
    idade_max = models.PositiveSmallIntegerField(blank=True, null=True)
    interesses = models.CharField(max_length=200, blank=True, null=True)
    mapa = models.URLField(blank=True, default=None, null=True)

    def save(self, *args, **kwargs):
        if self.nome:
            self.nome = self.nome.title()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.nome:
            return self.nome
        return self.telefone


class Estoque(models.Model):
    nome = models.CharField(max_length=140)
    quantidade = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.nome


class Produto(models.Model):
    estoque = models.ForeignKey(Estoque, on_delete=models.CASCADE)
    nome = models.CharField(max_length=140, unique=True)
    preco = models.FloatField("Preço: ")
    preco_riscado = models.FloatField("Preço riscado R̶$̶2̶0̶: ")
    cor = models.CharField(max_length=6, blank=True, default=None)
    foto = models.ImageField(upload_to='media/produtos/', blank=True, default=None)
    descricao = models.CharField(max_length=200, blank=True, default=None)
    arquivado = models.BooleanField('Arquivado', default=False)

    def __str__(self):
        return self.nome

class Vendedor(models.Model):
    nome = models.CharField(max_length=140)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Vendedores"


class Desconto(models.Model):
    TIPO_CHOICES = (
        ('porcentagem', 'Porcentagem'),
        ('dinheiro', 'Dinheiro')
    )
    nome = models.CharField(max_length=100)
    tipo_desconto = models.CharField("Tipo do Desconto:", max_length=20, choices=TIPO_CHOICES)
    desconto = models.FloatField()

    def aplicar_desconto(self, valor):
        if self.tipo_desconto == 'porcentagem':
            return valor - (valor * (self.desconto / 100))
        elif self.tipo_desconto == 'dinheiro':
            return valor - self.desconto
        else:
            return valor

    def __str__(self):
        return self.nome

class Venda(models.Model):
    #vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, default=1)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, default=1)
    quantidade = models.PositiveSmallIntegerField()
    desconto = models.ForeignKey(Desconto, on_delete=models.CASCADE, blank=True, null=True, default=1)
    data_entrega = models.DateField(default=date.today)
    
    valor_total = models.FloatField('Valor da Venda', blank=True, null=True)
    desconto_aplicado = models.FloatField('Desconto Aplicado', blank=True, null=True)
    tem_desconto = models.BooleanField('Tem Desconto', default=False)

    MEIO_DE_PAGAMENTO_CHOICES = [
        ('pix', 'Pix'),
        ('dinheiro', 'Dinheiro'),
        ('cartão_crédito', 'Cartão de Crédito'),
        ('cartão_débito', 'Cartão de Dédito'),
    ]

    meio_de_pagamento = models.CharField(
        'Meio de Pagamento',
        max_length=20,
        choices=MEIO_DE_PAGAMENTO_CHOICES,
        default=0
    )


    @property
    def get_desconto(self):
        if self.tem_desconto == True:
            return f'-R${self.desconto_aplicado:0.2f}'
        return 'Sem Desconto'
    
    SEGUNDA_FEIRA = 'segunda'
    TERCA_FEIRA = 'terca'
    QUARTA_FEIRA = 'quarta'
    QUINTA_FEIRA = 'quinta'
    SEXTA_FEIRA = 'sexta'
    SABADO = 'sabado'
    DOMINGO = 'domingo'
    
    DIA_DA_SEMANA_CHOICES = [
        (SEGUNDA_FEIRA, 'Segunda'),
        (TERCA_FEIRA, 'Terça'),
        (QUARTA_FEIRA, 'Quarta'),
        (QUINTA_FEIRA, 'Quinta'),
        (SEXTA_FEIRA, 'Sexta'),
        (SABADO, 'Sábado'),
        (DOMINGO, 'Domingo'),
    ]

    dia_da_semana = models.CharField(
        'Dia da Semana',
        max_length=20,
        choices=DIA_DA_SEMANA_CHOICES,
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        if self.desconto:
            if self.desconto.tipo_desconto == 'porcentagem':
                self.desconto_aplicado = self.quantidade * (self.produto.preco * (self.desconto.desconto / 100))
                print(self.desconto_aplicado)
            elif self.desconto.tipo_desconto == 'dinheiro':
                self.desconto_aplicado = self.desconto.desconto
            self.tem_desconto = True
        else:
            self.desconto_aplicado = 0
            self.tem_desconto = False

        self.valor_total = (self.quantidade * self.produto.preco) - self.desconto_aplicado

        self.dia_da_semana = self.calcular_dia_da_semana()

        super().save(*args, **kwargs)

    def calcular_dia_da_semana(self):
        dias_da_semana = {
            0: self.SEGUNDA_FEIRA,
            1: self.TERCA_FEIRA,
            2: self.QUARTA_FEIRA,
            3: self.QUINTA_FEIRA,
            4: self.SEXTA_FEIRA,
            5: self.SABADO,
            6: self.DOMINGO,
        }
        return dias_da_semana[self.data_entrega.weekday()]

    def __str__(self):
        return f"{self.cliente.nome} - {self.produto.nome}"

    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'



