from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .mixins import TimeStampedMixin, UUIDMixin


class FilmWorkType(models.TextChoices):
    MOVIE = 'mov', _('movie')
    TV_SHOW = 'tvs', _('tv show')


class RoleType(models.TextChoices):
    ACTOR = 'actor', _('actor')
    DIRECTOR = 'director', _('director')
    WRITER = 'writer', _('writer')


class Genre(UUIDMixin, TimeStampedMixin):
    """Жанр"""
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self):
        return self.name


class FilmWork(UUIDMixin, TimeStampedMixin):
    """Кинопроизведение"""
    title = models.CharField(_('title'), max_length=100)
    description = models.CharField(_('description'),
                                   max_length=1000, blank=True)
    creation_date = models.DateField(_('creation date'), blank=True, null=True)
    rating = models.FloatField(_('rating'), blank=True,
                               validators=[MinValueValidator(0.0),
                                           MaxValueValidator(10.0)])
    type = models.CharField(_('type'), max_length=32,
                            choices=FilmWorkType.choices)
    genres = models.ManyToManyField(Genre, through='GenreFilmWork')
    file_path = models.FileField(verbose_name=_('file'), blank=True,
                                 null=True, upload_to='movies/')
    persons = models.ManyToManyField('Person', through='PersonFilmWork')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('film work')
        verbose_name_plural = _('film works')
        constraints = [models.Index(fields=['creation_date'],
                                    name='film_work_creation_date_idx'),
                       models.Index(fields=['title'],
                                    name='film_work_title_idx')]

    def __str__(self):
        return self.title


class GenreFilmWork(UUIDMixin):
    """Жанр кинопроизведения"""
    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE,
                                  verbose_name=_('film work'),)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,
                              verbose_name=_('genre'),)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('filmwork genre')
        verbose_name_plural = _('filmwork genres')
        constraints = [models.UniqueConstraint(
            fields=['film_work_id', 'genre_id'],
            name='unique_film_work_genre_idx')]


class Person(UUIDMixin, TimeStampedMixin):
    """Участник"""
    full_name = models.CharField(_('full name'), max_length=100)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('person')
        verbose_name_plural = _('people')
        constraints = [models.Index(fields=['full_name'],
                                    name='person_full_name_idx')]

    def __str__(self):
        return self.full_name


class PersonFilmWork(UUIDMixin):
    """Участники кинопроизведения"""
    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE,
                                  verbose_name=_('film work'),)
    person = models.ForeignKey(Person, on_delete=models.CASCADE,
                               verbose_name=_('person'),)
    role = models.TextField(_('role'), null=True,
                            choices=RoleType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('filmwork person')
        verbose_name_plural = _('filmwork people')
        constraints = [models.UniqueConstraint(
            fields=['film_work_id', 'person_id', 'role'],
            name='unique_film_work_person_role_idx')]
