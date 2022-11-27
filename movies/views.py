from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import MovieForm, CommentForm
from .models import *


def movies_list(request):
    movies = Movie.objects.filter(is_valid=True)
    return render(request, 'movies/index.html', {'movies': movies})


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    genres = movie.genres.all()
    movie_crew = MovieCrew.objects.filter(movie=movie).select_related('crew', 'role')
    directors = []
    writers = []
    actors = []
    for crew in movie_crew:
        if crew.role.title == 'director':
            directors.append(crew.crew.full_name)
        elif crew.role.title == 'Writer':
            writers.append(crew.crew.full_name)
        elif crew.role.title == 'actor':
            actors.append(crew.crew.full_name)
    movie_comments = movie.movie_comments.all().filter(status='30')
    form = CommentForm(request.POST)
    if request.method == 'POST':
        if request.user.is_authenticated:
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.movie = movie
                comment.save()
                form = CommentForm()
            else:
                form = CommentForm()
        else:
            return redirect('login')
    else:
        form = CommentForm()

    return render(request, 'movies/detail_movie.html', {
        'movie': movie,
        'form': form,
        'movie_comments': movie_comments,
        'directors': directors,
        'writers': writers,
        'actors': actors,
        'genres': genres,
    })


@login_required
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


@login_required
def edit_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'GET':
        form = MovieForm(instance=movie)
        context = {
            'form': form,
            'movie': movie
        }
        return render(request, 'movies/edit_movie_form.html', context=context)
    elif request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            context = {
                'form': form,
                'movie': movie
            }
            return redirect('movie_detail', pk=pk)
        else:
            form = MovieForm(instance=movie)
            context = {
                'form': form,
                'movie': movie
            }
            return render(request, 'movies/edit_movie_form.html', context=context)


@login_required
def delete_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    movie.is_valid = False
    movie.save()

    return redirect('movies_list')



def rate_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk, is_valid=True)
    MovieRate.objects.update_or_create(
        movie=movie,
        user=request.user,
        defaults={'rate': int(request.POST.get('rate'))})
    return redirect('movies_list')
