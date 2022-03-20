from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create_page, name="create_page"),
    path("edit", views.edit_page, name="edit_page"),
    path("save", views.save_page, name = "save_page"),
    path("random", views.random_page, name = "random_page"),
    path("<str:title>", views.display_info, name = "display")
    
]
