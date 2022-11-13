from django.contrib import admin
from .models import *


class AdminCrew(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'is_valid')
    search_fields = ('first_name', 'last_name')
    list_filter = ('is_valid',)


class AdminGenre(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_valid')
    search_fields = ('title',)
    list_filter = ('is_valid',)


class AdminMovieCrew(admin.TabularInline):
    model = MovieCrew
    extra = 3
    readonly_fields = ('crew_gender',)

    def crew_gender(self, obj):
        return obj.crew.get_gender_display()

class AdminMovieGenre(admin.StackedInline):
    model = Movie.genres.through
    extra = 3


class AdminMovie(admin.ModelAdmin):
    list_display = ('id', 'title', 'release_date', 'is_valid')
    search_fields = ('title',)
    list_filter = ('is_valid',)
    inlines = (AdminMovieCrew, AdminMovieGenre)


class AdminRole(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_valid')
    search_fields = ('title',)
    list_filter = ('is_valid',)


admin.site.register(Movie, AdminMovie)
admin.site.register(Crew, AdminCrew)
admin.site.register(Role, AdminRole)
admin.site.register(Genre, AdminGenre)
