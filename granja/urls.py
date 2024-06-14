from django.urls import path
from granja import views

app_name = 'granja'

urlpatterns = [
    path('', views.vendas, name='index'), 
    path('dashboard/', views.dashboard, name='dashboard'), 
]

urlpatterns += [
    path('produtos/', views.produtos, name='produtos'),
    path('produto/criar/', views.criar_produto, name='criar_produto'),
    path('produto/<int:id>/editar/', views.editar_produto, name='editar_produto'),
    path('produto/<int:id>/excluir/', views.excluir_produto, name='excluir_produto'),  
]

urlpatterns += [
    path('vendas/', views.vendas, name='vendas'),
    path('venda/criar/', views.gerar_venda, name='gerar_venda'),
    path('venda/<int:id>/editar/', views.editar_venda, name='editar_venda'),
    path('venda/<int:id>/excluir/', views.excluir_venda, name='excluir_venda'),
    path('excluir/<str:model>/<int:pk>/', views.excluir, name='excluir'),  
]
