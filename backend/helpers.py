from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Question, Category


QUESTIONS_PER_PAGE = 10


def get_categories_helper(page=1):
    pagination = Category.query.paginate(
        page,
        QUESTIONS_PER_PAGE,
    )
    return {
        "status": "success",
        "current_page": pagination.page,
        "total_categories": pagination.total,
        "categories": {item.id: item.type for item in pagination.items},
    }
