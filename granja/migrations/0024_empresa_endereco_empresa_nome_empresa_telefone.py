# Generated by Django 5.0.6 on 2024-06-25 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('granja', '0023_gasto_alter_cliente_meio_de_contato_appuser_empresa'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='endereco',
            field=models.TextField(default='Rua tapajos 388'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='empresa',
            name='nome',
            field=models.CharField(default='Granja Ovos Seu João', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='empresa',
            name='telefone',
            field=models.CharField(default='991154681', max_length=15),
            preserve_default=False,
        ),
    ]