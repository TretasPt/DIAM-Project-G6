# Generated by Django 5.0.4 on 2024-05-02 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0010_alter_filme_data_publicacao_alter_filme_genre_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mensagem',
            name='texto',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]
