from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import *

# Create your views here.

def index(request):
    publicacoes_list = Publicacao.objects.order_by('-data_publicacao')#[:5]  TODO
    context = {
        'publicacoes_list':publicacoes_list
    }
    return render(request, 'movies/index.html', context)

def register(request):
    if (request.method == 'POST'):
        print('register')
    else:
        return render(request, 'movies/register.html')

def login(request):
    if (request.method == 'POST'):
        print('login')
    else:
        return render(request, 'movies/login.html')

def group(request):
    return render(request, 'movies/group.html')

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

    output += "<li>EscolhaFilme<ul>\n"
    for escolhaFilme in EscolhaFilme.objects.all():
        output+= "<li> <ul> <li>Sessão:"+str(escolhaFilme.sessao)+"</li>\n"
        output+= "<li>Filme:" + escolhaFilme.filme.nome + "</li>\n"
        output+= "<li>Evento:" + escolhaFilme.evento.nome+"</li></ul></li>\n"
    output +="</ul></li>\n"

    output += "<li>Voto<ul>\n"
    for voto in Voto.objects.all():
        output+= "<li> <ul> <li>Utilizador:"+voto.utilizador.user.username+"</li>\n"
        output+= "<li>Voto:" + voto.voto.filme.nome +"|"  +str(voto.voto.sessao) + "|" + voto.voto.evento.nome+"</li></ul></li>\n"
    output +="</ul></li>\n"

    output += "<li>ListaFilmes<ul>\n"
    for lista in ListaFilmes.objects.all():
        output+= "<li> <ul> <li>Tipo:"+lista.tipo+"</li>\n"
        output+= "<li>Utilizador:" + (str(lista.utilizador.user.username) if lista.utilizador else "Não definido") + "</li>\n"
        output+= "<li>Grupo:" + (str(lista.grupo.nome) if lista.grupo else "Não definido")+"</li></ul></li>\n"
    output +="</ul></li>\n"

    output += "<li>ElementoLista<ul>\n"
    for elemento in ElementoLista.objects.all():
        output+= "<li> <ul> <li>Filme:"+elemento.filme.nome+"</li>\n"
        output+= "<li>Lista:" + elemento.lista.tipo + "|" + (str(elemento.lista.utilizador.user.username) if elemento.lista.utilizador else elemento.lista.grupo.nome) +"</li></ul></li>\n"
    output +="</ul></li>\n"

    output += "<li>UtilizadorGrupo<ul>\n"
    for ug in UtilizadorGrupo.objects.all():
        output+= "<li> <ul> <li>Administrador:"+ str(ug.administrador) +"</li>\n"
        output+= "<li>Convite por aceitar:" + str(ug.convite_por_aceitar) + "</li>\n"
        output+= "<li>Data de adesão:" + str(ug.date_joined) + "</li>\n"
        output+= "<li>Utilizador:" + ug.utilizador.user.username + "</li>\n"
        output+= "<li>Grupo:" + ug.grupo.nome +"</li></ul></li>\n"
    output +="</ul></li>\n"

    output += "<li>UtilizadorCinema<ul>\n"
    for uc in UtilizadorCinema.objects.all():
        output+= "<li> <ul> <li>Utilizador:"+ uc.utilizador.user.username +"</li>\n"
        output+= "<li>Cinema:" + uc.cinema.localizacao +"</li></ul></li>\n"
    output +="</ul></li>\n"


    output += "</ul>\n"
    return HttpResponse(output)
