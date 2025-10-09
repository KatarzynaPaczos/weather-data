#!/bin/bash
set -e

AIRFLOW_VERSION=3.0.6
source ./venvs/airflow_${AIRFLOW_VERSION}/bin/activate
export AIRFLOW_HOME=$(pwd)/airflow
export PYTHONPATH=$AIRFLOW_HOME:$PYTHONPATH

# Launch Airflow and its components
airflow standalone
