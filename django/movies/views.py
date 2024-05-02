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

    output += "<li>Publicacao<ul>\n"
    for pub in Publicacao.objects.all():
        output+= "<li> <ul> <li>Permissão:"+pub.permissao+"</li>\n"
        output+= "<li>Parent:" + (str(pub.parent) if pub.parent else "Não definido") + "</li>\n"
        output+= "<li>Data de publicação:" + str(pub.data_publicacao) + "</li>\n"
        output+= "<li>Texto:" + pub.texto + "</li>\n"
        output+= "<li>Grupo:" +  (pub.grupo.nome if pub.grupo else "Não definido") + "</li>\n"
        output+= "<li>Cinema:" +  (pub.cinema.localizacao if pub.cinema else "Não definido") + "</li>\n"
        output+= "<li>Filme:" +  (pub.filme.nome if pub.filme else "Não definido") + "</li>\n"
        output+= "<li>Timestamp inicio:" + (str(pub.timestamp_inicio) if pub.timestamp_inicio else "Não definido")+"</li>\n"
        output+= "<li>Timestamp fim:" + (str(pub.timestamp_fim) if pub.timestamp_fim else "Não definido")+"</li></ul></li>\n"
    output +="</ul></li>\n"

    output += "<li>Mensagem<ul>\n"
    for mensagem in Mensagem.objects.all():
        output+= "<li> <ul> <li>Grupo:"+mensagem.grupo.nome+"</li>\n"
        output+= "<li>Sender:" + (str(mensagem.sender.user.username) if mensagem.sender else "Não definido") + "</li>\n"
        output+= "<li>Texto:" + mensagem.texto + "</li>\n"
        output+= "<li>Timestamp:" + (str(mensagem.timestamp) if mensagem.timestamp else "Não definido")+"</li></ul></li>\n"
    output +="</ul></li>\n"

    output += "<li>Evento<ul>\n"
    for evento in Evento.objects.all():
        output+= "<li> <ul> <li>Nome:"+evento.nome+"</li>\n"
        output+= "<li>Grupo:" + evento.grupo.nome+"</li></ul></li>\n"
    output +="</ul></li>\n"


# class EscolhaFilme(models.Model):
#     sessao = models.DateTimeField()
#     filme = models.ForeignKey(Filme, models.CASCADE)
#     evento = models.ForeignKey(Evento, models.CASCADE)

# class Voto(models.Model):
#     utilizador = models.ForeignKey(Utilizador, models.CASCADE)
#     voto = models.ForeignKey(EscolhaFilme, models.CASCADE)

# class ListaFilmes(models.Model):

#     class Tipo(models.TextChoices):
#         VISTOS = 'V' , _('Vistos')
#         FUTUROS = 'F' , _('Futuros')

#     tipo = models.CharField(max_length=1,choices=Tipo.choices)
#     utilizador = models.ForeignKey(Utilizador, models.CASCADE, blank=True, null=True)#null=true?
#     grupo = models.ForeignKey(Grupo, models.CASCADE,blank=True, null=True)

# class ElementoLista(models.Model):
#     lista = models.ForeignKey(ListaFilmes, models.CASCADE)
#     filme = models.ForeignKey(Filme, models.CASCADE)

# class UtilizadorGrupo(models.Model):
#     utilizador = models.ForeignKey(Utilizador, models.CASCADE)#TODO Mudar para restrict
#     grupo = models.ForeignKey(Grupo, models.CASCADE)
#     administrador = models.BooleanField(default=False)#TODO Check default
#     convite_por_aceitar = models.BooleanField(default=True)
#     date_joined = models.DateTimeField()#Para eleger o proximo admin em caso de saida.

# class UtilizadorCinema(models.Model):
#     utilizador = models.ForeignKey(Utilizador, models.CASCADE)
#     cinema = models.ForeignKey(Cinema,models.CASCADE)

    output += "</ul>\n"
    return HttpResponse(output)