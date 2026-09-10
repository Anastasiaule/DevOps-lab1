import sqlite3
from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS genres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS publishers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    genre_id INTEGER,
    publisher_id INTEGER,
    year INTEGER,
    FOREIGN KEY(author_id) REFERENCES authors(id),
    FOREIGN KEY(genre_id) REFERENCES genres(id),
    FOREIGN KEY(publisher_id) REFERENCES publishers(id)
);
"""

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

def init_app(app):
    app.teardown_appcontext(close_db)

def close_db(exception=None):
    database = g.pop("db", None)
    if database is not None:
        database.close()

def create_tables():
    get_db().executescript(SCHEMA)
    get_db().commit()
