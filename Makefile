# Makefile - simple targets for building docs with Quarto and running tests
.PHONY: docs test fmt

QUARTO := quarto

docs:
	@echo "Building Quarto docs (if any)..."
	if [ -d docs ]; then \
		$(QUARTO) render docs; \
	else \
		$(QUARTO) render . || true; \
	fi

test:
	python3 -m pytest -q

fmt:
	# placeholder for formatting (black, isort) if you add Python tooling
	echo "No formatter configured"
