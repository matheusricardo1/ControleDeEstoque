# Generated by Django 5.0.6 on 2024-05-22 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('granja', '0019_alter_venda_data_entrega'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='telefone',
            field=models.CharField(blank=True, max_length=12, verbose_name='Telefone:'),
        ),
    ]
