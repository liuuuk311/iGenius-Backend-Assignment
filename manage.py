from flask.cli import FlaskGroup
import os
from app import create_app, db

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)
cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    cli()
