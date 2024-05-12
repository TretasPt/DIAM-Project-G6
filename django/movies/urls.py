from django.urls import path#,include
from . import views

app_name = 'movies'
urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.registerUser, name="registerUser"),
    path("login", views.loginUser, name="loginUser"),
    path('deleteUser/<int:user_id>', views.deleteUser, name="deleteUser"),
    path('editUser/<int:user_id>', views.editUser, name="editUser"),
    path("logout", views.logoutUser, name="logoutUser"),
    path("profile", views.profile, name="profile"),
    path('index', views.logoutuser, name='logoutuser'),
    path("creategroup", views.createGroup, name="createGroup"),
    path("createpost", views.createPost, name="createPost"),
    path("sendmessage", views.sendMessage, name="sendMessage"),
    path("receivemessage", views.receiveMessage, name="receiveMessage"),
    path("group/<int:group_id>", views.group, name="group"),
    path("listUsers", views.listUsers, name="listUsers"),
    path("listUsers/<int:user_id>", views.userOptions, name='userOptions'),
    path('discovery', views.discovery, name="discovery"),
    path('searchcinema', views.searchCinema, name="searchCinema"),
    path('adherecinema', views.adhereCinema, name="adhereCinema"),
    path("inviteToGroup/<int:group_id>", views.inviteToGroup, name="inviteToGroup"),
    path("userAcceptInvite/<int:group_id>", views.userAcceptInvite, name="userAcceptInvite"),
 
    path("listMovies", views.listMovies, name="listMovies"),
    path('searchMovie', views.searchMovie, name="searchMovie"),
    path("listMovies/<int:filme_id>", views.moviesOptions, name='moviesOptions'),
    path('editMovie/<int:filme_id>', views.editMovie, name="editMovie"),

    #Test
    path("test", views.databaseTest, name="databaseTest"),

    #React 
    path('api/login/', views.login_api, name='login'),
    path('api/escolhas/', views.escolhas),#POST-Lista de escolhas de um evento
    path('api/eventos/', views.eventos),#POST-Lista de eventos de um grupo
    path('api/grupos/', views.grupos),#POST-Lista de grupos do utilizador
    path('api/voto/', views.voto),#POST-Efetua o voto num elemento da lista de escolhas
]
