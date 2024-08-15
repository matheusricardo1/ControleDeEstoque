from django.shortcuts import render, redirect, get_object_or_404
from granja.models import Venda, Produto, Estoque, Cliente, Vendedor, AppUser
from granja.forms import ProdutoForm, VendaForm, ClienteForm, UserRegisterForm
from .dashboard import Dashboard
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm


def index(request):
    return render(request, 'granja/pages/vendas.html', {
        'vendas': Venda.objects.all(),
    })


def dashboard(request):
    today = datetime.today()
    option = None

    if request.method == "GET":
        date_str = request.GET.get('date')
        option = request.GET.get('option')

        if date_str:
            today = datetime.strptime(date_str, '%d-%m-%Y')

    if option == '1':
        dashboard_obj = Dashboard(today)
    elif option == '2':
        last_week = today - timedelta(days=7)
        dashboard_obj = Dashboard(last_week)
    else:
        dashboard_obj = Dashboard(today)

    #today = datetime(2024, 6, 23)
    dashboard = Dashboard(today)

    semana_passada = dashboard.totais_semana_passada
    semana_atual = dashboard.totais_semana_atual
    tamanho_grafico = dashboard.calcular_tamanho_grafico()
    messagem_whatsapp =  dashboard.mensagem

    clientes = dashboard.total_clientes
    lucro = dashboard.total_valor
    formas = dashboard.total_formas
    clientes_semana_passada = dashboard.total_clientes_semana_passada
    lucro_semana_passada = dashboard.total_valor_semana_passada
    formas_semana_passada = dashboard.total_formas_semana_passada

    diferenca_lucro = abs(dashboard.total_valor - dashboard.total_valor_semana_passada)
    porcentagem_aumento = 0

    if lucro == 0 or lucro_semana_passada == 0:
        porcentagem_aumento = 0
    else:
        porcentagem_aumento = (diferenca_lucro / min(lucro_semana_passada, lucro)) * 100


    return render(request, 'granja/pages/dashboard.html', {
        'option': option,
        'clientes': clientes,
        'lucro': lucro,
        'formas': formas,

        'clientes_semana_passada': clientes_semana_passada,
        'lucro_semana_passada': lucro_semana_passada,
        'formas_semana_passada': formas_semana_passada,
        'diferenca_lucro': diferenca_lucro,

        'porcentagem_aumento': porcentagem_aumento,

        'messagem_whatsapp': messagem_whatsapp,

        'semana_atual': semana_atual,
        'semana_passada': semana_passada,
        'tamanho_grafico': tamanho_grafico,

        'DIA_DA_SEMANA_CHOICES': Venda.DIA_DA_SEMANA_CHOICES,
    })


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        data = request.POST
        if form.is_valid():
            role = data.get('role', None)
            user = form.save(commit=False) 
            user.save()
            AppUser.objects.create(user=user, user_type=role)
            #print(form.cleaned_data, data, role)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada para {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'granja/auth/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Usuário ou senha inválidos')
        else:
            messages.error(request, 'Usuário ou senha inválidos')
    else:
        form = AuthenticationForm()
    return render(request, 'granja/auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(dashboard)


def empresa(request, arroba):
    return render(request, 'granja/auth/auth.html')




def produtos(request):
    produtos = Produto.objects.all()

    return render(request, 'granja/pages/products.html', {
        'produtos': produtos,
        'sub_title': 'Produtos'
    })


def criar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('granja:index')
    else:
        form = ProdutoForm()

    form.fields['estoque'].queryset = Estoque.objects.all()  
    return render(request, 'granja/pages/admin_form.html', {
        'form': form,
        'sub_title': 'Criar Produto'
        })


def editar_produto(request, id):
    obj = Produto
    editar = [True, obj.__name__.lower(), id]
    produto = get_object_or_404(obj, pk=id)
    

    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('granja:produtos') 
    else:
        form = ProdutoForm(instance=produto)

    return render(request, 'granja/pages/admin_form.html', {
        'form': form,
        'produto': produto,
        'editar': editar,
        'sub_title': 'Editar Produto'
    })


def excluir_produto(request, id):
    try:
        Produto.objects.get(id=id).delete()
    except Exception as e:
        print("Error!")
    return redirect('granja:produtos')


def vendas(request):
    vendas = Venda.objects.all().order_by('-data_entrega')[:20]

    return render(request, 'granja/pages/vendas.html', {
        'vendas': vendas,
        'sub_title': 'Vendas'
    })


def gerar_venda(request):
    if request.method == 'POST':
        form = VendaForm(request.POST, request.FILES)
        form2 = ClienteForm(request.POST, request.FILES)
        if form2.is_valid():
            cliente = form2.cleaned_data
            cliente['nome'] = cliente['nome'].title()
        
            obj = None
            meio_de_contato = cliente['meio_de_contato']            
            list_filter = {
                '1': Cliente.objects.check(nome=cliente['nome'], telefone=cliente['telefone'], meio_de_contato=meio_de_contato),
                '2': Cliente.objects.check(telefone=cliente['telefone'], meio_de_contato=meio_de_contato),
                '3': Cliente.objects.check(nome=cliente['nome'], meio_de_contato=meio_de_contato),
            }

            cliente_id = None
            for key, value in list_filter.items():
                if value:
                    cliente_id = value.id
                    break

            if cliente_id:
                obj = Cliente.objects.get(id=cliente_id)
            else:
                obj = Cliente.objects.create(**cliente)

            if not obj.nome and cliente.get('nome', None) is not None:
                obj.nome = cliente['nome']
            if not obj.nome and cliente.get('nome', None) is not None:
                obj.nome = cliente['nome']
            if not obj.endereco and cliente.get('endereco', None) is not None:
                obj.endereco = cliente['endereco']
            obj.save()

            if form.is_valid():
                venda = form.save(commit=False)
                venda.cliente = obj
                venda.save()
                return redirect('granja:index')        
    else:
        form = VendaForm()
        form2 = ClienteForm()

    #form.fields['cliente'].queryset = Cliente.objects.all()
    form.fields['produto'].queryset = Produto.objects.all()

    return render(request, 'granja/pages/admin_form.html', {
        'form': form,
        'form2': form2,
        'sub_title': 'Gerar Venda'
    })


def editar_venda(request, id):
    obj = Venda
    editar = [True, obj.__name__.lower(), id]
    venda = get_object_or_404(obj, pk=id)

    if request.method == 'POST':
        form = VendaForm(request.POST, request.FILES, instance=venda)
        if form.is_valid():
            form.save()
            return redirect('granja:vendas') 
    else:
        form = VendaForm(instance=venda)

    return render(request, 'granja/pages/admin_form.html', {
        'form': form,
        'venda': venda,
        'editar': editar,
        'sub_title': 'Editar Venda'
    })


def excluir_venda(request, id):
    try:
        Venda.objects.get(id=id).delete()
    except Exception as e:
        print("Error!")
    return redirect('granja:produtos')


def excluir(request, model, pk):
    url_anterior = request.META.get('HTTP_REFERER', '/')
    model_class = {
        'venda': Venda,
        'produto': Produto,
        'cliente': Cliente,
    }.get(model)

    if model_class is None:
        return redirect(url_anterior)

    objeto = get_object_or_404(model_class, pk=pk)
    
    objeto.delete()
    return redirect('granja:index')