from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('playing/<str:username>/', views.playing, name='playing')
]
