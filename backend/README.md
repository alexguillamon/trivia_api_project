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

#### GET `/categories`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
- Request:
  ```
  curl http://127.0.0.1:5000/categories
  ```
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

#### GET `/questions`

- Fetches a list questions. This list of questions can be fetched by page (fetching from all the available questions) or by search term which returns only the questions containing a the search term as a substring. When fetching a list of questions the list will be paginated 10 at a time.
- Request Arguments:

  - Optional:

    ```
    ?page=<int:page_number>
    ```

    ```
    ?search_term=<str:search_term>
    ```

- Returns a list of questions together with the same object returned by `get /categories`

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

  ```
  curl http://127.0.0.1:5000/questions?search_term=world
  ```

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

#### POST `/questions`

- Creates a new question using the submitted question, answer, difficulty, and category. using the submitted title, author and rating.
- The request body should be a JSON object and come in the following schema:

  ```
  {
      "question": {"type": "string"},
      "answer": {"type": "string"},
      "difficulty": {"type": "integer"},
      "category": {"type": "integer"},
  }
  ```

  - Note: all fields are required or else an error response will be returned

- Returns an JSON object:
  ```
  {
      "answer": String,
      "category": Int,
      "difficulty": Int,
      "id": Int,
      "question": String,
      "success": Boolean
  }
  ```
- Request:
  ```
  curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"who am I?", "answer":"Alejandro", "difficulty":2, "category":1}'
  ```
- Response:
  ```
  {
      "answer": "Alejandro",
      "category": 1,
      "difficulty": 2,
      "id": 25,
      "question": "who am I?",
      "success": true
  }
  ```

#### DELETE `/questions/{int:question_id}`

- Deletes the question matching the id provided else returns a 404 error. Returns the `question_id` of the deleted question.

- Request:
  ```
  curl -X DELETE http://127.0.0.1:5000/questions/25
  ```
- Response:
  ```
  {
    "question_id": 25,
    "success": true
  }
  ```

#### GET `/categories/{int:category_id}/questions`

- Fetches a list of questions within the requested category.

- Request:
  ```
  curl -X GET http://127.0.0.1:5000/categories/2/questions
  ```
- Response:
  ```
  {
    "current_category": 2,
    "questions": [
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
        },
            {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        }
    ],
    "success": true,
    "total_questions": 4,
    "type": "Art"
  }
  ```

#### POST `/quizzes`

- Fetches a new random question from the selected to category. The returned question will be either a new question or a Null if there are no more questions.
- The request body should be a JSON object and come in the following schema:

  ```
  {
      "previous_questions": {"type": "list"}, // list of id's of the questions that should not be sent as an option
      "quiz_category": {
          "type": "dict",
          "require_all": True,
          "schema": {
              "id": {"type": "integer"},
          },
      },
  }
  ```

  - Note: all fields are required or else an error response will be returned

- Returns an JSON object:
  ```
  {
      "answer": String,
      "category": Int,
      "difficulty": Int,
      "id": Int,
      "question": String,
      "success": Boolean
  }
  ```
- Request:
  ```
  curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[], "quiz_category":{"id":1}}'
  ```
- Response:

  ```
  {
    "current_category": {
        "id": 1
    },
    "question": {
        "answer": "The Liver",
        "category": 1,
        "difficulty": 4,
        "id": 20,
        "question": "What is the heaviest organ in the human body?"
    },
    "success": true,
    "total_questions": 3
  }
  ```

## Deployment N/A

## Authors

Alejandro Guillamon and the Udacity team

## Acknowledgements

The awesome team at Udacity and Coach Caryn
