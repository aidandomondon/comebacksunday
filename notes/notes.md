# Notes

## System Overview
[High-level diagram of system](PostsApp.pdf)

## Potential future improvements

### Migrate frontend to ReactJS
Frontend is currently implemented with Django templates. To improve modularity, re-implement the frontend in React
and refactor the backend to use Django Rest Framework (DRF). This will make support for different interfaces (e.g. native mobile apps) possible.

### Move user creation into `registration` app
User creation is more related to logging in/out than routine platform use actions like posting, viewing your feed, etc.

### Standardize redirect message shown when unauthorized user tries to access protected content
- Create a reusable helper that returns a 405 Http response for when an unsupported method is invoked.

### [Move session tracking to separate, dedicated database](https://docs.djangoproject.com/en/5.2/topics/http/sessions/#configuring-the-session-engine)
By default, Django stores user session information on the server-side, on the same database as everything else.
Moving it to its own dedicated database could potentially allow the main database (the one storing user information, posts, etc.) to be read from/written to faster as the quantity of database operations it has to handle would decrease.

### [Switch to Django Rest Framework (DRF)](https://www.django-rest-framework.org)
Currently, the website is set up to use the [default Django auth system](https://docs.djangoproject.com/en/5.2/topics/auth/default/#all-authentication-views). This is session-based, and thus this backend is not RESTful. Pivoting to DRF would make for a RESTful API, which would allow creation + integration of a mobile app or other user interface easier in the future.