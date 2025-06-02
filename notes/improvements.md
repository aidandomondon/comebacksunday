# Potential future improvements

## [1. Move session tracking to separate, dedicated database](https://docs.djangoproject.com/en/5.2/topics/http/sessions/#configuring-the-session-engine)
By default, Django stores user session information on the server-side, on the same database as everything else.
Moving it to its own dedicated database could potentially allow the main database (the one storing user information, posts, etc.) to be read from/written to faster as the quantity of database operations it has to handle would decrease.

## [2. Switch to Django Rest Framework (DRF)](https://www.django-rest-framework.org)
Currently, the website is set up to use the [default Django auth system](https://docs.djangoproject.com/en/5.2/topics/auth/default/#all-authentication-views). This is session-based, and thus this backend is not RESTful. Pivoting to DRF would make for a RESTful API, which would allow creation + integration of a mobile app or other user interface easier in the future.