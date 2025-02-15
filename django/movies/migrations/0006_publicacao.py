# Generated by Django 5.0.4 on 2024-04-29 07:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_evento_mensagem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publicacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permissao', models.CharField(choices=[('T', 'Todos'), ('G', 'Grupo'), ('C', 'Cinema')], default='T', max_length=1)),
                ('data_publicacao', models.DateTimeField()),
                ('texto', models.CharField(max_length=1000)),
                ('timestamp_inicio', models.IntegerField(blank=True)),
                ('timestamp_fim', models.IntegerField(blank=True)),
                ('cinema', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='movies.cinema')),
                ('filme', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='movies.filme')),
                ('grupo', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='movies.grupo')),
                ('parent', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='movies.publicacao')),
            ],
        ),
    ]
