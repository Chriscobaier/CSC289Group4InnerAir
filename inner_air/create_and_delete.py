import json
from datetime import datetime, timedelta
from random import uniform

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
            db.session.add(DBVersion(version='0.06'))
            db.session.commit()
            thisVersion = db.session.query(DBVersion).order_by(DBVersion.version.desc()).first()

        elif str(thisVersion.version) < '0.05':
            print("Database is outdated.")
            print("Beginning Migration")
            print("Updating to DB Version 0.06")
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
            db.session.add(DBVersion(version='0.06'))
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

        if str(thisVersion.version) == '0.06':
            print("Migrating to DB 0.07")
            print("Adding Control Pause exercise")
            db.session.add(Exercise(exercise_name="Control Pause",
                                    exercise_instructions="Sit up with a straight back.  Pinch both nostrils closed with your thumb and forefinger.  Exhale slowly out of your mouth to a natural conclusion.  Press the Start button to begin. When you feel the first potent desire to breath, press stop and take a soft inhale.",
                                    exercise_description="It is important that the first breath in after the Control Pause is controlled and relaxed.  Do not wait so long that you begin to gasp for air, or have generally labored breathing.  Please wait a few minutes and try again.  You should only do this when you are calm and relaxed.  Do not do this after strenuous activities.  Like ANY breath restriction techniques, never attempt while driving, underwater, or in any condition that you could become injured.",
                                    exercise_length="1", category_id="1",
                                    exercise_inhale="1",
                                    exercise_inhale_pause="1",
                                    exercise_exhale="1",
                                    exercise_exhale_pause="1"))
            db.session.add(Exercise(exercise_name="Mini Breath Holds",
                                    exercise_instructions="Exhale gently and hold the breath for half of your Control Pause.  IE: if your Control Pause is 50 seconds, your goal is 25 seconds. You can repeat as often as you want throughout the day.  Try for 100 repetitions.",
                                    exercise_description="A key component to Buteyko breathing is to practice breathing less throughout the day.  This technique trains the body to do just this. Many Buteyko practitioners, medical researchers, and other swear by this to stave off asthma and anxiety attacks.  You can try to do this every 15 minutes through the day if you want to practice.",
                                    exercise_length="1", category_id="1",
                                    exercise_inhale="1",
                                    exercise_inhale_pause="1",
                                    exercise_exhale="1",
                                    exercise_exhale_pause="1"))
            print("Migrated to DB 0.07")
            db.session.add(DBVersion(version='0.07'))
            db.session.commit()

        if str(thisVersion.version) == '0.07':
            print("Migrating to DB 0.08")
            print("Fake Exercise for Demo")
            db.session.add(Exercise(exercise_name="Demo Exercise",
                                    exercise_instructions="Test Demo Instructions",
                                    exercise_description="Test Demo Descriptions",
                                    exercise_length="1", category_id="1",
                                    exercise_inhale="2",
                                    exercise_inhale_pause="2",
                                    exercise_exhale="2",
                                    exercise_exhale_pause="2"))

            print("Migrated to DB 0.08")
            db.session.add(DBVersion(version='0.08'))
            db.session.commit()

        if str(thisVersion.version) == '0.08':
            print("Migrating to DB 0.09, adding demo user with additional exercises")
            db.session.add(User(firstname='DemoFirstName',
                                email='demo@demo.com',
                                password_hash="$2b$12$nEfHRbAwWBJYrk05CvH/x.WEa1DK.mWjmM0HU6LDIIYr9V4ra6l4S",
                                consecutive_days=45,
                                is_confirmed=1))
            db.session.commit()
            demoUser = db.session.query(User).filter(User.email == 'demo@demo.com').first()
            j = 160.20
            k = 190.34
            for i in range(45):
                x = datetime.today() - timedelta(days=i)
                db.session.add(
                    Statistics(date_completed=x, user_id=demoUser.id, exercise_id=11, hold_length=uniform(j, k)))
                db.session.commit()
                j -= uniform(1, 3)
                k -= uniform(1, 5)

            db.session.add(DBVersion(version='0.09'))
            db.session.commit()


DeleteAndCreateDB()
