from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from django.db.models import Avg


class Genre(models.Model):
    title = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Role(models.Model):
    title = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Crew(models.Model):
    MALE = 1
    FEMALE = 2
    GENDER_CHOICES = (
        (MALE, ' male'),
        (FEMALE, 'female')
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField(null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, default=MALE)
    avatar = models.ImageField(upload_to='crew/avatars/', null=True, blank=True)
    is_valid = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} : {self.last_name}'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='movies/avatars/', null=True, blank=True)
    genres = models.ManyToManyField(Genre)
    crew = models.ManyToManyField(Crew, through='MovieCrew')
    is_valid = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def rate(self):
        avg_rate = self.movie_rate.all().aggregate(avg=Avg('rate'))
        return avg_rate.get('avg') or 1


class MovieCrew(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('movie', 'crew', 'role')


class AbstaractComment(models.Model):
    CREATED = 10
    REJECTED = 20
    APPROVED = 30
    DELETED = 40
    STATUS_CHOISES = (
        (CREATED, "CREATED"),
        (REJECTED, "REJECTED"),
        (APPROVED, "APPROVED"),
        (DELETED, "DELETED")
    )

    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comment")
    comment_body = models.TextField()
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOISES, default=CREATED)
    validated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name="validated_by")
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MovieComment(AbstaractComment):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie_comments")


class AbstractRate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rate_user')
    rate = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MovieRate(AbstractRate):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_rate')

    class Meta:
        constraints = [models.UniqueConstraint(fields=('user', 'movie'), name='unique_user_movie_rate')]
