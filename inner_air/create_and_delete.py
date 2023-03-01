import json
from datetime import datetime, timedelta

from inner_air import app, db
from inner_air.models import DBVersion, Exercise, User, Statistics
from sqlalchemy import text


def DeleteAndCreateDB():
    with app.app_context():
        try:
            thisVersion = db.session.query(DBVersion).order_by(DBVersion.version.desc()).first()
        except:
            print("Database is not found - generating database with starter generic data. DB Version is now 0.05")
            thisVersion = None

        if thisVersion is None:
            db.drop_all()
            db.create_all()
            with open('importdata/data.json') as f:
                data = json.load(f)
                j = data["exercises"]
                for i in j:
                    db.session.add(Exercise(exercise_name=i["name"],
                                            exercise_instructions=i["exercise_instructions"],
                                            exercise_description=i["exercise_description"],
                                            exercise_length=i["exercise_length"], category_id=i["category_id"],
                                            exercise_inhale=i["exercise_inhale"],
                                            exercise_inhale_pause=i["exercise_inhale_pause"],
                                            exercise_exhale=i["exercise_exhale"],
                                            exercise_exhale_pause=i["exercise_exhale_pause"]))

                    db.session.commit()
                j = data["users"]
                for i in j:
                    db.session.add(User(firstname=i["firstname"],
                                        email=i["email"],
                                        password_hash=i["password_hash"],
                                        consecutive_days=i['consecutive_days'],
                                        is_confirmed=1)
                                   )
                for i in range(365):
                    x = datetime.today() - timedelta(days=i)
                    db.session.add(Statistics(date_completed=x, user_id=1, exercise_id=1))
                    db.session.commit()
                for i in range(45):
                    x = datetime.today() - timedelta(days=i)
                    db.session.add(Statistics(date_completed=x, user_id=2, exercise_id=1))
                    db.session.commit()
                for i in range(7):
                    x = datetime.today() - timedelta(days=i)
                    db.session.add(Statistics(date_completed=x, user_id=3, exercise_id=3))
                    db.session.commit()
            db.session.add(DBVersion(version='0.05'))
            db.session.commit()
            thisVersion = db.session.query(DBVersion).order_by(DBVersion.version.desc()).first()

        elif str(thisVersion.version) < '0.05':
            print("Database is outdated.")
            print("Beginning Migration")
            print("Updating to DB Version 0.05")
            print("INCOMPATIBILITY - MUST USE BLANK DATA")
            db.drop_all()
            db.create_all()
            with open('importdata/data.json') as f:
                data = json.load(f)
                j = data["exercises"]
                for i in j:
                    db.session.add(Exercise(exercise_name=i["name"],
                                            exercise_instructions=i["exercise_instructions"],
                                            exercise_description=i["exercise_description"],
                                            exercise_length=i["exercise_length"], category_id=i["category_id"],
                                            exercise_inhale=i["exercise_inhale"],
                                            exercise_inhale_pause=i["exercise_inhale_pause"],
                                            exercise_exhale=i["exercise_exhale"],
                                            exercise_exhale_pause=i["exercise_exhale_pause"]))
                    db.session.commit()
                j = data["users"]
                for i in j:
                    db.session.add(User(firstname=i["firstname"],
                                        email=i["email"],
                                        password_hash=i["password_hash"],
                                        consecutive_days=i['consecutive_days'],
                                        is_confirmed=1)
                                   )
                for i in range(365):
                    x = datetime.today() - timedelta(days=i)
                    db.session.add(Statistics(date_completed=x, user_id=1, exercise_id=1))
                    db.session.commit()
                for i in range(45):
                    x = datetime.today() - timedelta(days=i)
                    db.session.add(Statistics(date_completed=x, user_id=2, exercise_id=1))
                    db.session.commit()
                for i in range(7):
                    x = datetime.today() - timedelta(days=i)
                    db.session.add(Statistics(date_completed=x, user_id=3, exercise_id=3))
                    db.session.commit()
            db.session.add(DBVersion(version='0.05'))
            db.session.commit()

        if str(thisVersion.version) == '0.05':
            print("Upgrading DB from 0.05 to 0.06")

            # Comment about change
            # Updating Exercise length from float to int
            # Disable foreign keys

            class ExerciseNew(db.Model):
                __tablename__ = 'Exercise.Details.new'
                id = db.Column(db.Integer, primary_key=True, autoincrement=True)
                exercise_name = db.Column(db.String(64), nullable=False, unique=True)
                exercise_instructions = db.Column(db.String(2048), nullable=False)
                exercise_description = db.Column(db.String(2048), nullable=False)
                exercise_length = db.Column(db.Integer, nullable=False)
                cumulative_rating = db.Column(db.Float)
                category_id = db.Column(db.Integer, nullable=False)
                user_rating_count = db.Column(db.Integer)
                exercise_inhale = db.Column(db.Integer, nullable=False)
                exercise_inhale_pause = db.Column(db.Integer, nullable=False)
                exercise_exhale = db.Column(db.Integer, nullable=False)
                exercise_exhale_pause = db.Column(db.Integer, nullable=False)

            db.create_all()
            old_exercise_data = db.session.query(Exercise).all()
            for row in old_exercise_data:
                new_row = ExerciseNew(id=row.id, exercise_name=row.exercise_name,
                                      exercise_instructions=row.exercise_instructions,
                                      exercise_description=row.exercise_description,
                                      exercise_length=row.exercise_length,
                                      cumulative_rating=row.cumulative_rating, category_id=row.category_id,
                                      user_rating_count=row.user_rating_count, exercise_inhale=row.exercise_inhale,
                                      exercise_inhale_pause=row.exercise_inhale_pause,
                                      exercise_exhale=row.exercise_exhale,
                                      exercise_exhale_pause=row.exercise_exhale_pause)
                db.session.add(new_row)
            db.session.commit()
            db.session.execute(text("DROP TABLE 'Exercise.Details'"))
            db.session.execute(text("ALTER TABLE 'Exercise.Details.New' RENAME TO 'Exercise.Details'"))

            print("Migrated to DB 0.06")
            db.session.add(DBVersion(version='0.06'))
            db.session.commit()


DeleteAndCreateDB()
