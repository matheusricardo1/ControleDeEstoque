# Generated by Django 5.0.6 on 2024-05-22 15:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('granja', '0018_alter_venda_data_entrega'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venda',
            name='data_entrega',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
