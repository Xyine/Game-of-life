install-dev:
	@echo "Creating virtual environment..."
	python3 -m venv .venv
	@echo "Upgrading pip..."
	.venv/bin/python -m pip install --upgrade pip
	@echo "Installing project with dev dependencies..."
	.venv/bin/python -m pip install -e .[dev]

game:
	.venv/bin/python3 main.py gui
