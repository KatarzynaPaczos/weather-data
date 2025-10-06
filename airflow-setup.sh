#!/bin/bash
set -e

AIRFLOW_VERSION=3.0.6
PYTHON_VERSION=3.12
AIRFLOW_HOME=$(pwd)/airflow

sudo apt update
sudo apt install -y python${PYTHON_VERSION} python${PYTHON_VERSION}-venv python${PYTHON_VERSION}-dev python3-pip build-essential

mkdir -p ./venvs  # virtual environment for Airflow and activate it
python${PYTHON_VERSION} -m venv ./venvs/airflow_${AIRFLOW_VERSION}
source ./venvs/airflow_${AIRFLOW_VERSION}/bin/activate

pip install --upgrade pip

# Define the constraint-file URL
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

# Install Apache Airflow with the specified version and constraints (dependency versions)
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "$CONSTRAINT_URL"
pip install -r requirements.txt --constraint "$CONSTRAINT_URL"
