ENV=dev
VERSION=3.10.11

SHELL:=/bin/bash
VENV=${PROJECT}-py${VERSION}
VENV_DIR=$(shell pyenv root)/versions/${VENV}
PYTHON=${VENV_DIR}/bin/python
JUPYTER_ENV_NAME=${VENV}
JUPYTER_PORT=8888
PROJECT=$(shell basename $(CURDIR))
BUCKET=compstak-machine-learning

DEFAULT_GOAL: help
.PHONY: help run clean build venv ipykernel update jupyter pytest check-all

# Colors for echos
ccend=$(shell tput sgr0)
ccbold=$(shell tput bold)
ccgreen=$(shell tput setaf 2)
ccso=$(shell tput smso)

HELP_FUN = \
	%help; \
	while(<>) { push @{$$help{$$2 // 'options'}}, [$$1, $$3] if /^([a-zA-Z\-\$\(]+)\s*:.*\#\#(?:@([a-zA-Z\-\)]+))?\s(.*)$$/ }; \
	print "usage: make [target]\n\n"; \
	for (sort keys %help) { \
	print "${WHITE}$$_:${RESET}\n"; \
	for (@{$$help{$$_}}) { \
	$$sep = " " x (32 - length $$_->[0]); \
	print "  ${YELLOW}$$_->[0]${RESET}$$sep${GREEN}$$_->[1]${RESET}\n"; \
	}; \
	print "\n"; }

help: ##@other >> Show this help.
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

build: ##@build >> build the virtual environment with an ipykernel and install requirements
	@echo ""
	@echo "$(ccso)--> Build $(ccend)"
	$(MAKE) venv
	$(MAKE) install
	$(MAKE) pre-commit
	$(MAKE) ipykernel

venv: ##@build >> setup the virtual environment
	@echo "$(ccso)--> Install and setup pyenv and virtualenv $(ccend)"
	pyenv virtualenv -f ${VERSION} ${VENV}
	pyenv local ${VENV}
	echo ${VENV} > .python-version

install: ##@build >> update requirements-dev.txt inside the virtual environment
	@echo "$(ccso)--> Updating packages $(ccend)"
	poetry lock
	poetry install --with=dev,lint,fmt,type_check,jupyter --sync

pre-commit: ##@build >> install pre-commit and update pre-commit hooks
	pre-commit install
	pre-commit autoupdate

ipykernel: venv ##@build >> install a Jupyter iPython kernel using our virtual environment
	@echo ""
	@echo "$(ccso)--> Install ipykernel to be used by jupyter notebooks $(ccend)"
	$(PYTHON) -m ipykernel install \
					--user \
					--name=$(VENV) \
					--display-name=$(JUPYTER_ENV_NAME)
	$(PYTHON) -m jupyter nbextension enable --py widgetsnbextension --sys-prefix

clean: ##@build >> remove all environment and build files
	@echo ""
	@echo "$(ccso)--> Removing virtual environment $(ccend)"
	pyenv virtualenv-delete --force ${VENV}
	rm .python-version

jupyter: venv ##@tool >> start a jupyter notebook
	@echo ""
	@echo "$(ccso)--> Running jupyter notebook on port $(JUPYTER_PORT) $(ccend)"
	jupyter notebook --port $(JUPYTER_PORT)

pytest: ##@tool >> run pytest
	$(PYTHON) -m pytest -s

check-all: ##@tool >> perform pre-commit checks
	pre-commit run --all-files
