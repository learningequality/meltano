# files-airflow

Meltano project [file bundle](https://meltano.com/docs/command-line-interface.html#file-bundle) for [Airflow](https://airflow.apache.org/).

Files:
- [`orchestrate/dags/meltano.py`](./bundle/orchestrate/dags/meltano.py)

```py
# Add Airflow orchestrator and this file bundle to your Meltano project
meltano add orchestrator airflow

# Add only this file bundle to your Meltano project
meltano add files airflow
```
