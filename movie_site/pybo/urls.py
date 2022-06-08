from django.urls import path

from .views import base_views

app_name = 'pybo'

urlpatterns = [
    #base_views.py
    path('', base_views.index, name='index'),
    path('movie_code=<int:movie_code>/', base_views.detail, name='detail'),
]