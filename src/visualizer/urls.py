from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signout', views.signout, name='signout'),
    path('update_settings/', views.update_settings, name='update_settings'),
    path('<str:username>/', views.visview, name='visview'),
]
