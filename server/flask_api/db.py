from flask import current_app, g
from neo4j import GraphDatabase, basic_auth


def get_db():
    if not hasattr(g, 'db'):
        driver = GraphDatabase.driver(
            current_app.config['DATABASE_URL'],
            auth=basic_auth(current_app.config['DATABASE_USERNAME'], current_app.config['DATABASE_SECRET_KEY']))
        g.db = driver.session()
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
