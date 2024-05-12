from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST

from .models import *
from .serializers import *
from django.contrib.auth import authenticate
from django.http import HttpResponse,JsonResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission 

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models import Q


def index(request):
    publicacoes_list = Publicacao.objects.order_by('-data_publicacao')#[:5] #TODO
    if (not request.user.is_authenticated):
        publicacoes_list = publicacoes_list.filter(permissao='T')
    else:
        utilizador = Utilizador.objects.get(user=request.user)
        publicacoes_list = publicacoes_list.filter(
            Q(publicacaogrupo__grupo__utilizadorgrupo__utilizador=utilizador)
            | Q(publicacaocinema__cinema__utilizadorcinema__utilizador=utilizador)
            | Q(permissao='T')
        ).distinct()
    return render(request, 'movies/index.html', {
        'publicacoes_list': publicacoes_list
    })

def registerUser(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST['username'],
            email=request.POST['email'],
            password=request.POST['password'],
        )
        utilizador = Utilizador(user=user)
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
            login(request,user)
            return HttpResponseRedirect(reverse('movies:index'))

        else:
            return render(request, 'movies/login.html', {
                'error_message': 'Falha de login'
            })
    else:
        return render(request, 'movies/login.html')

@login_required
def logoutUser (request):
    logout(request)
    return HttpResponseRedirect(reverse('movies:index'))

@login_required
def createGroup(request):
    if request.method == 'POST':
        utilizador = Utilizador.objects.get(user=request.user)
        grupo = Grupo.create(request.POST.get('groupname'),bool(request.POST.get("publico")))
        utilizadorGrupo = UtilizadorGrupo(
            utilizador=utilizador,
            grupo=grupo,
            administrador=True,
            convite_por_aceitar_user=False,
            convite_por_aceitar_grupo=False,
            date_joined=timezone.now()
        )
        utilizadorGrupo.save()
        return HttpResponseRedirect(reverse('movies:group', args=(grupo.id,)))
    else:
        return render(request, 'movies/createGroup.html')

@login_required
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
                .order_by('timestamp')  # [:5]  TODO
            context['group_name'] = group_name
            context['group_id'] = group_id
            context['messages_list'] = messages_list
            context['group_id'] = group_id
        context['groups_list'] = groups_list
        return render(request, 'movies/group.html', context)

@login_required
def createPost(request):
    utilizador = Utilizador.objects.get(user=request.user)
    if request.method == 'POST':
        publicacao = Publicacao(
            data_publicacao=timezone.now(),
            texto=request.POST['text'],
            utilizador=utilizador,
            filme=Filme.objects.get(pk=request.POST['film_id'])
        )
        publicacao.save()
        for group_id in request.POST.getlist('groups[]'):
            publicacaoGrupo = PublicacaoGrupo(
                publicacao=publicacao,
                grupo=Grupo.objects.get(pk=group_id)
            )
            publicacaoGrupo.save()
        for cinema_id in request.POST.getlist('cinemas[]'):
            publicacaoCinema = PublicacaoGrupo(
                publicacao=publicacao,
                grupo=Grupo.objects.get(pk=cinema_id)
            )
            publicacaoCinema.save()
        return HttpResponseRedirect(reverse('movies:index'))
    else:
        groups_list = Grupo.objects.filter(utilizadorgrupo__utilizador=utilizador)
        cinemas_list = Cinema.objects.filter(utilizadorcinema__utilizador=utilizador)
        films_list = Filme.objects.filter(
            Q(elementolista__lista__grupo__utilizadorgrupo__utilizador=utilizador)
            | Q(elementolista__lista__utilizador=utilizador)
        ).distinct()
        return render(request, 'movies/createpost.html', {
            'groups_list': groups_list,
            'cinemas_list': cinemas_list,
            'films_list': films_list
        })

@require_POST
def sendMessage(request):
    utilizador = Utilizador.objects.get(user=request.user)
    group = Grupo.objects.get(pk=request.POST['group_id'])
    message_text = request.POST['message']
    message = Mensagem(
        sender=utilizador,
        grupo=group,
        timestamp=timezone.now(),
        texto=message_text
    )
    message.save()
    return JsonResponse({
        'message_id': 69,
        'message_text': message_text
    })

@require_POST
def receiveMessage(request):
    #for i in request.POST.getlist('shown_messages_id_list[]'):
    #    print('RECEIVED ---> ', i)
    #print('')
    messages_list = Mensagem.objects\
        .filter(grupo_id=request.POST['group_id'])\
        .exclude(id__in=request.POST.getlist('shown_messages_id_list[]'))
    
    return JsonResponse({
        'messages_list': list(messages_list.values('id', 'texto','sender__imagem'))
    })

def getRecentGroupsList(user):
    recentgroups_list = Grupo.objects.filter(Utilizador.objects.get(
        user=user
    )).order_by('last_message_timestamp')
    return recentgroups_list

@login_required
def inviteToGroup(request, group_id):
    context = {}
    if(request.method=="GET"):
        search=request.GET.get("search","")
        context['search']=search
        context['group_id'] = group_id
        utilizador = Utilizador.objects.get(user=request.user)

        context['groups_list'] = Grupo.objects.filter(utilizadorgrupo__utilizador=utilizador)
        context['members'] = UtilizadorGrupo.objects.filter(grupo__id=group_id,convite_por_aceitar_user=False,convite_por_aceitar_grupo=False,utilizador__user__username__icontains=search)

        ug = UtilizadorGrupo.objects.filter(utilizador=utilizador,grupo__id=group_id).first()
        context['admin'] = ug.administrador if ug is not None else False
        
        def add_ug_if_exists(utilizador):
            ug = UtilizadorGrupo.objects.filter(utilizador=utilizador,grupo__id=group_id).first()
            return {"utilizador":utilizador,"ug":ug}

        if(context['admin']):
            context['users'] = list(map(add_ug_if_exists,Utilizador.objects.filter(user__username__icontains=search).filter(~Q(id__in=context['members'].values("utilizador")))[:25]))
        return render(request, 'movies/inviteToGroup.html', context)
    elif(request.method=="POST"):
        if(request.POST.get('RemoveAdmin')):
            ug = UtilizadorGrupo.objects.get(id=request.POST.get('ug_id'))
            ug.unpromote()
        elif(request.POST.get('AddAdmin')):
            ug = UtilizadorGrupo.objects.get(id=request.POST.get('ug_id'))
            ug.promote()
        elif(request.POST.get('RemoveFromGroup') or request.POST.get('RefuseJoin') or request.POST.get('RemoveInvite')):
            ug = UtilizadorGrupo.objects.get(id=request.POST.get('ug_id'))
            ug.remove_user()
        elif(request.POST.get('AcceptJoin')):
            ug = UtilizadorGrupo.objects.get(id=request.POST.get('ug_id'))
            ug.accept_join_request()
        elif(request.POST.get('AddInvite')):
            u = Utilizador.objects.get(id=request.POST.get('utilizador_id'))
            grupo = Grupo.objects.get(id=group_id)
            UtilizadorGrupo.grupo_invite_user(grupo,u)
        else:
            print("Error. Empty form.")

        search=request.POST.get("search","")
        print(search)
        return HttpResponseRedirect(reverse('movies:inviteToGroup', args=(group_id,),) + "?search=" +search)

    else:
        return HttpResponse("TODO" + " - Convidar para o grupo " + str(group_id) + "\nBAD METHOD: "+request.method)






@login_required
def databaseTest(request):
    output = "<h1>DATABASE DUMP</h1>\n<ul>\n"

    output += "<a href='/movies'>Go to the site</a>\n\n"

    output += "<li>Utilizador<ul>\n"
    for user in Utilizador.objects.all():
        output+= "<li> <ul> <li>Username:"+user.user.username+"</li>\n"
        output+= "<li>Email:" + user.user.email + "</li>\n"
        output+= "<li>Imagem: <a href='"  +"http://localhost:8000/static/" + user.imagem + "'>"+user.imagem+"</a> </li>\n"
        output+= "<li>Verificado:" + str(user.verificado) + "</li>\n"
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
        output+= "<li>Imagem: <a href='" +"http://localhost:8000/static/"+ filme.imagem + "'>"+filme.imagem+"</a> </li>\n"
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
        output+= "<li>Imagem: <a href='"+"http://localhost:8000/static/" + grupo.imagem + "'>"+grupo.imagem+"</a> </li></ul></li>\n"

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


@login_required(login_url=reverse_lazy('movies:loginUser'))
def listUsers(request):
    users_list = Utilizador.objects.order_by('data_adesao')[:5]
    context = {
        'users_list': users_list
    }
    return render(request, 'movies/listUsers.html', context)


def userOptions(request, user_id):
    user = get_object_or_404(Utilizador, pk=user_id)
    context = {
        'user': user
    }
    return render(request, 'movies/userOptions.html', context)


def logoutuser (request):
    logout(request)
    return HttpResponseRedirect(reverse('movies:index'))   


@permission_required('movies.deleteUser', login_url=reverse_lazy('movies:loginuser'))
def deleteUser (request, user_id):
    user = get_object_or_404(Utilizador, pk=user_id)
    user.delete()

    return HttpResponseRedirect(reverse('movies:listUsers'))   


@permission_required('movies.editUser', login_url=reverse_lazy('movies:loginuser'))
def editUser (request, user_id):
    utilizador = get_object_or_404(Utilizador, pk=user_id) 
    user = utilizador.user

    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        new_verified = request.POST.get('verified')

        print(user.username)
        if new_username.strip(): user.username = new_username
        print(new_username)
        
        if(new_email):user.email = new_email
        
        print(new_verified)
        if(new_verified == "on"):
            utilizador.verificado = True
        elif (new_verified == None):
            utilizador.verificado = False
        else: False

        user.save()
        utilizador.save()
        
    return HttpResponseRedirect(reverse('movies:index'))  