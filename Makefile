export UV_PROJECT_ENVIRONMENT:=$(shell \
if [ ! -d pacman ] && [ ! -d .pacman_venv ]; then \
	echo pacman; \
elif [ -d pacman ] && [ -x pacman/bin/python3 ]; then \
	echo pacman; \
else \
	echo .pacman_venv; \
fi)

PYTHON = $(UV_PROJECT_ENVIRONMENT)/bin/python3
PIP = $(UV_PROJECT_ENVIRONMENT)/bin/pip
UV = $(UV_PROJECT_ENVIRONMENT)/bin/uv

MYPY_FLAGS = --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs --explicit-package-bases \
		--namespace-packages

RM = rm -rf
CONFIG = config.json

install:
	@if [ ! -d $(UV_PROJECT_ENVIRONMENT) ]; then \
		python3 -m venv $(UV_PROJECT_ENVIRONMENT); \
	elif [ -d $(UV_PROJECT_ENVIRONMENT) ] && [ ! -x $(PYTHON) ]; then \
		python3 -m venv $(UV_PROJECT_ENVIRONMENT); \
	fi
	@if [ ! -x $(UV) ]; then \
		if [ ! -x $(PIP) ]; then \
			$(PYTHON) -m ensurepip; \
		fi; \
		$(PIP) install uv; \
	fi
	$(UV) sync

run: install
	$(UV) run pac-man.py $(CONFIG);

debug: install
	$(PYTHON) -m pdb pac-man.py $(CONFIG)

clean:
	$(RM) config_tests/
	$(RM) .mypy_cache
	$(RM) __pycache__
	$(RM) */__pycache__
	$(RM) dist
	$(RM) build

lint: install
	clear
	$(PYTHON) -m flake8
	$(PYTHON) -m mypy $(MYPY_FLAGS) .

lint-strict: install
	clear
	$(PYTHON) -m flake8
	$(PYTHON) -m mypy --strict .

destroy: clean
	$(RM) $(UV_PROJECT_ENVIRONMENT)
	$(RM) package
	$(RM) pac-man

package: install
	$(UV) run pyinstaller pac-man.spec
	mv dist/pac-man .
	zip pacman.zip pac-man assets/* config.json README_Package.md
	mkdir package
	mv pac-man package
	mv pacman.zip package
	$(RM) dist
	$(RM) build
	$(RM) pac-man

.PHONY: install run debug clean lint lint-strict destroy package