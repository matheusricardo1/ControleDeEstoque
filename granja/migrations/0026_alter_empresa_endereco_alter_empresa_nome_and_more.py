# Generated by Django 5.0.6 on 2024-06-25 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('granja', '0025_alter_empresa_endereco_alter_empresa_nome_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='endereco',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='nome',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='telefone',
            field=models.CharField(max_length=15),
        ),
    ]