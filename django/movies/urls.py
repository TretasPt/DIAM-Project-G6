from django.urls import include, path
from . import views

app_name = 'movies'
urlpatterns = [
 path("", views.index, name="index"),
 path("register", views.registerUser, name="register"),
 path("login", views.loginUser, name="login"),
 path("group", views.group, name="group"),
 path("test", views.databaseTest, name="databaseTest"),
]
