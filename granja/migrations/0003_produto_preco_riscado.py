# Generated by Django 5.0.6 on 2024-05-16 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('granja', '0002_alter_venda_desconto'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='preco_riscado',
            field=models.FloatField(default='0', verbose_name='Preço riscado R̶$̶2̶0̶: '),
        ),
    ]