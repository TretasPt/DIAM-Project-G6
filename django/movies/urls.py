from django.urls import include, path
from . import views
# from .views import LoginView

urlpatterns=[
    path("",views.index, name="index"),
    path("test",views.databaseTest, name="databaseTest"),
    
    #React login
    # path('api/login/', LoginView.as_view(), name='login'),#Old login
    path('api/login/', views.login, name='login'),

    path('api/grupos/', views.grupos),#POST-Lista de grupos do utilizador
    path('api/eventos/', views.eventos),#POST-Lista de eventos de um grupo
    path('api/escolhas/', views.escolhas),#POST-Lista de escolhas de um evento
    path('api/voto/', views.voto),#POST-Efetua o voto num elemento da lista de escolhas
]