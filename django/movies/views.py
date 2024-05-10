from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import *
from .serializers import *
from django.contrib.auth import authenticate
from django.http import HttpResponse,JsonResponse
# from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.conf import settings
from django.core.files.storage import FileSystemStorage

def index(request):
    publicacoes_list = Publicacao.objects.order_by('-data_publicacao')#[:5] #TODO
    if (not request.user.is_authenticated):
        publicacoes_list = publicacoes_list.filter(permissao='T')
    context = {
        'publicacoes_list': publicacoes_list
    }
    if (request.user.is_authenticated):
        utilizador = Utilizador.objects.get(user=request.user)
        groups_list = Mensagem.objects\
            .filter(grupo__utilizadorgrupo__utilizador=utilizador)\
            .order_by('timestamp')\
            .values('grupo_id')\
            .distinct()
        groups_list = Grupo.objects.filter(id__in=groups_list)
        context['grupos_list'] = groups_list
    return render(request, 'movies/index.html', context)

def registerUser(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST['username'],
            email=request.POST['email'],
            password=request.POST['password'],
        )
        utilizador = Utilizador(
            user=user,
        )
        utilizador.save()
        return HttpResponseRedirect(reverse('movies:index'))
    else:
        return render(request, 'movies/register.html')

def loginUser(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(
                username=username,
                password=password
            )
        except KeyError:
            return render(request, 'movies/login.html')
        if user:
            login(request, user)
            print("TODO - set profile image") #TODO - set profile image
            return HttpResponseRedirect(reverse('movies:index'))
        else:
            return render(request, 'movies/login.html', {
                'error_message': 'Falha de login'
            })
    else:
        return render(request, 'movies/login.html')

@login_required(login_url=reverse_lazy('votacao:loginUser'))
def createGroup(request):
    if request.method == 'POST':
        utilizador = Utilizador.objects.get(user=request.user)
        grupo = Grupo(
            nome=request.POST.get('groupname'),
            data_criacao=timezone.now()
        )
        utilizadorGrupo = UtilizadorGrupo(
            utilizador=utilizador,
            grupo=grupo,
            administrador=True,
            convite_por_aceitar=False,
            date_joined=timezone.now()
        )
        grupo.save()
        utilizadorGrupo.save()
        return HttpResponseRedirect(reverse('movies:group', args=(grupo.id,)))
    else:
        return render(request, 'movies/createGroup.html')

@login_required(login_url=reverse_lazy('votacao:loginUser'))
def group(request, group_id):
    if request.method == 'POST':
        message = request.POST.get('messageinput')
    else:
        context = {}
        utilizador = Utilizador.objects.get(user=request.user)
        groups_list = Grupo.objects.filter(utilizadorgrupo__utilizador=utilizador)
        if group_id == 0:
            context['no_messages'] = True
        else:
            group_name = Grupo.objects.get(pk=group_id).nome
            messages_list = Mensagem.objects \
                .filter(grupo_id=group_id) \
                .order_by('-timestamp')  # [:5]  TODO
            context['group_name'] = group_name
            context['messages_list'] = messages_list
        context['groups_list'] = groups_list
        return render(request, 'movies/group.html', context)

def getRecentGroupsList(user):
    recentgroups_list = Grupo.objects.filter(Utilizador.objects.get(
        user=user
    )).order_by('last_message_timestamp')
    return recentgroups_list






def databaseTest(request):
    output = "<h1>DATABASE DUMP</h1>\n<ul>\n"

    output += "<li>Utilizador<ul>\n"
    for user in Utilizador.objects.all():
        output+= "<li> <ul> <li>Username:"+user.user.username+"</li>\n"
        output+= "<li>Email:" + user.user.email + "</li>\n"
        output+= "<li>Imagem: <a href='"  + user.imagem + "'>"+user.imagem+"</a> </li>\n"
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
        output+= "<li>Imagem: <a href='" + filme.imagem + "'>"+filme.imagem+"</a> </li>\n"
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
        output+= "<li>É publico:" + str(grupo.publico) + "</li>\n"
        output+= "<li>Imagem: <a href='" + grupo.imagem + "'>"+grupo.imagem+"</a> </li></ul></li>\n"

    output +="</ul></li>\n"

    output += "<li>Publicacao<ul>\n"
    for pub in Publicacao.objects.all():
        output+= "<li> <ul> <li>Utilizador:"+pub.utilizador.user.username+"</li>\n"
        output+= "<li>Destaque?:" + str(pub.destaque) + "</li>\n"
        output+= "<li>Permissão:"+pub.permissao+"</li>\n"
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
        output+= "<li>Convite por aceitar user:" + str(ug.convite_por_aceitar_user) + "</li>\n"
        output+= "<li>Convite por aceitar grupo:" + str(ug.convite_por_aceitar_grupo) + "</li>\n"
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

@api_view(['POST'])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return JsonResponse({'token': token.key,'image':user.utilizador.imagem})
    else:
        return JsonResponse({'error': 'Credenciais inválidas'}, status=400)


@api_view(['POST'])
def grupos(request):
    username = request.data.get('username')
    token = request.data.get("token")
    if(username==None or token==None):
        return Response({'error':"Not enough arguments passed. Expected username and token."},status=status.HTTP_400_BAD_REQUEST)
    try:
        user = Utilizador.objects.get(user__username=username)
    except Utilizador.DoesNotExist:
        return Response({'error':"Couldn't find user."},status=status.HTTP_400_BAD_REQUEST)

    groups_of_user = UtilizadorGrupo.objects.filter(utilizador=user,convite_por_aceitar_user=False,convite_por_aceitar_grupo=False).values("grupo")
    groups = Grupo.objects.filter(id__in=groups_of_user)
    serializer = GrupoSerializer(groups,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def eventos(request):
    username = request.data.get('username')
    token = request.data.get("token")
    grupo = request.data.get("grupo")
    if(username==None or token==None or grupo == None):
        return Response({'error':"Not enough arguments passed. Expected username,token and grupo."},status=status.HTTP_400_BAD_REQUEST)
    eventos = Evento.objects.filter(grupo__id=grupo)
    serializer = EventoSerializer(eventos,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def escolhas(request):
    username = request.data.get('username')
    token = request.data.get("token")
    evento = request.data.get("evento")
    if(username==None or token==None or evento == None):
        return Response({'error':"Not enough arguments passed. Expected username,token and evento."},status=status.HTTP_400_BAD_REQUEST)

    try:
        user = Utilizador.objects.get(user__username=username)
    except Utilizador.DoesNotExist:
        return Response({'error':"Couldn't find user."},status=status.HTTP_400_BAD_REQUEST)

    escolhas = EscolhaFilme.objects.filter(evento__id=evento)
    serializer = EscolhaFilmeSerializer(escolhas,many=True)

    def addFields(escolha_filme):
        filme = FilmeSerializer(Filme.objects.get(id=escolha_filme['filme'])).data
        filme['genre'] = Genre.objects.get(id=filme['genre']).nome if Genre.objects.filter(id=filme['genre']).first() is not None else None
        filme['saga'] = Saga.objects.get(id=filme['saga']).nome if Saga.objects.filter(id=filme['saga']).first() is not None else None
        escolha_filme['filme'] = filme
        votos = Voto.objects.filter(voto=escolha_filme['pk'])
        count = len(votos)
        user_voted = len(votos.filter(utilizador=user)) >0
        escolha_filme['votos'] = {'count':count,'user_voted':user_voted}
        return escolha_filme
    res = list(map(addFields, serializer.data))
    return Response(res)

@api_view(['POST','DELETE'])
def voto(request):
    username = request.data.get('username')
    token = request.data.get("token")
    voto = request.data.get('voto')#Um id para um EscolhaFilme
    if(username==None or token==None or voto==None):
        return Response({'error':"Not enough arguments passed. Expected username,token and voto."},status=status.HTTP_400_BAD_REQUEST)

    try:
        user = Utilizador.objects.get(user__username=username)
    except Utilizador.DoesNotExist:
        return Response({'error':"Couldn't find user."},status=status.HTTP_400_BAD_REQUEST)

    escolha_filme = EscolhaFilme.objects.get(id=voto)
    temp_voto=Voto.objects.filter(utilizador=user,voto=escolha_filme)

    if request.method=='POST':
        if(len(temp_voto)!=0):
            return Response({'error':"Can't create more vote. User already has a vote on this."},status=status.HTTP_400_BAD_REQUEST)
        #create
        new_voto = Voto(utilizador=user,voto=escolha_filme)
        new_voto.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method=='DELETE':
        if(len(temp_voto)==0):
            return Response({'error':"Can't delete vote. No vote bellonging to current user."},status=status.HTTP_400_BAD_REQUEST)
        #delete
        temp_voto[0].delete()
        return Response(status=status.HTTP_202_ACCEPTED)
    else:
        return Response({'error':'Invalid request method. Methods allowed:POST,DELETE'},status=status.HTTP_400_BAD_REQUEST)

