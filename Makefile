
run:
	python main.py

test:
	python -m pytest tests

u_requirements:
	pip3 freeze > requirements.txt
