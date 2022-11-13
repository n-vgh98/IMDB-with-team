from django.http import HttpResponse
from django.shortcuts import render
from .models import *


def movies_list(request):
    movies = Movie.objects.filter(is_valid=True)
    return render(request, 'movies/index.html', {'movies': movies})

def movie_detail(request, pk):
    movie = Movie.objects.get(pk=pk)
    return render(request, 'movies/detail_movie.html', {'movie': movie})

