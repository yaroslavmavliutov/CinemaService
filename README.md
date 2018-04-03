# CinemaService
Service for cinema that allows you:
 - Register new User
 - JSON Web Token Authorization (saved in local storage)
 - Add/Edit/Delete/Get new films with posters (drag-n-drop for posters)
 - Add/Delete/Get booked places for every film or/and every user
 - Filter films by genre. Live search by title
 
 Available API:
  - api/v1/auth/login/ - method:POST - obtain new JSON Web Token
  - api-token-verify/ - method:POST - verify token
  - users/ - method:GET - get all registered users
  - admin_check/ - method:GET - check whether user is staff (based on web token)
  - reg_form/ - method:POST - register new user
  - film_list/ - method:GET - get film list 
  - film_list/filter/(?P<genre>.+)/ - method:GET - get films with definite genre
  - film_list/(?P<title>.+) - method:GET - live search for films (title)
  - user_bookings/film/(?P<film_id>[0-9]+)/ - method:GET - get all bookings for definite film
  - user_bookings/ - method:POST/DELETE - add/delete order (book the place)
  - user_bookings/(?P<id>[0-9]+)/ - method:GET - get all bookings for definite user
  - film/(?P<id>[0-9]+)/ - method:GET - get film detail
  - film/ - method:POST/PUT/DELETE - add/change/delete new film
  - poster/(?P<id>[0-9]+)/ - method:GET - get poster
  - poster - method:POST/PUT/DELETE - add/change/delete new posters

Form for adding new film - submit two forms at once (one for film, one for poster)

Database models relations:
 - User - one to many - BookedPlace (foreign key)
 - Film - one to many - BookedPlace (foreign key)
 - Film - one to many - Poster (foreign key)

Database: SQLITE

Frameworks: Django (with Django-REST)

Front-end: without frameworks (jQuery)
 
 
