# Rick and Morty ETL

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

This project performs an ETL (Extract, Transform, Load) process on data from the [Rick and Morty API](https://rickandmortyapi.com/) using a Python script, Airflow, and Docker. The data is extracted from the API, transformed for easier ingestion, and loaded into a PostgreSQL database using SQLAlchemy.

The whole process is Dockerised for ease of use and deployment. To make it easier to query and work with the data, a pgAdmin4 service has also been added.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Running the ETL Process](#running-the-etl-process)
- [Checking and Querying Data with pgAdmin4](#checking-and-querying-data-with-pgadmin4)
- [Customization](#customization)
- [Cleanup](#cleanup)
- [Contributing](#contributing)

## Prerequisites

Before running the project, ensure that you have the following prerequisites installed on your system:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Project Structure

The project has the following structure:

- `dags/`: Contains the Airflow DAG definition file (`rick_and_morty_dag.py`).
- `Dockerfile`: Defines the Docker image for running the ETL process.
- `docker-compose.yml`: Defines the services and their configurations for running the project with Docker Compose.
- `etl.py`: Contains the ETL logic for extracting data from the Rick and Morty API, transforming it, and loading it into the PostgreSQL database.
- `requirements.txt`: Lists the Python dependencies required for the project.
- `.env`: Environment variables file for Airflow and the ETL database variables.
- `setup.sh`: A bash script to automate the setup process.
- `README.md`: Provides an overview of the project and instructions for setting it up and running the ETL process.

## Setup

To set up the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/teodorionita/rick-and-morty-etl.git
   cd rick-and-morty-etl
   ```

2. Make the `setup.sh` script executable:
   ```bash
   chmod +x setup.sh
   ```

3. Run the `setup.sh` script to build the Docker images, start the containers, initialize the Airflow database, create the admin user, and unpause the DAG:
   ```bash
   sh setup.sh
   ```

4. Access the Airflow web UI at `http://localhost:8080` using the following credentials:
   - Username: `admin`
   - Password: `admin`

## Running the ETL Process

To run the ETL process, follow these steps:

1. In the Airflow web UI, locate the `rick_and_morty_etl` DAG.

2. Trigger the DAG by clicking on the "Trigger DAG" button.

3. The ETL process will start running, and you can monitor its progress in the Airflow web UI.

4. Once the DAG run is completed, the data from the Rick and Morty API will be loaded into the PostgreSQL database.

## Checking and Querying Data with pgAdmin4

To check and query the data using pgAdmin4, follow these steps:

1. Access pgAdmin4 by opening a web browser and navigating to `http://localhost:5050`.

2. Log in using the following credentials:
   - Email: `admin@example.com`
   - Password: `admin`

3. In the pgAdmin4 interface, expand the "Servers" node in the left sidebar.

4. Right-click on the "Servers" node and select "Create" > "Server".

5. In the "Create - Server" dialog, provide the following details:
   - General tab:
     - Name: Enter a name for the server connection (e.g., "Rick and Morty DB").
   - Connection tab:
     - Host: Enter the hostname or IP address of your PostgreSQL container (`postgres-rick-morty`).
     - Port: Enter the port number on which the PostgreSQL server is running (default: `5432`).
     - Maintenance database: Enter the name of the database you want to connect to (`rick_and_morty`).
     - Username: Enter the username to authenticate with the PostgreSQL server (`rick`).
     - Password: Enter the password for the specified username (`morty`).
   - SSL tab:
     - SSL mode: Select "Prefer" or "Disable" based on your setup. If you are using a local development environment without SSL, you can select "Disable".

6. Click "Save" to create the server connection.

7. Expand the newly created server connection in the left sidebar.

8. Expand the "Databases" node, navigate to the "rick_and_morty" database, and explore the tables under the "Schemas" > "public" section.

9. Right-click on a table (e.g., `characters`, `episodes`, `locations`) and select "View/Edit Data" to view and query the data.

You can now use pgAdmin4 to explore and query the data loaded by the ETL process.

## Customization

If you want to customize the project, you can:

- Modify the ETL logic by updating the `etl.py` script.
- Change the DAG configuration or schedule by updating the `rick_and_morty_dag.py` file in the `dags/` directory.
- Modify the PostgreSQL database configuration by updating the `config.ini` file.

## Cleanup

To stop and remove the Docker containers, run the following command:
```bash
docker-compose down
```

To fully remove the volumes along with the containers, run the following command:
```bash
docker-compose down -v
```
`!This will also remove all of the data alongside the database!`

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request. You can reach out to me at teodorio@protonmail.com or on DM me on Twitter at `@teodor_io`.
