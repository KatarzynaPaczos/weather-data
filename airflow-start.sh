#!/bin/bash
set -e

AIRFLOW_VERSION=3.0.6
export AIRFLOW_HOME=$(pwd)/airflow
export PYTHONPATH=$AIRFLOW_HOME:$PYTHONPATH
source ./venvs/airflow_${AIRFLOW_VERSION}/bin/activate

# Launch Airflow and its components
airflow standalone
