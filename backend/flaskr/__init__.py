import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from helpers import get_categories_helper
import json

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    db = SQLAlchemy()

    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.route("/categories")
    def get_categories():
        page = request.args.get("page", 1, int)
        return jsonify(get_categories_helper(page))

    @app.route("/questions")
    def get_questions():
        page = request.args.get("page", 1, int)
        pagination = Question.query.paginate(page, QUESTIONS_PER_PAGE)
        categories_query = get_categories_helper()
        return jsonify(
            {
                "status": "success",
                "current_page": pagination.page,
                "total_questions": pagination.total,
                "questions": [item.format() for item in pagination.items],
                "current_category": 0,
                "categories": categories_query["categories"],
            }
        )

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        error = False
        question = Question.query.filter_by(id=question_id).one_or_none()
        if not question:
            return abort(404)
        try:
            question.delete()
        except:
            error = True
            db.session.rollback()
        finally:
            db.session.close()
        return jsonify({"status": "success", "question_id": question_id})

    @app.route("/questions", methods=["POST"])
    def create_question():
        data = request.get_json()
        error = False
        question = Question(
            question=data["question"],
            answer=data["answer"],
            category=data["category"],
            difficulty=data["difficulty"],
        )
        question_id = 0
        try:
            question.insert()
            question_id = question.id
        except:
            error = True
            db.session.rollback()
        finally:
            db.session.close()
        return (
            abort(500)
            if error
            else jsonify(
                {
                    "status": "success",
                    "id": question_id,
                    "question": question.question,
                    "answer": question.answer,
                    "category": question.category,
                    "difficulty": question.difficulty,
                }
            )
        )

    """
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    """

    """
    @TODO: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    """

    @app.route("/categories/<int:category_id>/questions")
    def get_questions_by_category(category_id):
        questions = Question.query.filter_by(category=category_id).all()
        category = Category.query.get(category_id)
        if not questions:
            return abort(404)
        return jsonify(
            {
                "status": "success",
                "questions": [question.format() for question in questions],
                "total_questions": len(questions),
                "current_category": category_id,
                "type": category.type,
            }
        )

    """
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    """

    """
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    """
    return app
