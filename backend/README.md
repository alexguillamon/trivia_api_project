# The Trivia API Project

This project is a trivia api that powers a frontend game of trivia. The goal of this project is two fold:

1. To create a great easy to use API that handles request efficiently and error gracefully.
2. To learn and apply my skills as a Full Stack Developer by accomplishing goal 1.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

## Getting Started

### Pre-requisites and Local Development

You will need `python`, `pip`, `node`, and `postgresql` installed in your local machine in order to run this project.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```
psql trivia < trivia.psql
```

#### Backend

If you don't have `pipenv` installed yet you can do so by running the following command `pip install pipenv`

We use `pipenv` as our virtual environment and dependency manager of choice but you are welcomed to use your preferred one.

From the backend folder run `pipenv shell`. This will create a new virtual environment and install all the needed dependencies listed in the Pipfile.

To run the application run the following commands in your environment :

```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

The application will run on `http://127.0.0.1:5000/`

#### Frontend

From the frontend folder, run the following commands to start the client:

```
npm i
npm start
```

By default, the frontend will run on localhost:3000.

### Testing

In order to run the test you will need to run the following commands from the `/backend` folder:

```
dropdb trivia_test //ommit when running for the first time
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Reference

### Getting Started

- Base URL: At present this app is not deployed to a remote server and can only be run locally. The base url for the API is `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable
- 500: Internal Server Error

### Endpoints

### GET `/categories`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
- Request:
  `curl http://127.0.0.1:5000/categories`
- Response:
  ```
  {
      '1' : "Science",
      '2' : "Art",
      '3' : "Geography",
      '4' : "History",
      '5' : "Entertainment",
      '6' : "Sports"
  }
  ```

### GET `/questions`

- Fetches a list questions. This list of questions can be fetched by page (fetching from all the available questions) or by search term which returns only the questions containing a the search term as a substring. When fetching a list of questions the list will be paginated 10 at a time.
- Request Arguments:

  - Optional:

    ```
    ?page=<int:page_number>
    ```

    ```
    ?search_term=<str:search_term>
    ```

- Returns: An list of questions together with the same object returned by `get /categories`

- Request:

  ```
  curl http://127.0.0.1:5000/questions
  ```

  - Note: `page` argument will default to 1

  ```
  curl http://127.0.0.1:5000/questions?page=3
  ```

- Response:

  ```
  {
      "categories": {
          "1": "Science",
          "2": "Art",
          "3": "Geography",
          "4": "History",
          "5": "Entertainment",
          "6": "Sports"
      },
      "current_category": 0,
      "current_page": 1,
      "questions": [
          {
          "answer": "Maya Angelou",
          "category": 4,
          "difficulty": 2,
          "id": 5,
          "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
          },
          {
          "answer": "Muhammad Ali",
          "category": 4,
          "difficulty": 1,
          "id": 9,
          "question": "What boxer's original name is Cassius Clay?"
          },
          {
          "answer": "Apollo 13",
          "category": 5,
          "difficulty": 4,
          "id": 2,
          "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
          },
          {
          "answer": "Tom Cruise",
          "category": 5,
          "difficulty": 4,
          "id": 4,
          "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
          },
          ...
      ],
      "success": true,
      "total_questions": 19
  }
  ```

  - Request:
    `curl http://127.0.0.1:5000/questions?search_term=world`

  - Response:

  ```
  {
      "current_category": 1,
      "questions": [
      {
          "answer": "Brazil",
          "category": 6,
          "difficulty": 3,
          "id": 10,
          "question": "Which is the only team to play in every soccer World Cup tournament?"
      },
      {
          "answer": "Uruguay",
          "category": 6,
          "difficulty": 4,
          "id": 11,
          "question": "Which country won the first ever soccer World Cup in 1930?"
      }
      ],
      "search_term": "world",
      "success": true,
      "total_questions": 2
  }
  ```

#### GET /books

- General:
  - Returns a list of book objects, success value, and total number of books
  - Results are paginated in groups of 8. Include a request argument to choose page number, starting from 1.
- Sample: `curl http://127.0.0.1:5000/books`

```{
  "books": [
    {
      "author": "Stephen King",
      "id": 1,
      "rating": 5,
      "title": "The Outsider: A Novel"
    },
    {
      "author": "Lisa Halliday",
      "id": 2,
      "rating": 5,
      "title": "Asymmetry: A Novel"
    },
    {
      "author": "Kristin Hannah",
      "id": 3,
      "rating": 5,
      "title": "The Great Alone"
    },
    {
      "author": "Tara Westover",
      "id": 4,
      "rating": 5,
      "title": "Educated: A Memoir"
    },
    {
      "author": "Jojo Moyes",
      "id": 5,
      "rating": 5,
      "title": "Still Me: A Novel"
    },
    {
      "author": "Leila Slimani",
      "id": 6,
      "rating": 5,
      "title": "Lullaby"
    },
    {
      "author": "Amitava Kumar",
      "id": 7,
      "rating": 5,
      "title": "Immigrant, Montana"
    },
    {
      "author": "Madeline Miller",
      "id": 8,
      "rating": 5,
      "title": "CIRCE"
    }
  ],
"success": true,
"total_books": 18
}
```

#### POST /books

- General:
  - Creates a new book using the submitted title, author and rating. Returns the id of the created book, success value, total books, and book list based on current page number to update the frontend.
- `curl http://127.0.0.1:5000/books?page=3 -X POST -H "Content-Type: application/json" -d '{"title":"Neverwhere", "author":"Neil Gaiman", "rating":"5"}'`

```
{
  "books": [
    {
      "author": "Neil Gaiman",
      "id": 24,
      "rating": 5,
      "title": "Neverwhere"
    }
  ],
  "created": 24,
  "success": true,
  "total_books": 17
}
```

#### DELETE /books/{book_id}

- General:
  - Deletes the book of the given ID if it exists. Returns the id of the deleted book, success value, total books, and book list based on current page number to update the frontend.
- `curl -X DELETE http://127.0.0.1:5000/books/16?page=2`

```
{
  "books": [
    {
      "author": "Gina Apostol",
      "id": 9,
      "rating": 5,
      "title": "Insurrecto: A Novel"
    },
    {
      "author": "Tayari Jones",
      "id": 10,
      "rating": 5,
      "title": "An American Marriage"
    },
    {
      "author": "Jordan B. Peterson",
      "id": 11,
      "rating": 5,
      "title": "12 Rules for Life: An Antidote to Chaos"
    },
    {
      "author": "Kiese Laymon",
      "id": 12,
      "rating": 1,
      "title": "Heavy: An American Memoir"
    },
    {
      "author": "Emily Giffin",
      "id": 13,
      "rating": 4,
      "title": "All We Ever Wanted"
    },
    {
      "author": "Jose Andres",
      "id": 14,
      "rating": 4,
      "title": "We Fed an Island"
    },
    {
      "author": "Rachel Kushner",
      "id": 15,
      "rating": 1,
      "title": "The Mars Room"
    }
  ],
  "deleted": 16,
  "success": true,
  "total_books": 15
}
```

#### PATCH /books/{book_id}

- General:
  - If provided, updates the rating of the specified book. Returns the success value and id of the modified book.
- `curl http://127.0.0.1:5000/books/15 -X PATCH -H "Content-Type: application/json" -d '{"rating":"1"}'`

```
{
  "id": 15,
  "success": true
}
```

## Deployment N/A

## Authors

Yours truly, Coach Caryn

## Acknowledgements

The awesome team at Udacity and all of the students, soon to be full stack extraordinaires!
