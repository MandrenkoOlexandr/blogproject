from django.urls import path
from . import views

app_name = "myblog"

urlpatterns = [
    path("", views.home, name="home"),                              # /myblog/
    path("articles/", views.article_list, name="article_list"),     # /myblog/articles/?category=ID&tag=ID
    path("articles/<int:pk>/", views.article_detail, name="article_detail"),
    path("articles/<int:pk>/comment/", views.add_comment, name="add_comment"),
    path("categories/", views.category_list, name="category_list"),

]
