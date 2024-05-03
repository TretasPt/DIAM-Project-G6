from django.urls import include, path
from . import views

app_name = 'movies'
urlpatterns = [
 path("", views.index, name="index"),
 path("test",views.databaseTest, name="databaseTest"),
]
