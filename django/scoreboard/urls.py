from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<track>/', views.track_normal, name='track_normal'),
    path('<track>/<mode>/', views.track_global, name='track_global'),
    path('<track>/<mode>/<category>/', views.track_category, name='track_category'),
    path('sync', views.sync, name='sync'),
]