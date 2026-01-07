.SILENT:

setup-env:
	python -m venv venv
	venv\Scripts\activate && python -m pip install --upgrade pip
	venv\Scripts\activate && python -m pip install -r requirements.txt

run-agent:
	venv\Scripts\activate && python agent.py

run-test:
	venv\Scripts\activate && python -m test.test_units