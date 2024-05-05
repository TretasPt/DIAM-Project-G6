from rest_framework import serializers
from .models import Evento,EscolhaFilme,Voto,Grupo,Saga,Genre,Filme#,Utilizador

class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = ('pk', 'data_criacao','nome','imagem')

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = ('pk','nome','grupo')

class EscolhaFilmeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EscolhaFilme
        fields = ('pk', 'sessao','filme','evento')

class VotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voto
        fields = ('pk','utilizador','voto')



class SagaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saga
        fields = ('pk','nome')

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('pk','nome')

class FilmeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filme
        fields = ('pk','nome','genre','saga','duracao','imagem','data_publicacao')


#May need to add: utilizador|user
