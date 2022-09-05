from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from . import api

urlpatterns = [
    path('', views.index, name = 'index'),
    path('donate', views.donate, name= 'donate'),
    path('login', views.login, name='login'),
    path('profile', views.myprofile, name = 'profilePage'),
    path('registration', views.registration, name = 'registration'),
    path('logout', views.userlogout, name = 'logout'),
    path('jumpIndex', views.jumpIndex, name = 'jumpIndex'),
    path('help', views.helpBird, name = 'helpBird'),
    path('adopt', views.adopt, name= "adopt"),
    path('gallery', views.gallery, name = "gallery"),
    path('bird/<int:birdid>', views.adoptapply, name = "adoptapplication"),
    path('submitsuccess', views.success, name = 'success'),
    path('donate/<int:level>', views.donateform, name = 'donateform'),
    path('notlogin', views.loginRequire, name = 'loginRequire')
    ]