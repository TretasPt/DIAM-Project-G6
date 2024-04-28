from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.utils.translation import gettext_lazy as _

# Create your models here.
#TODO Check all the field options.

class Utilizador(models.Model):
    #Nome é parte do user
    user = models.OneToOneField(User,on_delete=models.RESTRICT)#TODO On delete CASCADE?
    data_adesao = models.DateTimeField()#TODO Check options
    verificado = models.BooleanField(default=False)#TODO Check options

class Saga(models.Model):
    nome = models.CharField(max_length=100)

class Genre(models.Model):
    nome = models.CharField(max_length=100)

class Filme(models.Model):
    nome = models.CharField(max_length=100)
    genre = models.ForeignKey(Genre, models.SET_DEFAULT, default="None")
    saga = models.ForeignKey(Saga, models.CASCADE,blank=True)
    duracao = models.IntegerField()
    imagem = models.CharField(max_length=200)#TODO Imagens como caminhos?
    data_publicacao = models.DateTimeField()

class Cinema(models.Model):
    localizacao = models.CharField(max_length=200)
    administrador = models.ForeignKey(Utilizador, models.SET_NULL, blank=True, null=True)#TODO Check this

class Grupo(models.Model):
    data_criacao = models.DateTimeField()
    nome = models.CharField(max_length=100)
    imagem = models.CharField(max_length=200)#TODO Imagens como caminhos?

class Publicacao(models.Model):

    class Permissao(models.TextChoices):
        TODOS = 'T' , _('Todos')
        Grupo = 'G' , _('Grupo')
        CINEMA = 'C' , _('Cinema')

    permissao = models.CharField(max_length=1,choices=Permissao.choices,default=Permissao.TODOS)
    parent = models.ForeignKey('self', models.CASCADE,blank=True)
    data_publicacao = models.DateTimeField()
    texto = models.CharField(max_length=1000)#TODO Mayeb use models.TextField() instead
    grupo = models.ForeignKey(Grupo, models.CASCADE,blank=True)
    cinema = models.ForeignKey(Cinema, models.CASCADE,blank=True)
    filme = models.ForeignKey(Filme, models.CASCADE,blank=True)
    timestamp_inicio = models.IntegerField(blank=True)#TODO Consider using models.TimeField() instead
    timestamp_fim = models.IntegerField(blank=True)#TODO Consider using models.TimeField() instead

class Mensagem(models.Model):
    sender = models.ForeignKey(Utilizador, models.SET_NULL, blank=True, null=True)
    grupo = models.ForeignKey(Grupo, models.CASCADE)
    timestamp = models.DateTimeField()


class UtilizadorCinema(models.Model):
    utilizador = models.ForeignKey(Utilizador, models.CASCADE)
    cinema = models.ForeignKey(Cinema, models.CASCADE)
    pass

class Evento(models.Model):
    nome = models.CharField(max_length=200)
    grupo = models.ForeignKey(Grupo, models.CASCADE)

class EscolhaFilme(models.Model):
    sessao = models.DateTimeField()
    filme = models.ForeignKey(Filme, models.CASCADE)
    evento = models.ForeignKey(Evento, models.CASCADE)

class Voto(models.Model):
    utilizador = models.ForeignKey(Utilizador, models.CASCADE)
    voto = models.ForeignKey(EscolhaFilme, models.CASCADE)

class ListaFilmes(models.Model):

    class Tipo(models.TextChoices):
        VISTOS = 'V' , _('Vistos')
        FUTUROS = 'F' , _('Futuros')

    tipo = models.CharField(max_length=1,choices=Tipo.choices)
    utilizador = models.ForeignKey(Utilizador, models.CASCADE, blank=True)#null=true
    grupo = models.ForeignKey(Grupo, models.CASCADE,blank=True)

class ElementoLista(models.Model):
    lista = models.ForeignKey(ListaFilmes, models.CASCADE)
    filme = models.ForeignKey(Filme, models.CASCADE)

class UtilizadorGrupo(models.Model):
    utilizador = models.ForeignKey(Utilizador, models.CASCADE)
    grupo = models.ForeignKey(Grupo, models.CASCADE)
    administrador = models.BooleanField(default=False)#TODO Check default
    convite_por_aceitar = models.BooleanField(default=True)

class UtilizadorCinema(models.Model):
    utilizador = models.ForeignKey(Utilizador, models.CASCADE)
    cinema = models.ForeignKey(Cinema,models.CASCADE)
