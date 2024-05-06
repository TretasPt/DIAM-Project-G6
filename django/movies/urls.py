from django.urls import include, path
from . import views

app_name = 'movies'
urlpatterns = [
 path("", views.index, name="index"),
 path("login", views.login, name="login"),
 path("test", views.databaseTest, name="databaseTest"),
]
