# Generated by Django 5.0.6 on 2024-05-18 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('granja', '0003_produto_preco_riscado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='nome',
            field=models.CharField(max_length=140, unique=True),
        ),
        migrations.AlterField(
            model_name='produto',
            name='preco_riscado',
            field=models.FloatField(verbose_name='Preço riscado R̶$̶2̶0̶: '),
        ),
    ]
