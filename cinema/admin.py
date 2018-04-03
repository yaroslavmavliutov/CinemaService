from django.contrib import admin
from .models import Film, Poster, BookedPlace


class FilmAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'genre', 'premiere_date', 'session_time', 'film_duration', 'price')


class PosterAdmin(admin.ModelAdmin):
    list_display = ('film', 'pic')


class BookedPlaceAdmin(admin.ModelAdmin):
    list_display = ('film', 'customer', 'place', 'row', 'booking_date')


admin.site.register(Film, FilmAdmin)
admin.site.register(Poster, PosterAdmin)
admin.site.register(BookedPlace, BookedPlaceAdmin)