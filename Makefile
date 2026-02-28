install-dev:
	python -m pip install --upgrade pip
	pip install uv
	uv venv
	uv pip install -e .[dev]
