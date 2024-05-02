from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.
def index(request):
    return HttpResponse("Pagina de entrada da app votacao.")

def databaseTest(request):
    output = "<h1>DATABASE DUMP</h1>\n<ul>\n"

    output += "<li>Utilizador<ul>\n"
    for user in Utilizador.objects.all():
        output+= "<li> <ul> <li>Username:"+user.user.username+"</li>\n"
        output+= "<li>Email:" + user.user.email + "</li>\n"
        output+= "<li>Data de adesão:" + str(user.data_adesao)+"</li></ul></li>\n"
    output +="</ul></li>\n"

    output += "<li>Saga<ul>\n"
    for saga in Saga.objects.all():
        output+= "<li>"+saga.nome+"</li>\n"
    output +="</ul></li>\n"

    output += "<li>Genre<ul>\n"
    for genre in Genre.objects.all():
        output+= "<li>"+genre.nome+"</li>\n"
    output +="</ul></li>\n"

    output += "<li>Filme<ul>\n"
    for filme in Filme.objects.all():
        output+= "<li> <ul> <li>Nome:"+filme.nome+"</li>\n"
        output+= "<li>Genero:" + (filme.genre.nome if filme.genre else "Não definido") + "</li>\n"
        output+= "<li>Saga:" + (filme.saga.nome if filme.saga else "Não definido") + "</li>\n"
        output+= "<li>Duracao:" + str(filme.duracao) + "</li>\n"
        output+= "<li>Imagem:" + filme.imagem + "</li>\n"
        output+= "<li>Data de publicacao:" + str(filme.data_publicacao)+"</li></ul></li>\n"
    output +="</ul></li>\n"

    output += "<li>Cinema<ul>\n"
    for cinema in Cinema.objects.all():
        output+= "<li> <ul> <li>Localização:"+cinema.localizacao+"</li>\n"
        output+= "<li>Administrador:" + (cinema.administrador.user.username if cinema.administrador else "Não definido") + "</li></ul></li>\n"
    output +="</ul></li>\n"

    output += "<li>Grupo<ul>\n"
    for grupo in Grupo.objects.all():
        output+= "<li> <ul> <li>Nome:"+grupo.nome+"</li>\n"
        output+= "<li>Data de criação:" + str(grupo.data_criacao) + "</li>\n"
        output+= "<li>Imagem:" + grupo.imagem+"</li></ul></li>\n"
    output +="</ul></li>\n"


# class Publicacao(models.Model):

#     class Permissao(models.TextChoices):
#         TODOS = 'T' , _('Todos')
#         Grupo = 'G' , _('Grupo')
#         CINEMA = 'C' , _('Cinema')

#     permissao = models.CharField(max_length=1,choices=Permissao.choices,default=Permissao.TODOS)
#     parent = models.ForeignKey('self', models.SET_NULL,blank=True,null=True)
#     data_publicacao = models.DateTimeField()
#     texto = models.CharField(max_length=1000)#TODO Mayeb use models.TextField() instead
#     grupo = models.ForeignKey(Grupo, models.CASCADE,blank=True,null=True)
#     cinema = models.ForeignKey(Cinema, models.CASCADE,blank=True,null=True)
#     filme = models.ForeignKey(Filme, models.CASCADE,blank=True,null=True)
#     timestamp_inicio = models.TimeField(blank=True,null=True)#TODO Consider using models.IntegerField() instead
#     timestamp_fim = models.TimeField(blank=True,null=True)#TODO Consider using models.IntegerField() instead

# class Mensagem(models.Model):
#     sender = models.ForeignKey(Utilizador, models.SET_NULL, blank=True, null=True)
#     grupo = models.ForeignKey(Grupo, models.CASCADE)
#     timestamp = models.DateTimeField()

# class Evento(models.Model):
#     nome = models.CharField(max_length=200)
#     grupo = models.ForeignKey(Grupo, models.CASCADE)


    output += "</ul>\n"
    return HttpResponse(output)