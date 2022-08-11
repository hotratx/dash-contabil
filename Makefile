.PHONY: isort
isort:
	isort ./arbi/ ./tests/

.PHONY: black
black:
	black -l 79 *.py

.PHONY: typehint
typehint:
	mypy --ignore-missing-imports arbi/

.PHONY: test 
test:
	pytest tests/

.PHONY: clean
clean:
	find . -type f -name "*.pyc" | xargs rm -fr
	 
	find . -type d -name __pycache__ | xargs rm -fr

.PHONY: checklist
checklist: isort black typehint clean

