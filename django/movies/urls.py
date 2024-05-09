from django.urls import path#,include
from . import views

app_name = 'movies'
urlpatterns = [
 path("", views.index, name="index"),
 path("register", views.registerUser, name="registerUser"),
 path("login", views.loginUser, name="loginUser"),
 path("creategroup", views.createGroup, name="createGroup"),
 path("<int:group_id>/group", views.group, name="group"),
 
 #Test
 path("test", views.databaseTest, name="databaseTest"),

 #React 
    path('api/login/', views.login, name='login'),
    path('api/escolhas/', views.escolhas),#POST-Lista de escolhas de um evento
    path('api/eventos/', views.eventos),#POST-Lista de eventos de um grupo
    path('api/grupos/', views.grupos),#POST-Lista de grupos do utilizador
    path('api/voto/', views.voto),#POST-Efetua o voto num elemento da lista de escolhas
]
