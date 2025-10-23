.PHONY: venv mlflow etl train infer airflow demo config

venv:
	python -m venv .venv && . .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

mlflow:
	@echo "Using local MLflow tracking (no server needed)"
	@echo "MLflow experiments are stored in: $(PWD)/mlruns"
	@echo "To view experiments, use: python -c 'from config import get_config; print(get_config().get_mlflow_ui_command())'"

etl:
	. .venv/bin/activate && python scripts/etl_incremental.py

train:
	. .venv/bin/activate && python scripts/train_gbt.py

infer:
	. .venv/bin/activate && python scripts/batch_infer.py 7

airflow:
	export AIRFLOW_HOME=$(PWD)/.airflow; airflow db init; airflow users create --role Admin --username admin --password admin --email a@a.com --firstname a --lastname a; airflow webserver -p 8080 & sleep 5; airflow scheduler

demo: venv etl train infer

config:
	. .venv/bin/activate && python validate_config.py

dashboard:
	. .venv/bin/activate && python -c 'from config import get_config; import subprocess; subprocess.run(get_config().get_streamlit_command().split())'