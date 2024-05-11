from django.urls import path#,include
from . import views

app_name = 'movies'
urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.registerUser, name="registerUser"),
    path("login", views.loginUser, name="loginUser"),
    path("creategroup", views.createGroup, name="createGroup"),
    path("group/<int:group_id>", views.group, name="group"),
    path("listUsers", views.listUsers, name="listUsers"),
    path("listUsers/<int:user_id>", views.userOptions, name='userOptions'),
    path('index', views.logoutuser, name='logoutuser'),
    path('<int:user_id>/deleteUser', views.deleteUser, name="deleteUser"),
    path('<int:user_id>/editUser', views.editUser, name="editUser"),
 
    #Test
    path("test", views.databaseTest, name="databaseTest"),

    #React 
    path('api/login/', views.login_api, name='login'),
    path('api/escolhas/', views.escolhas),#POST-Lista de escolhas de um evento
    path('api/eventos/', views.eventos),#POST-Lista de eventos de um grupo
    path('api/grupos/', views.grupos),#POST-Lista de grupos do utilizador
    path('api/voto/', views.voto),#POST-Efetua o voto num elemento da lista de escolhas
]
