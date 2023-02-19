
run:
	python main.py

test:
	python -m pytest test_db_models.py

u_requirements:
	pip3 freeze > requirements.txt
