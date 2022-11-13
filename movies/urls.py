from django.urls import path
from .views import *

urlpatterns = [
    path('', movies_list, name="movies_list"),

]
