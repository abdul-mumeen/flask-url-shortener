# flask-url-shortener
[![Build Status](https://travis-ci.org/andela-aolasode/flask-url-shortener.svg?branch=develop)](https://travis-ci.org/andela-aolasode/flask-url-shortener)
[![Coverage Status](https://coveralls.io/repos/github/andela-aolasode/flask-url-shortener/badge.svg?branch=develop)](https://coveralls.io/github/andela-aolasode/flask-url-shortener?branch=develop)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/andela-aolasode/flask-url-shortener/badges/quality-score.png?b=develop)](https://scrutinizer-ci.com/g/andela-aolasode/flask-url-shortener/?branch=develop)
[![Code Health](https://landscape.io/github/andela-aolasode/flask-url-shortener/develop/landscape.svg?style=flat)](https://landscape.io/github/andela-aolasode/flask-url-shortener/develop)

### Table of Content
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [API Resource Endpoints](#api-resource-endpoints)
4. [Usage](#usage)
5. [Other Features](#other-features)
6. [Running Tests](#running-tests)
7. [Built With](#built-with)
8. [Limitations](#limitations)
9. [Authors](#authors)
10. [Acknowledgments](#acknowledgments)
11. [Project Demo](#project-demo)

### <a name="introduction"></a>Introduction
Flask-url-shortener is a REST API that allows users to shorten long, ugly URLs into nicely formatted short URLs that can be customized using a user's vanity string of choice. Endpoints can be accessed through token based authentication which token can be gotten by the user through basic authentication (email and password).

### <a name="installation"></a>Installation
1. Clone the repo `$ git clone https://github.com/andela-aolasode/flask-url-shortener.git`.
2. Navigate to the project folder downloaded.
3. Create and activate a virtual environment.
4. Install dependencies  `$ pip install -r requirements.txt`
5. Run the migration script to setup database:
    * Create migrations by running `$ python manage.py db migrate`.
    * Apply migrations with `$ python manage.py db upgrade`.
6. Run the server using `$ python manage.py runserver`.

### <a name="api-resource-endpoints"></a>API Resource Endpoints
| EndPoint                             | Functionality                                | Public Access |
| ------------------------------------ | -------------------------------------------- | ------ |
| POST /register                       | Register a user                              | TRUE   |
| GET  /token                          | Return a token                               | TRUE   |
| POST /shorten                        | Return a shortened URL                       | FALSE  |
| GET  /shorturl/                      | Get a list of user's shortened URLs          | FALSE  |
| GET /shorturl/recent                 | Get a list of recently shortened URLs        | FALSE  |
| GET /shorturl/id                     | Get a single shortened URL                   | FALSE  |
| DELETE /shorturl/id                  | Delete a single shortened URL                | FALSE  |
| PUT /shorturl/id                     | Change the target of a shortened URL         | FALSE  |
| PUT /shorturl/id/activate            | Activate a shortened URL                     | FALSE  |
| PUT /shorturl/id/deactivate          | Deactivate a shortened URL                   | FALSE  |
| GET /shorturl/popular                | Get a list of popular shortened URLs         | FALSE  |
| GET /shorturl/id/visitors/           | Get a list of visitors to a shortened URLs   | FALSE  |
| GET /shorturl/id/visitors/vid        | Get details of a visitor to a shortened URLs | FALSE  |
| POST /visit                          | Get the long URL of a short URL              | FALSE  |
| GET /users/influential               | Get a list of influential users              | FALSE  |
| GET /user                            | Get the details of a user                    | FALSE  |

### <a name="usage"></a>Usage
Its important to state here again that the two means of authentication (i.e Basic Auth and Token Auth) must be passed into the request header.

1. To create a new user on the api:
    Input:
    ```cmd
    curl -i -X POST -H "Content-Type: application/json" -d '{"first_name":"rikky", "last_name":"Ngozi", "email":"ngozi@andela.com", "password":"python", "confirm_password":"python"}' http://frus.herokuapp.com/api/v1.0/register
    ```
    Output:
    ```cmd
    {
      "message": "User creation successful",
      "success": true
    }
    ```


2. To get token:
    Input:
    ```cmd
    url -u ngozi@andela.com:python http://frus.herokuapp.com/api/v1.0/token
    ```
    Output:
    ```
    {
      "expiration": 3600,
      "token": "eyJhbGciOiJIUzI1NiIsImlhdCI6MTQ5MzExMDQzMCwiZXhwIjoxNDkzMTE0MDMwfQ.eyJ1c2VyX2lkIjozfQ.NvL9u4eAO4iKB8pT501mk-BXx4Kq3p9gcTU83s23Nwo"
    }
    ```
    **NOTE:** The token needs to be attached to subsequent calls in order to access restricted resources.

3. Shorten a long URL:
    Input:
    ```
    curl -i -X POST -H '{"Authorization: Token eyJhbGciOiJIUzI1NiIsImlhdCI6MTQ5MzExMDQzMCwiZXhwIjoxNDkzMTE0MDMwfQ.eyJ1c2VyX2lkIjozfQ.NvL9u4eAO4iKB8pT501mk-BXx4Kq3p9gcTU83s23Nwo", "Content-Type: application/json"}' -d '{"long_url":"http://www.andela.com"}' http://frus.herokuapp.com/api/v1.0/shorten
    ```
    Output:
    ```
    {
      "success": true,
      "url": {
        "long_url": "http://www.andela.com",
        "number_of_visits": 0,
        "short_url": "https://www.frus.herokuapp.com/TSi4Q",
        "short_url_url": "http://frus.herokuapp.com/api/v1.0/shorturl/1",
        "visitors": []
      }
    }
    ```

4. Get a list of user's shortened URLs:
    Input:
    ```cmd
    curl -i -X GET -H '{"Authorization: Token eyJhbGciOiJIUzI1NiIsImlhdCI6MTQ5MzExMDQzMCwiZXhwIjoxNDkzMTE0MDMwfQ.eyJ1c2VyX2lkIjozfQ.NvL9u4eAO4iKB8pT501mk-BXx4Kq3p9gcTU83s23Nwo", "Content-Type: application/json"}' http://frus.herokuapp.com/api/v1.0/shorturl/
    ```
    Output:
    ```
    {
      "success": true,
      "urls": [
        {
          "long_url": "http://www.andela.com",
          "number_of_visits": 0,
          "short_url": "https://www.frus.herokuapp.com/TSi4Q",
          "short_url_url": "http://frus.herokuapp.com/api/v1.0/shorturl/1",
          "visitors": []
        },
        {
          "long_url": "http://www.google.com",
          "number_of_visits": 0,
          "short_url": "https://www.frus.herokuapp.com/TSiV7Q",
          "short_url_url": "http://frus.herokuapp.com/api/v1.0/shorturl/2",
          "visitors": []
        }
      ]
      }
    }
    ```

5. Get a list of recently shortened URLs:
    Input:
    ```cmd
    curl -i -X GET -H '{"Authorization: Token eyJhbGciOiJIUzI1NiIsImlhdCI6MTQ5MzExMDQzMCwiZXhwIjoxNDkzMTE0MDMwfQ.eyJ1c2VyX2lkIjozfQ.NvL9u4eAO4iKB8pT501mk-BXx4Kq3p9gcTU83s23Nwo", "Content-Type: application/json"}' http://frus.herokuapp.com/api/v1.0/shorturl/recent
    ```
    Output:
    ```
    {
      "success": true,
      "recents": [
        {
          "long_url": "http://www.google.com",
          "number_of_visits": 0,
          "short_url": "https://www.frus.herokuapp.com/TSiV7Q",
          "short_url_url": "http://frus.herokuapp.com/api/v1.0/shorturl/2",
          "visitors": []
        },
        {
          "long_url": "http://www.andela.com",
          "number_of_visits": 0,
          "short_url": "https://www.frus.herokuapp.com/TSi4Q",
          "short_url_url": "http://frus.herokuapp.com/api/v1.0/shorturl/1",
          "visitors": []
        }
      ]
      }
    }
    ```

6. Delete a shortened URL:
    Input:
    ```cmd
    curl -i -X DELETE -H '{"Authorization: Token eyJhbGciOiJIUzI1NiIsImlhdCI6MTQ5MzExMDQzMCwiZXhwIjoxNDkzMTE0MDMwfQ.eyJ1c2VyX2lkIjozfQ.NvL9u4eAO4iKB8pT501mk-BXx4Kq3p9gcTU83s23Nwo", "Content-Type: application/json"}' http://frus.herokuapp.com/api/v1.0/shorturl/1
    ```
    Output:
    ```
    {
      "success": true,
      "message": "Deleted"
    }
    ```

7. Change shortened URL target long_url:
Input:
    ```cmd
    curl -i -X PUT -H '{"Authorization: Token eyJhbGciOiJIUzI1NiIsImlhdCI6MTQ5MzExMDQzMCwiZXhwIjoxNDkzMTE0MDMwfQ.eyJ1c2VyX2lkIjozfQ.NvL9u4eAO4iKB8pT501mk-BXx4Kq3p9gcTU83s23Nwo", "Content-Type: application/json"}' -d '{"http://www.flask-url-shortener.com"}' http://frus.herokuapp.com/api/v1.0/shorturl/2
    ```
    Output:
    ```
    {
      "success": true,
      "message": "Updated"
    }
    ```

8. Get user details
    Input:
    ```cmd
    curl -i -X GET -H '{"Authorization: Token eyJhbGciOiJIUzI1NiIsImlhdCI6MTQ5MzExMDQzMCwiZXhwIjoxNDkzMTE0MDMwfQ.eyJ1c2VyX2lkIjozfQ.NvL9u4eAO4iKB8pT501mk-BXx4Kq3p9gcTU83s23Nwo", "Content-Type: application/json"}' http://frus.herokuapp.com/api/v1.0/shorturl/recent
    ```
    Output:
    ```
    {
      "success": true,
      "user": {
        "email": "erika@andela.com",
        "first_name": "Erika",
        "last_name": "Dike",
        "short_urls": [
          "http://frus.herokuapp.com/api/v1.0/shorturl/4"
        ]
      }
    }
    ```

### <a name="running-tests"></a>Running Tests
1. Navigate to the project directory.
2. Run `python manage.py test` to run test and check coverage.

### <a name="built-with"></a>Built With
* [Flask](http://flask.pocoo.org/) - Flask is a BCD licensed microframework for Python based on Werkzeug and Jinja 2.
* [Flasl-HTTPAuth](https://flask-httpauth.readthedocs.io/en/latest/) - This is a simple extension that simplifies the use of HTTP authentication with Flask routes.
* [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) - This an extension that handles SQLAlchemy database migrations for Flask applications using Alembic. The database operations are made available through the Flask command-line interface.
* [Flask-Script](https://flask-script.readthedocs.io/en/latest/) - This extension provides support for writing external scripts in Flask. This includes running a development server, a customized Python shell, scripts to set up a database and other command-line tasks that belong outside the web application itself.
* [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/) - This extension help to simplify using SQLAlchemy with Flask by providing useful defaults and extra helpers that make it easier to accomplish common tasks.
* [Flask-WTF (Validator)](http://wtforms.readthedocs.io/en/latest/validators.html) - This a WTForms class that simply takes an input, verifies it fulfills some criterion, such as a maximum length for a string and returns. Or, if the validation fails, raises a ValidationError.
* [Flask-Inputs](http://pythonhosted.org/Flask-Inputs/) - This extension adds support for WTForms to validate request data from args to headers to json.
* [Python-Env](https://github.com/mattseymour/python-env) - This library allows the saving of environment variables in .env and loaded when the application runs.
* [Nose](https://pypi.python.org/pypi/nose/1.3.7) - The python framework that extends the test loading and running features of unittest, making it easier to write, find and run tests.

### <a name="limitations"></a>Limitations
One obvious limitation to this project is that the shortened URL can be longer than the long URL supplied since the app is curren hosted on Heroku and the domain name given by Heroku is long.

### <a name="authors"></a>Authors
* **Olasode Adeyemi Abdul-Mumeen** - *Software Developer at Andela*

### <a name="acknowledgments"></a>Acknowledgments
* My gratitude goes to the following people;
1. **Njira Percila** for  being a great facilitator and an icon to emulate in terms of doing it the right way.
2. **Ichiato Ikinkin**, **Koya Adegboyega**, **Durodola Damilola**, **Bolaji Olajide** and **Oladipupo Adeniran** for being a wonderful teammates giving good ideas and support.
3. **Hassan Oyeboade**, **Kola Erinoso** and **Chukwuerika Dike** for their mentoring during the development of this project.

### <a name="project-demo"></a>Project Demo
Click [here](https://www.youtube.com/watch?v=OWKAxiGB1RA&feature=youtu.be) to view the project demo
