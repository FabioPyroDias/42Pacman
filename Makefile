export UV_PROJECT_ENVIRONMENT = pacman

PYTHON = pacman/bin/python3

MYPY_FLAGS = --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs --explicit-package-bases \
		--namespace-packages

RM = rm -rf

install:
	uv sync

run:
	@echo ""

debug:
	@echo ""

clean:
	$(RM) config_tests/
	$(RM) .mypy_cache
	$(RM) __pycache__
	$(RM) parser/__pycache__

lint:
	$(PYTHON) -m flake8
	$(PYTHON) -m mypy $(MYPY_FLAGS) .

lint-strict:
	$(PYTHON) -m flake8
	$(PYTHON) -m mypy --strict .

destroy: clean
	$(RM) pacman