from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import FileSystemStorage
from django.utils import timezone

class Utilizador(models.Model):
    #Nome é parte do user
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    data_adesao = models.DateTimeField(auto_now_add=True)
    verificado = models.BooleanField(default=False)
    imagem = models.CharField(max_length=200,default="NO_USER_IMAGE.png")

    def create(username,password=None,email=None,imagem=None):
        try:
            user = User.objects.create_user(username=username,password=password,email=email)
        except Exception as e:
            print(e)
            return

        if(imagem is None):
            utilizador = Utilizador(user=user)
        else:
            try:
                fs = FileSystemStorage()
                filename = fs.save("user_images/"+imagem.name, imagem)
                image_url = fs.url(filename)
            except Exception as e:
                user.delete()
                print(e)
                return
            utilizador = Utilizador(user=user,imagem=image_url)

        utilizador.save()
        return utilizador


class Saga(models.Model):
    nome = models.CharField(max_length=100)

class Genre(models.Model):
    nome = models.CharField(max_length=100)

class Filme(models.Model):
    nome = models.CharField(max_length=100)
    genre = models.ForeignKey(Genre, models.SET_NULL, null=True)
    saga = models.ForeignKey(Saga, models.SET_NULL,blank=True,null=True)
    duracao = models.IntegerField()
    imagem = models.CharField(max_length=200,default="NO_MOVIE_IMAGE.png")
    data_publicacao = models.DateField()#Não precisa de ser DateTime porque não tem time.

    def create(nome,genre,saga,duracao,imagem,data_publicacao):

        try:
            fs = FileSystemStorage()
            filename = fs.save("movie_images/"+imagem.name, imagem)
            image_url = fs.url(filename)
        except Exception as e:
            print(e)
            return

        filme = Filme(nome=nome,genre=genre,saga=saga,duracao=duracao,imagem=image_url,data_publicacao=data_publicacao)
        filme.save()
        return filme

class Cinema(models.Model):
    localizacao = models.CharField(max_length=200)
    administrador = models.ForeignKey(Utilizador, models.SET_NULL, blank=True, null=True)#Cinemas sem administrador ficam a null.

class Grupo(models.Model):
    data_criacao = models.DateTimeField(auto_now_add=True)
    nome = models.CharField(max_length=100)
    imagem = models.CharField(max_length=200,default="NO_GROUP_IMAGE.png")
    publico = models.BooleanField(default=False)

    def get_last_message(grupo):
        return Mensagem.objects.filter(grupo=grupo).order_by("timestamp").last()

    def create(nome,publico=False,imagem=None):
        if(imagem is None):
            group = Grupo(nome=nome,publico=publico)
        else:
            try:
                fs = FileSystemStorage()
                filename = fs.save("group_images/"+imagem.name, imagem)
                image_url = fs.url(filename)
            except Exception as e:
                print(e)
                return
            group = Grupo(nome=nome,imagem=image_url,publico=publico)

        group.save()
        return group

class Publicacao(models.Model):

    class Permissao(models.TextChoices):
        EVERYONE = 'T' , _('Todos')
        GROUP = 'G' , _('Grupo')
        CINEMA = 'C' , _('Cinema')

    permissao = models.CharField(max_length=1,choices=Permissao.choices,default=Permissao.EVERYONE)
    parent = models.ForeignKey('self', models.SET_NULL,blank=True,null=True)
    data_publicacao = models.DateTimeField(auto_now_add=True)
    texto = models.CharField(max_length=1000)
    grupo = models.ForeignKey(Grupo, models.CASCADE,blank=True,null=True)
    cinema = models.ForeignKey(Cinema, models.CASCADE,blank=True,null=True)
    filme = models.ForeignKey(Filme, models.CASCADE,blank=True,null=True)
    timestamp_inicio = models.TimeField(blank=True,null=True)
    timestamp_fim = models.TimeField(blank=True,null=True)
    utilizador = models.ForeignKey(Utilizador, models.CASCADE)
    destaque = models.BooleanField(default=False)


class Mensagem(models.Model):
    sender = models.ForeignKey(Utilizador, models.SET_NULL, blank=True, null=True)
    grupo = models.ForeignKey(Grupo, models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    texto = models.CharField(max_length=1000)

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
    
    def clean(self, *args, **kwargs):
        if self.utilizador is None and self.grupo is None:
            raise ValidationError(_("ListaFilmes deve conter pelo menos ou um utilizador ou um grupo."))
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class ElementoLista(models.Model):
    lista = models.ForeignKey(ListaFilmes, models.CASCADE)
    filme = models.ForeignKey(Filme, models.CASCADE)

class UtilizadorGrupo(models.Model):
    utilizador = models.ForeignKey(Utilizador, models.CASCADE)
    grupo = models.ForeignKey(Grupo, models.CASCADE)
    administrador = models.BooleanField(default=False)
    date_joined = models.DateTimeField(null=True)#Para eleger o proximo admin em caso de saida. Pode ser null se ainda não tiver aceite o convite
    convite_por_aceitar_user = models.BooleanField(default=True)
    convite_por_aceitar_grupo = models.BooleanField(default=True)

    def accept_invitation(self):
        self.convite_por_aceitar_user=False
        self.date_joined=timezone.now()
        self.save()
    def accept_join_request(self):
        self.convite_por_aceitar_grupo=False
        self.date_joined=timezone.now()
        self.save()
    def grupo_invite_user(grupo,utilizador):#convite_por_aceitar_grupo=False,convite_por_aceitar_user=True
        ug = UtilizadorGrupo(utilizador=utilizador,grupo=grupo,convite_por_aceitar_grupo=False)
        ug.save()
        return ug
    def user_request_join_group(utilizador,grupo):#convite_por_aceitar_grupo=True,convite_por_aceitar_user=False
        ug = UtilizadorGrupo(utilizador=utilizador,grupo=grupo,convite_por_aceitar_user=False)
        ug.save()
        return ug

class UtilizadorCinema(models.Model):
    utilizador = models.ForeignKey(Utilizador, models.CASCADE)
    cinema = models.ForeignKey(Cinema,models.CASCADE)

