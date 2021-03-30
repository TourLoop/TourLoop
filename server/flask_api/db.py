from flask import current_app, g
from db_wrapper import DBWrapper

def get_db():
    if not hasattr(g, 'db'):
        g.db = DBWrapper(\
            current_app.config['DATABASE_URL'],\
            current_app.config['DATABASE_USERNAME'],\
            current_app.config['DATABASE_SECRET_KEY'])
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
