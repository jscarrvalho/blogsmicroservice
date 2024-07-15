# Blog Posts Microservice

## This is a simple one-resource REST API under 8000 port.

After running the application you can read the documentation at:

http://localhost:8000/swagger <br />
http://localhost:8000/redoc


## Project details and design decisions

Django Rest Framework web application built only with Python. There are just 4 routes: <br />
http://localhost:8000/blogs (GET, POST) <br />
http://localhost:8000/blogs/{id} (GET, PUT, PATCH, DELETE) <br />
http://localhost:8000/auth/signup (POST) <br />
http://localhost:8000/auth/signin (POST) <br />

Signup and signin routes, given a username and password, returns a token to be used in data manipulation (POST, PUT, PATCH and DELETE verbs), usage in authorization header (Ex.: Authorization: Token [given token]). <br /> <br />
In route http://localhost:8000/blogs/{id}, data manipulation verbs (PUT, PATCH and DELETE) only can be performed by the owner (Token who created the blog post). <br /> <br />
To list all blog posts or get a specific one are public (Don't need the authorization token) <br /> <br />
The microservice uses the 'never delete' strategy. DELETE verb only updates the database with deleted_at datetime. On listing, only the rows with deleted_at NULL are selected.<br /> <br />

This is all you have to know about the project, don't worry about run it, it's dockerized!

## Run

### With docker compose

1 - Download (or clone) the project files and put into a target folder.<br />
2 - Go to the target folder.<br />
3 - Run `docker compose up --build -d`.<br />
4 - Go to http://localhost:8000/redoc or http://localhost:8000/swagger.<br />

### OR <br />

### Without docker

1 - Provide your own mysql service and the respective user ([mysqluser]) for the application.

2 - Download (or clone) the project files and put into a target folder.<br />
3 - Go to the target folder > blogsmicroservice/.<br />
4 - Run `pip install -r requirements.txt`.<br />
5 - Go back to the target folder `cd ..`.<br />
6 - Run `export DB_HOST=[hostname] DB_NAME=[dbname] DB_USER=[mysqluser] DB_PASSWORD=[mysqluserpass]`<br />
7 - Run `python manage.py init_db`.<br />
8 - Run `python manage.py migrate`.<br />
9 - Run `python manage.py runserver 0.0.0.0:8000`.<br />
10 - Go to http://localhost:8000/redoc or http://localhost:8000/swagger.<br />

## Future features / improvements

Usage feature: include an organic field called 'tags' for the user to classify their posts with keywords. Further ahead, a supervised machine learning can be implemented to classify automatically the blog posts.<br />
Usage feature: include comments to each blog post.<br />
Usage feature: include reactions (like, love, hate, dislike) to each blog post.<br />
Security improvement: change token to expire in x hours and allow refresh token lifetime. (Current implementation allows each user to use their unique fixed token with no expiration time).<br />
