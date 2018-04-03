from django.contrib.auth.models import User
from .models import Film, Poster, BookedPlace
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    tickets = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email','tickets')


class FilmSerializer(serializers.ModelSerializer):
    tickets = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Film
        fields = ('id', 'title', 'description', 'genre', 'premiere_date', 'session_time', 'film_duration', 'price',
                  'tickets')


class PosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poster
        fields = ('film', 'pic', 'is_main')


class FilmListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100)
    genre = serializers.CharField(max_length=20)
    premiere_date = serializers.DateField()
    session_time = serializers.TimeField()
    film_duration = serializers.IntegerField()
    tickets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    price = serializers.FloatField()
    poster = serializers.ImageField(default=None)

    def to_representation(self, obj):
        serialized_data = super(FilmListSerializer, self).to_representation(obj)

        try:
            serialized_data['poster'] = str(Poster.objects.get(is_main=True, film=obj).pic)
        except:
            serialized_data['poster'] = None
        return serialized_data


class BookedPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookedPlace
        fields = ('place', 'row')
