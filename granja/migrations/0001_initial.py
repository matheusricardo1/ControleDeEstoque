# Generated by Django 5.0.6 on 2024-05-16 16:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=140)),
                ('telefone', models.CharField(max_length=12, verbose_name='Telefone**:')),
                ('endereco', models.CharField(blank=True, max_length=200)),
                ('genero', models.CharField(choices=[('homem', 'Homem'), ('mulher', 'Mulher')], max_length=10, verbose_name='Gênero**:')),
                ('idade_min', models.PositiveSmallIntegerField(blank=True)),
                ('idade_max', models.PositiveSmallIntegerField(blank=True)),
                ('interesses', models.CharField(blank=True, max_length=200)),
                ('mapa', models.URLField(blank=True, default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Desconto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('tipo_desconto', models.CharField(choices=[('porcentagem', 'Porcentagem'), ('dinheiro', 'Dinheiro')], max_length=20, verbose_name='Tipo do Desconto:')),
                ('desconto', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Estoque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=140)),
                ('quantidade', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Vendedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=140)),
            ],
            options={
                'verbose_name_plural': 'Vendedores',
            },
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=140)),
                ('preco', models.FloatField(verbose_name='Preço: ')),
                ('cor', models.CharField(blank=True, default=None, max_length=6)),
                ('foto', models.ImageField(blank=True, default=None, upload_to='media/produtos/')),
                ('descricao', models.CharField(blank=True, default=None, max_length=200)),
                ('estoque', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='granja.estoque')),
            ],
        ),
        migrations.CreateModel(
            name='Venda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveSmallIntegerField()),
                ('data_pedido', models.DateField()),
                ('data_entrega', models.DateField()),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='granja.cliente')),
                ('desconto', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='granja.desconto')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='granja.produto')),
                ('vendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='granja.vendedor')),
            ],
        ),
    ]