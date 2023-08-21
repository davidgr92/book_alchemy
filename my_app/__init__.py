from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from book_alchemy.config import get_sqlite_db_uri, \
    get_folder_path_in_root_by_name, SECRET_KEY

db = SQLAlchemy()


def create_app():
    app = Flask(__name__,
                static_folder=get_folder_path_in_root_by_name("static"),
                template_folder=get_folder_path_in_root_by_name("templates"))

    app.config['SQLALCHEMY_DATABASE_URI'] = get_sqlite_db_uri()
    app.secret_key = SECRET_KEY

    db.init_app(app)

    from my_app import main_routes as main_bp
    app.register_blueprint(main_bp.main)

    return app
