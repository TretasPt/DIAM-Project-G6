from django.db import models
from django.contrib.auth.models import User
# from django.utils import timezone
# import datetime
from django.utils.translation import gettext_lazy as _

#TODO Check all the field options.
#TODO Check all max_length s

class Utilizador(models.Model):
    #Nome é parte do user
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    data_adesao = models.DateTimeField(auto_now_add=True)
    verificado = models.BooleanField(default=False)
    imagem = models.CharField(max_length=200,default="NO_USER_IMAGE")

class Saga(models.Model):
    nome = models.CharField(max_length=100)

class Genre(models.Model):
    nome = models.CharField(max_length=100)

class Filme(models.Model):
    nome = models.CharField(max_length=100)
    genre = models.ForeignKey(Genre, models.SET_NULL, null=True)
    saga = models.ForeignKey(Saga, models.SET_NULL,blank=True,null=True)
    duracao = models.IntegerField()
    imagem = models.CharField(max_length=200,default="NO_MOVIE_IMAGE")
    data_publicacao = models.DateField()#Não precisa de ser DateTime porque não tem time.

class Cinema(models.Model):
    localizacao = models.CharField(max_length=200)
    administrador = models.ForeignKey(Utilizador, models.SET_NULL, blank=True, null=True)#Cinemas sem administrador ficam a null.

class Grupo(models.Model):
    data_criacao = models.DateTimeField(auto_now_add=True)
    nome = models.CharField(max_length=100)
    imagem = models.CharField(max_length=200,default="NO_GROUP_IMAGE")

class Publicacao(models.Model):

    class Permissao(models.TextChoices):
        EVERYONE = 'T' , _('Todos')
        GROUP = 'G' , _('Grupo')
        CINEMA = 'C' , _('Cinema')

    permissao = models.CharField(max_length=1,choices=Permissao.choices,default=Permissao.TODOS)
    parent = models.ForeignKey('self', models.SET_NULL,blank=True,null=True)
    data_publicacao = models.DateTimeField(auto_now_add=True)
    texto = models.CharField(max_length=1000)#TODO Mayeb use models.TextField() instead
    grupo = models.ForeignKey(Grupo, models.CASCADE,blank=True,null=True)
    cinema = models.ForeignKey(Cinema, models.CASCADE,blank=True,null=True)
    filme = models.ForeignKey(Filme, models.CASCADE,blank=True,null=True)
    timestamp_inicio = models.TimeField(blank=True,null=True)#TODO Consider using models.IntegerField() instead
    timestamp_fim = models.TimeField(blank=True,null=True)#TODO Consider using models.IntegerField() instead
    utilizador = models.ForeignKey(Utilizador, models.CASCADE)

class Mensagem(models.Model):
    sender = models.ForeignKey(Utilizador, models.SET_NULL, blank=True, null=True)
    grupo = models.ForeignKey(Grupo, models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    texto = models.CharField(max_length=1000)#TODO Mayeb use models.TextField() instead

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
    utilizador = models.ForeignKey(Utilizador, models.CASCADE, blank=True, null=True)
    grupo = models.ForeignKey(Grupo, models.CASCADE,blank=True, null=True)
    #TODO Check if it has either a group or a user

class ElementoLista(models.Model):
    lista = models.ForeignKey(ListaFilmes, models.CASCADE)
    filme = models.ForeignKey(Filme, models.CASCADE)

class UtilizadorGrupo(models.Model):
    utilizador = models.ForeignKey(Utilizador, models.CASCADE)
    grupo = models.ForeignKey(Grupo, models.CASCADE)
    administrador = models.BooleanField(default=False)
    convite_por_aceitar = models.BooleanField(default=True)
    date_joined = models.DateTimeField(null=True)#Para eleger o proximo admin em caso de saida. Pode ser null se ainda não tiver aceite o convite

class UtilizadorCinema(models.Model):
    utilizador = models.ForeignKey(Utilizador, models.CASCADE)
    cinema = models.ForeignKey(Cinema,models.CASCADE)
