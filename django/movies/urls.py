from django.urls import include, path
from . import views
from .views import LoginView

urlpatterns=[
    path("",views.index, name="index"),
    path("test",views.databaseTest, name="databaseTest"),
    
    #React login
    path('external/login/', LoginView.as_view(), name='login'),
]