import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from helpers import get_categories_helper
import json
from cerberus import Validator

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    db = SQLAlchemy()

    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request_func(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    @app.route("/categories")
    def get_categories():
        page = request.args.get("page", 1, int)
        return jsonify(get_categories_helper(page))

    @app.route("/questions")
    def get_questions():
        page = request.args.get("page", 1, int)
        search_term = request.args.get("search_term", None, str)
        response = {}
        if search_term:
            questions = Question.query.filter(
                Question.question.ilike(f"%{search_term}%")
            ).all()
            response = {
                "success": True,
                "total_questions": len(questions),
                "questions": [question.format() for question in questions],
                "current_category": 1,
                "search_term": search_term,
            }
        else:
            pagination = Question.query.paginate(page, QUESTIONS_PER_PAGE)
            categories_query = get_categories_helper()
            response = {
                "success": True,
                "current_page": pagination.page,
                "total_questions": pagination.total,
                "questions": [item.format() for item in pagination.items],
                "current_category": 0,
                "categories": categories_query["categories"],
            }
        return jsonify(response)

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
        return jsonify({"success": True, "question_id": question_id})

    @app.route("/questions", methods=["POST"])
    def create_question():
        error = False
        data = request.get_json()
        schema = {
            "question": {"type": "string"},
            "answer": {"type": "string"},
            "difficulty": {"type": "integer"},
            "category": {"type": "integer"},
        }
        v = Validator(schema, require_all=True, allow_unknown=True)
        if not v(data):
            return abort(400)
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
                    "success": True,
                    "id": question_id,
                    "question": question.question,
                    "answer": question.answer,
                    "category": question.category,
                    "difficulty": question.difficulty,
                }
            )
        )

    @app.route("/categories/<int:category_id>/questions")
    def get_questions_by_category(category_id):
        questions = Question.query.filter_by(category=category_id).all()
        category = Category.query.get(category_id)
        if not questions:
            return abort(404)
        return jsonify(
            {
                "success": True,
                "questions": [question.format() for question in questions],
                "total_questions": len(questions),
                "current_category": category_id,
                "type": category.type,
            }
        )

    @app.route("/quizzes", methods=["POST"])
    def quiz_question():
        data = request.get_json()
        schema = {
            "previous_questions": {"type": "list"},
            "quiz_category": {
                "type": "dict",
                "require_all": True,
                "schema": {
                    "id": {"type": "integer"},
                },
            },
        }
        v = Validator(schema, require_all=True, allow_unknown=True)
        if not v(data):
            return abort(400)
        questions = Question.query.filter(
            Question.id.notin_(data["previous_questions"]),
            Question.category == data["quiz_category"]["id"],
        ).all()
        return jsonify(
            {
                "success": True,
                "question": None if len(questions) < 1 else questions[0].format(),
                "total_questions": len(questions),
                "current_category": data["quiz_category"],
            }
        )

    @app.errorhandler(400)
    def bad_request(e):
        return (
            jsonify({"error": "400", "message": "bad request", "success": False}),
            400,
        )

    @app.errorhandler(404)
    def not_found(e):
        return (
            jsonify(
                {"error": "404", "message": "resource not found", "success": False}
            ),
            404,
        )

    @app.errorhandler(405)
    def not_method(e):
        return (
            jsonify(
                {
                    "error": "405",
                    "message": "method not allowed, refer to the documentation for list of allowed methods",
                    "success": False,
                }
            ),
            405,
        )

    @app.errorhandler(422)
    def unprossesable(e):
        return (
            jsonify(
                {
                    "error": "422",
                    "message": "Unprocessable entity, please format your data in as explained in the api documentation",
                    "success": False,
                }
            ),
            422,
        )

    @app.errorhandler(500)
    def internal_error(e):
        return (
            jsonify(
                {
                    "error": "500",
                    "message": "That is weird... Something went wrong on our side and the server failed to process the request",
                    "success": False,
                }
            ),
            500,
        )

    return app
