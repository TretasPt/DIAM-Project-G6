# Generated by Django 5.0.4 on 2024-04-29 19:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0009_elementolista'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filme',
            name='data_publicacao',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='filme',
            name='genre',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='movies.genre'),
        ),
        migrations.AlterField(
            model_name='filme',
            name='saga',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='movies.saga'),
        ),
        migrations.AlterField(
            model_name='listafilmes',
            name='grupo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.grupo'),
        ),
        migrations.AlterField(
            model_name='listafilmes',
            name='utilizador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.utilizador'),
        ),
        migrations.AlterField(
            model_name='publicacao',
            name='cinema',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.cinema'),
        ),
        migrations.AlterField(
            model_name='publicacao',
            name='filme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.filme'),
        ),
        migrations.AlterField(
            model_name='publicacao',
            name='grupo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.grupo'),
        ),
        migrations.AlterField(
            model_name='publicacao',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='movies.publicacao'),
        ),
        migrations.AlterField(
            model_name='publicacao',
            name='timestamp_fim',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='publicacao',
            name='timestamp_inicio',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='UtilizadorCinema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cinema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.cinema')),
                ('utilizador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.utilizador')),
            ],
        ),
        migrations.CreateModel(
            name='UtilizadorGrupo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('administrador', models.BooleanField(default=False)),
                ('convite_por_aceitar', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField()),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.grupo')),
                ('utilizador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.utilizador')),
            ],
        ),
    ]
