from django.urls import path
from .views import *

urlpatterns = [
    path('', movies_list, name="movies_list"),
    path('detail/<int:pk>', movie_detail, name="movie_detail"),
    path('add_movie/', add_movie, name="add_movie"),
    path('edit_movie/<int:pk>/', edit_movie, name="edit_movie"),
    path('delete_movie/<int:pk>/', delete_movie, name="delete_movie"),
    path('rate_moive/<int:pk>', rate_movie, name='rate_movie'),

]
