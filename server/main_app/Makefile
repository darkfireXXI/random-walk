MAX_LINE_LENGTH = 120


black:
	@black . --line-length $(MAX_LINE_LENGTH)

isort:
	@isort . --line-length $(MAX_LINE_LENGTH) --multi-line 3 --profile black

flake8:
	@flake8 . --exclude venv/,testing/memory_profiling/ --max-line-length $(MAX_LINE_LENGTH) --ignore=E203,W503

format:
	@make black
	@make isort
	@make flake8

venv:
	@python3 -m venv venv/

# setup-install:
# 	@pip install -e .

pip-req:
	@pip3 freeze > requirements.txt

pip-install:
	@pip3 install -r requirements.txt

docker-up:
	@docker compose -p random_walk up

alembic-autorevision:
	@alembic -c db/alembic.ini revision --autogenerate -m '$(filter-out $@,$(MAKECMDGOALS))'

alembic-upgrade:
	@alembic -c db/alembic.ini upgrade head

alembic-downgrade:
	@alembic -c db/alembic.ini downgrade -1

alembic-downgrade-base:
	@alembic -c db/alembic.ini downgrade base


# python3 -m http.server 8000
