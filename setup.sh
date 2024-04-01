#!/bin/bash

# Initialize Airflow database and create admin user
docker-compose run airflow-init

# Start Docker containers
docker-compose up