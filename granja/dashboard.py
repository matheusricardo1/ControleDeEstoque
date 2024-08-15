# dashboard.py
from datetime import datetime, timedelta
from django.db.models import Sum
from .models import Venda

class Dashboard:
    mensagem = ""
    total_clientes = 0
    total_formas = 0
    total_valor = 0

    total_clientes_semana_passada = 0
    total_formas_semana_passada = 0
    total_valor_semana_passada = 0

    totais_semana_atual = {dia: 0 for dia, _ in Venda.DIA_DA_SEMANA_CHOICES}
    totais_semana_passada = {dia: 0 for dia, _ in Venda.DIA_DA_SEMANA_CHOICES}

    semana_atual = []
    semana_passada = []

    def limpar_quantidade(self):
        self.totais_semana_atual = {dia: 0 for dia, _ in Venda.DIA_DA_SEMANA_CHOICES}
        self.totais_semana_passada = {dia: 0 for dia, _ in Venda.DIA_DA_SEMANA_CHOICES}

    def get_week(self, data):
        inicio_semana = data - timedelta(days=data.weekday())
        fim_semana = inicio_semana + timedelta(days=6)
        return inicio_semana, fim_semana

    def config(self, today):
        self.hoje = today
        self.inicio_semana_atual, self.fim_semana_atual = self.get_week(self.hoje)
        semana_passada = self.hoje - timedelta(days=7)
        self.inicio_semana_passada, self.fim_semana_passada = self.get_week(semana_passada)

    def __init__(self, today=datetime.today()):

        self.config(today)
        self.limpar_quantidade()
        
        self.vendas_semana_atual = Venda.objects.filter(data_entrega__range=[self.inicio_semana_atual, self.fim_semana_atual]).order_by('data_entrega')
        self.semana_atual = []
        for venda in self.vendas_semana_atual:
            dia = venda.calcular_dia_da_semana()
            self.totais_semana_atual[dia] += venda.quantidade
            self.semana_atual.append(venda)
        
        self.vendas_semana_passada = Venda.objects.filter(data_entrega__range=[self.inicio_semana_passada, self.fim_semana_passada]).order_by('data_entrega')
        self.semana_passada = []

        for venda in self.vendas_semana_passada:
            dia = venda.calcular_dia_da_semana()
            self.totais_semana_passada[dia] += venda.quantidade
            self.semana_passada.append(venda)
            self.total_clientes_semana_passada += 1 
            self.total_formas_semana_passada += venda.quantidade
            self.total_valor_semana_passada += venda.valor_total

        #print(self.totais_semana_passada)
        self.computar_vendas()

    def calcular_tamanho_grafico(self):
        maior_quantidade_atual = max(self.totais_semana_atual.values(), default=0)
        maior_quantidade_passada = max(self.totais_semana_passada.values(), default=0)
        tamanho_grafico = max(maior_quantidade_atual, maior_quantidade_passada)
        if tamanho_grafico % 2 == 0:
            return tamanho_grafico + 4
        if tamanho_grafico % 2 != 0:
            return tamanho_grafico + 3
        
    def computar_vendas(self):
        mensagem = ""
        total_clientes = 0
        total_formas = 0
        total_valor = 0

        dias_da_semana = {dia[0]: dia[1] for dia in Venda.DIA_DA_SEMANA_CHOICES}
        vendas_por_dia = {
            
        }

        for venda in self.vendas_semana_atual:
            dia = venda.calcular_dia_da_semana()
            dia_mes = venda.data_entrega.strftime("%d/%m")
            vendas = self.vendas_semana_atual.filter(dia_da_semana=dia)
            vendas_por_dia[dia, dia_mes] = vendas

        vendas_semana_atual = {dia[0]: [] for dia in Venda.DIA_DA_SEMANA_CHOICES}

        vendas = {}

        for dia, venda in vendas_por_dia.items():
            #print(f'\n{dia[0].title()} - {dia[1]}')
            mensagem += f'\n*{dia[0].title()} {dia[1]}*'
            if venda:
                for venda in venda:
                    nome = venda.cliente.nome
                    quantidade = venda.quantidade
                    valor = f'R${venda.valor_total:.0f},00'

                    total_clientes += 1
                    total_formas += venda.quantidade
                    total_valor += venda.valor_total

                    #print(nome, quantidade, valor)
                    mensagem += f'\n{nome}   {quantidade}   {valor}'
            mensagem += '\n'

        #print(vendas_por_dia[''])

        mensagem += f'\n*Resultados da Semana {self.inicio_semana_atual.strftime("%d/%m")} - {self.hoje.strftime("%d/%m")}*\n'
        mensagem += f'*{ total_clientes } Clientes*\n'
        mensagem += f'*{ total_formas } Fôrmas*\n'
        mensagem += f'*R${total_valor:0.0f},00*'

        self.mensagem = mensagem
        self.total_clientes = total_clientes
        self.total_formas = total_formas
        self.total_valor = total_valor
