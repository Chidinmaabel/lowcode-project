import sqlite3

import click
from flask import current_app, g


def get_db():
    """Return the SQLite connection for this request, opening it if needed."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        # Lets us read columns by name, e.g. row["customer_name"]
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """Close the connection at the end of the request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Run schema.sql to create the table."""
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    """Command: flask --app app init-db"""
    init_db()
    click.echo("Initialised the database.")


def init_app(app):
    """Register the close function and the command with the Flask app."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)