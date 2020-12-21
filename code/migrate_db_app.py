from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://root:root@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Inspections(db.Model):
    __tablename__ = 'inspections_test1'

    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer)
    project_id = db.Column(db.Integer)
    mp4_url = db.Column(db.String)
    neutral = db.Column(db.Float)
    porn = db.Column(db.Float)
    sexy = db.Column(db.Float)

    def __init__(self, movie_id, project_id, mp4_url, neutral, porn, sexy):
        self.movie_id = movie_id
        self.project_id = project_id
        self.mp4_url = mp4_url
        self.neutral = neutral
        self.porn = porn
        self.sexy = sexy

    def __repr__(self):
        return f"<Inspector {self.name}>"


if __name__ == "__main__":
    manager.run()
