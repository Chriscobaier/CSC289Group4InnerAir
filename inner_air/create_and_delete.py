import json
from datetime import datetime, timedelta

from inner_air import app, db
from inner_air.models import DBVersion, Exercise, User, Statistics


def DeleteAndCreateDB():
    with app.app_context():
        try:
            thisVersion = db.session.query(DBVersion).order_by(DBVersion.version.desc()).first()
        except:
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
                                            exercise_length=i["exercise_length"], category_id=i["category_id"]))
                    db.session.commit()
                j = data["users"]
                for i in j:
                    db.session.add(User(firstname=i["firstname"],
                                        email=i["email"],
                                        password_hash=i["password_hash"],
                                        consecutive_days=i['consecutive_days']))
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
            db.session.add(DBVersion(version='0.02'))
            db.session.commit()
        elif str(thisVersion.version) < '0.02':
            db.drop_all()
            db.create_all()
            with open('importdata/data.json') as f:
                data = json.load(f)
                j = data["exercises"]
                for i in j:
                    db.session.add(Exercise(exercise_name=i["name"],
                                            exercise_instructions=i["exercise_instructions"],
                                            exercise_description=i["exercise_description"],
                                            exercise_length=i["exercise_length"], category_id=i["category_id"]))
                    db.session.commit()
                j = data["users"]
                for i in j:
                    db.session.add(User(firstname=i["firstname"],
                                        email=i["email"],
                                        password_hash=i["password_hash"],
                                        consecutive_days=i['consecutive_days']))
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
            db.session.add(DBVersion(version='0.02'))
            db.session.commit()


DeleteAndCreateDB()
