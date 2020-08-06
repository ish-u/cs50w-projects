from django.urls import path
from . import views

urlpatterns =[
    path("",views.index,name="index"),
    path("video/",views.video,name="video"),
    path("video/<str:id>",views.video,name="video"),
    path("register",views.register,name="register"),
    path("playlist/<str:id>",views.playlist,name="playlist"),
    path("playlist",views.playlist,name="playlist"),
    path("admin-dashboard",views.admin_dashboard,name="admin-dashboard"),
    path("remove/<str:id>",views.remove,name="remove"),
    path("search",views.search,name="search"),
]