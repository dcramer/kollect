develop: install-requirements setup-git

upgrade: install-requirements

setup-git:
	pre-commit install
	git config branch.autosetuprebase always
	git config --bool flake8.strict true

install-requirements:
	poetry install

generate-requirements:
	poetry run pip freeze > $@

test:
	poetry run py.test

reset-db:
	$(MAKE) drop-db
	$(MAKE) create-db
	python manage.py migrate

drop-db:
	dropdb --if-exists kollect

create-db:
	createdb -E utf-8 kollect

build-docker-image:
	docker build -t kollect .

run-docker-image:
	docker rm kollect || exit 0
	docker run --init -d -p 8000:8000/tcp --name kollect kollect
