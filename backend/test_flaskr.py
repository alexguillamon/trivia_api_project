import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format(
            "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    new_question = {
        "question": "who am I?",
        "answer": "Alejandro",
        "difficulty": 2,
        "category": 1,
        "extra_cat": "nothing",
    }

    error_question = {
        "question": "who am I?",
        "answer": "Alejandro",
        "difficulty": 2,
    }

    error_quiz = {"this is not a": "correct usage"}

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["current_page"], 1)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["total_categories"], Category.query.count())
        self.assertEqual(len(data["categories"]), 6)
        self.assertEqual(data["categories"]["1"], "Science")

    def test_get_questions(self):
        page = 2
        res = self.client().get(f"/questions?page={page}")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["current_page"], page)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["total_questions"], Question.query.count())
        self.assertEqual(len(data["questions"]), 9)
        self.assertEqual(data["categories"]["1"], "Science")
        self.assertEqual(data["questions"][0]["id"], 15)

    def test_post_questions(self):
        post_response = self.client().post(
            "/questions",
            json=self.new_question,
        )
        data = post_response.get_json()
        question = Question.query.filter_by(question=data["question"]).first()

        self.assertEqual(post_response.status_code, 200)
        self.assertEqual(data["id"], question.id)
        self.assertEqual(data["question"], self.new_question["question"])
        self.assertEqual(data["answer"], self.new_question["answer"])
        self.assertEqual(data["category"], self.new_question["category"])
        self.assertEqual(data["difficulty"], self.new_question["difficulty"])

        with self.app.app_context():
            try:
                question.delete()
            except:
                print("Error deleting created test question")
                self.db.session.rollback()
            finally:
                self.db.session.close()

    def test_delete_questions(self):
        question_id = 0
        question = Question(
            question=self.new_question["question"],
            answer=self.new_question["answer"],
            category=self.new_question["category"],
            difficulty=self.new_question["difficulty"],
        )
        with self.app.app_context():
            try:
                question.insert()
                question_id = question.id
            except:
                print("Error inserting created test question")
                self.db.session.rollback()
            finally:
                self.db.session.close()

        delete_response = self.client().delete(
            f"/questions/{question_id}",
        )
        data = delete_response.get_json()

        question = Question.query.filter_by(id=question_id).one_or_none()

        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(data["question_id"], question_id)
        self.assertIsNone(question)

    def test_get_questions_by_category(self):
        category = 2
        res = self.client().get(f"/categories/{category}/questions")
        data = json.loads(res.data)
        total_questions = Question.query.filter_by(category=category).count()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["current_category"], category)
        self.assertEqual(data["total_questions"], total_questions)
        self.assertEqual(len(data["questions"]), total_questions)
        self.assertEqual(data["type"], "Art")

    def test_get_questions_search(self):
        search_term = "title"
        get_response = self.client().get(
            f"/questions?search_term={search_term}",
        )
        data = get_response.get_json()
        questions = Question.query.filter(
            Question.question.ilike(f"%{search_term}%")
        ).all()

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["total_questions"], len(questions))
        self.assertEqual(len(data["questions"]), len(questions))
        self.assertEqual(data["current_category"], 1)
        self.assertEqual(data["search_term"], search_term)

    def test_post_quizzes(self):
        previous_questions = []
        category = {"id": 3, "type": "geography"}
        post_response = self.client().post(
            "/quizzes",
            json={"previous_questions": previous_questions, "quiz_category": category},
        )
        data = post_response.get_json()
        questions = Question.query.filter(
            Question.id.notin_(previous_questions), Question.category == category["id"]
        ).all()

        self.assertEqual(post_response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["total_questions"], len(questions))
        self.assertEqual(data["question"], questions[0].format())
        self.assertEqual(data["current_category"], category)

    def test_404_error(self):
        res_delete = self.client().delete("/question/1000")
        res_get = self.client().get("/categories/2000/questions")

        self.assertEqual(res_delete.status_code, 404)
        self.assertEqual(res_get.status_code, 404)

    def test_405_error(self):
        res = self.client().get("/questions/1")
        self.assertEqual(res.status_code, 405)

    def test_400_error(self):
        res = self.client().post("/questions", json=self.error_question)
        self.assertEqual(res.status_code, 400)
        res = self.client().post("/quizzes", json=self.error_quiz)
        self.assertEqual(res.status_code, 400)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
