# Changelog

## 0.4

- [#2](https://gitlab.com/meltano/files-airflow/-/issues/2) Don't run `meltano elt` again when previous run lasts longer than the interval and hasn't completed yet

## 0.3

- [#1](https://gitlab.com/meltano/files-airflow/-/issues/1) Immediately create DAG for every scheduled pipeline, without waiting until a manual run has succeeded
