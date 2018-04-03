from django.shortcuts import render
from .models import Film, Poster, BookedPlace
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import generics, status
from cinema.serializers import UserSerializer, FilmSerializer, PosterSerializer, FilmListSerializer, BookedPlaceSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import jwt


def index(request):
    """Return the main page"""

    return render(request, 'index.html')


@authentication_classes((JSONWebTokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
class UserListAPIView(generics.ListAPIView):
    """API for getting the list of users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

@permission_classes((AllowAny, ))
class FilmList(APIView):

    def get(self, request, **kwargs):
        """
        :param request: get
        :param kwargs: genre = filtering of list by genre, title = live search by title, without kwargs = all films
        :return: Json with list of films
        """
        if kwargs.items():
            for name, value in kwargs.items():
                if name == 'genre':
                    film = Film.objects.filter(genre=value)
                    serializer = FilmListSerializer(film, many=True)
                    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
                elif name == 'title':
                    film = Film.objects.filter(title__istartswith=value)
                    serializer = FilmListSerializer(film, many=True)
                    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        else:
            film = Film.objects.all()
            serializer = FilmListSerializer(film, many=True)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)



@authentication_classes((JSONWebTokenAuthentication, ))
@permission_classes((IsAuthenticated, IsAdminUser))
def admin_check(request):
    """
    Check wheter user is staff or no
    :param request: get
    :return: response with the value of parameter isAdmin (True/False)
    """
    jwts = request.META['HTTP_AUTHORIZATION'][4:]
    jwt_decoded = jwt.decode(jwts, 'secret', algorithms=['HS256'], verify=False)
    curr_user = User.objects.filter(username=jwt_decoded['username'])[0]
    content = {
        'isAdmin': curr_user.is_staff  # `django.contrib.auth.User` instance.
    }
    if curr_user.is_staff:
        return JsonResponse(content)
    else:
        return HttpResponse(status=403)


@csrf_exempt
def reg_form(request):
    """
    Register new user
    :param request: POST
    :return: Json with information of new user, add new user record to database
    """
    if request.method == 'GET':
        return render(request, 'register.html')

    if request.method == 'POST':
        serializer = UserSerializer(data=request.POST)
        if serializer.is_valid():
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'], email=request.POST['email'])
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors)


class FilmDetail(APIView):

    @authentication_classes((JSONWebTokenAuthentication,))
    @permission_classes((IsAuthenticated, IsAdminUser))
    def post(self, request):
        """
        Add new film to database (only for privileged users, is_staff=True)
        :param request: POST
        :return: Json with fields of new film
        """
        jwts = request.META['HTTP_AUTHORIZATION'][4:]
        jwt_decoded = jwt.decode(jwts, 'secret', algorithms=['HS256'], verify=False)
        curr_user = User.objects.filter(username=jwt_decoded['username'])[0]
        print(request.FILES)
        if curr_user.is_staff:
            serializer = FilmSerializer(data=request.POST)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse(serializer.errors)
        else:
            return HttpResponse(status=403)

    def get_object(self, id):
        """
        Get film with definite id
        :param id: int
        :return: Film object
        """
        try:
            return Film.objects.filter(id=id)[0]
        except Film.DoesNotExist:
            HttpResponse(status=404)

    def get(self, request, id):
        """
        Get detail of film
        :param request: GET
        :param id: int
        :return: Json with information of film
        """
        film = self.get_object(id)
        serializer = FilmSerializer(film, many=False)
        return JsonResponse(serializer.data, safe=False)

    def put(self, request, id):
        """
        Update information of film
        :param request: PUT
        :param id: int
        :return: Json with new film information (update information in database)
        """
        film = self.get_object(id)
        serializer = FilmSerializer(film, data=request.PUT)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return JsonResponse(serializer.errors)

    def delete(self, request, id):
        """
        Delete chosen film
        :param request: DELETE
        :param id: int
        :return: Json with HTTP_204 response
        """
        poster = self.get_object(id)
        poster.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class PosterList(APIView):

    @authentication_classes((JSONWebTokenAuthentication,))
    @permission_classes((IsAuthenticated, IsAdminUser))
    def post(self, request):
        """
        Add new posters to chosen film
        :param request: POST
        :return: Json with message (add images to database)
        """
        print(request.FILES)
        try:
            film = Film.objects.filter(title=request.POST['title'])[0]
        except Film.DoesNotExist:
            return HttpResponse(status=404)
        Poster.objects.create(film=film, pic=request.FILES['file'])
        response_dict = {
            'message': 'Poster uploaded successfully!',
        }
        return JsonResponse(response_dict)

    def get(self, request, id):
        """
        Get poster from database
        :param request: GET
        :param id: int (id of film)
        :return: Json with links on posters
        """
        film = self.get_object(id)
        serializer = PosterSerializer(Poster.objects.filter(film=film), many=True)
        return JsonResponse(serializer.data, safe=False)

    def get_object(self, id):
        """
        Get poster from database
        :param id: int (id of poster)
        :return: Poster instance
        """
        try:
            return Poster.objects.filter(id=id)
        except Poster.DoesNotExist:
            HttpResponse(status=404)

    def put(self, request, id):
        """
        Change poster fields
        :param request: PUT
        :param id: int (id of poster)
        :return: Json with informaton of updated Poster instance
        """
        poster = self.get_object(id)
        serializer = PosterSerializer(poster, data=request.PUT)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return JsonResponse(serializer.errors)

    def delete(self, request, id):
        """
        Delete poster from database
        :param request: DELETE
        :param id: int (id of poster)
        :return: HTTP_204 response
        """
        poster = self.get_object(id)
        poster.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class BookedPlaceView(APIView):


    def get(self, request, **kwargs):
        """
        Get booked places: for film if parameter is film_id and for user if parameter is id
        :param request: GET
        :param kwargs: film_id or id
        :return: Json with booked places
        """
        for name, value in kwargs.items():
            if name == 'film_id':
                order = BookedPlace.objects.filter(film__id=value)
                serializer = BookedPlaceSerializer(order, many=True)
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
            elif name == 'id':
                order = BookedPlace.objects.filter(author__id=value)
                serializer = BookedPlaceSerializer(order, many=True)
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

    def get_item(self, id):
        """
        Get BookedPlace instance
        :param id: int (id of order)
        :return: BookedPlace instance
        """
        try:
            return BookedPlace.objects.get(id=id)
        except BookedPlace.DoesNotExist:
            return HttpResponse(status=404)


    @csrf_exempt
    def post(self, request):
        """
        Book the place
        :param request: POST
        :return: HTTP_201 response
        """
        post_data = request.POST.copy()
        print(post_data)
        BookedPlace.objects.create(film=Film.objects.get(id=post_data['film']), customer=User.objects.get(username=request.POST['customer']), place=post_data['place'], row=post_data['row'])
        return HttpResponse(status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        """
        Delete order
        :param request: DELETE
        :param id: int (id of order)
        :return: HTTP_204 response
        """
        place = self.get_item(id)
        place.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


@permission_classes((AllowAny, ))
class FilmBookPage(APIView):

    def get(self, request, id):
        """
        Show detail page for film instance
        :param request: GET
        :param id: int (id of film)
        :return: rendered HTML page with information about film and form for booking the places
        """
        film = Film.objects.get(id=id)
        return render(request,'detail.html', {'film': film})



