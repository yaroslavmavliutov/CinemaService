from django.db import models
from django.conf import settings


class Film(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(max_length=1000, null=False)
    genre = models.CharField(max_length=20, null=False)
    premiere_date = models.DateField(null=False)
    session_time = models.TimeField(null=False)
    film_duration = models.IntegerField(null=False)
    price = models.FloatField(null=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        unique_together = ('title', 'session_time')


class Poster(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to='images/', null=False)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pic)

    class Meta:
        unique_together = ('film', 'pic')


class BookedPlace(models.Model):
    film = models.ForeignKey(Film, related_name="tickets", on_delete=models.CASCADE)
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="customer",
        related_name="tickets",
        null=False
    )
    place = models.IntegerField(null=False)
    row = models.IntegerField(null=False)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%d %d' % (self.row, self.place)

    class Meta:
        unique_together = ('film', 'place', 'row')
