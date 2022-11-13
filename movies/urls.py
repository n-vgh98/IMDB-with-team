from django.urls import path
from .views import *

urlpatterns = [
    path('', movies_list, name="movies_list"),
    path('detail/<int:pk>', movie_detail, name="movie_detail")

]
