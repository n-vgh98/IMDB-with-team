from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import MovieForm
from .models import *


def movies_list(request):
    movies = Movie.objects.filter(is_valid=True)
    return render(request, 'movies/index.html', {'movies': movies})


def movie_detail(request, pk):
    movie = Movie.objects.get(pk=pk)
    return render(request, 'movies/detail_movie.html', {'movie': movie})


def add_movie(request):
    if request.method == 'GET':
        form = MovieForm()
        return render(request, 'movies/add_movie_form.html', {'form': form})
    elif request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('movies_list')
        else:
            form = MovieForm()
            return render(request, 'movies/add_movie_form.html', {'form': form})
