from django.urls import path

from . import views

urlpatterns = [
    path('', views.scoreboard, name='scoreboard'),
    path('json/<track>/<mode>/<category>/', views.scoreboard_json, name='json_scoreboard'),
    path('sync/', views.sync, name='sync'),
    path('sync/<int:count>/', views.sync, name='sync'),
]