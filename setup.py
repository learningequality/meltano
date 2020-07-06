from setuptools import setup, find_packages

setup(
    name="files-airflow",
    version="0.3",
    description="Meltano project files for Airflow",
    packages=find_packages(),
    package_data={"bundle": ["orchestrate/dags/meltano.py"]},
)
