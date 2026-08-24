@export UV_PROJECT_ENVIRONMENT = pacman

PYTHON = pacman/bin/python3 pac-man.py

MYPY_FLAGS = --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs --explicit-package-bases \
		--namespace-packages

RM = rm -rf

install:

run:

debug:

clean:

lint:

lint-strict:

destroy: