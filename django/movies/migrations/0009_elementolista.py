# Generated by Django 5.0.4 on 2024-04-29 07:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0008_listafilmes'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElementoLista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.filme')),
                ('lista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.listafilmes')),
            ],
        ),
    ]
