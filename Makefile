.PHONY: clean-pyc clean-build docs clean
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-docs - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate HTML documentation"
	@echo "publish-docs - publish documentation website to cloudfront"
	@echo "dist - package"
	@echo "install - install the package to the active Python's site-packages"
	@echo "deploy - deploy the envman REST API "
	@echo "show - show parameters"
	@echo "load - load parameters"

deploy :
	./bin/python2.7 ./deploy.py

show:
	python  ./envman/ssm/parameter.py show --env $(or $(env),dev)

load :
	python  ./envman/ssm/parameter.py load --env $(or $(env),dev) --filename $(or $(filename),config.json)

clean: clean-build clean-pyc clean-docs

clean-build:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr htmlcov/
	@rm -fr site/
	@rm -fr .eggs/
	@find . -name '*.egg-info' -exec rm -fr {} +
	@find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

clean-docs:
	sudo mkdocs build -c -f docs/mkdocs.yml

lint:
	python -m flake8 urilib

test:
	python setup.py test

test-all:
	tox

coverage:
	python -m coverage run --source envman setup.py test
	python -m coverage report -m
	python -m coverage html
	$(BROWSER) htmlcov/index.html

docs:
	sudo mkdocs build -f ./docs/mkdocs.yml -d ./site
	$(BROWSER) site/index.html

publish-docs:
	python -m mkdocs build -f ./docs/mkdocs.yml -d ./site
	aws s3 cp --recursive ./site/ s3://edp.platform.dev.docs/developerdocs/envman/ --profile engieddsipmnoprod
	aws  cloudfront create-invalidation --distribution-id EUKYMB4MXHNE0 --paths /developerdocs/envman/* --profile engieddsipmnoprod
	echo "http://d19czd9nkjyflw.cloudfront.net/developerdocs/envman/index.html"

dist: clean
	python setup.py sdist
	ls -l dist

install: clean
	python setup.py install
