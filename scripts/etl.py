import requests
import json
import logging
import os
from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine, text

# Load database configuration from environment variables
DATABASE = {
    'user': os.environ.get('RICK_AND_MORTY_USER'),
    'password': os.environ.get('RICK_AND_MORTY_PASSWORD'),
    'host': os.environ.get('RICK_AND_MORTY_HOST'),
    'port': os.environ.get('RICK_AND_MORTY_PORT'),
    'database': os.environ.get('RICK_AND_MORTY_DB'),
}
DATABASE_URL = f"postgresql://{DATABASE['user']}:{DATABASE['password']}@{DATABASE['host']}:{DATABASE['port']}/{DATABASE['database']}"

# SQL statements for creating and dropping tables in Postgres



CREATE_TABLES_SQL = {
    'characters': """
    CREATE TABLE IF NOT EXISTS characters (
        id SERIAL PRIMARY KEY,
        name TEXT,
        status TEXT,
        species TEXT,
        type TEXT,
        gender TEXT,
        origin JSONB,
        location JSONB,
        image TEXT,
        episode JSONB,
        url TEXT,
        created TIMESTAMP WITHOUT TIME ZONE
    );
    """,
    'locations': """
    CREATE TABLE IF NOT EXISTS locations (
        id SERIAL PRIMARY KEY,
        name TEXT,
        type TEXT,
        dimension TEXT,
        residents JSONB,
        url TEXT,
        created TIMESTAMP WITHOUT TIME ZONE
    );
    """,
    'episodes': """
    CREATE TABLE IF NOT EXISTS episodes (
        id SERIAL PRIMARY KEY,
        name TEXT,
        air_date TEXT,
        episode TEXT,
        characters JSONB,
        url TEXT,
        created TIMESTAMP WITHOUT TIME ZONE
    );
    """
}

# Function to fetch data from the API with error handling and logging
def extract_data(endpoint):
    url = f"https://rickandmortyapi.com/api/{endpoint}"
    results = []
    max_retries = 3
    retry_delay = 5

    while url:
        for retry in range(max_retries):
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
                data = response.json()
                results.extend(data.get('results', []))
                url = data.get('info', {}).get('next')
                break
            except requests.exceptions.RequestException as e:
                logging.error(f"Error fetching data from {url}: {e}")
                if retry < max_retries - 1:
                    logging.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    logging.error(f"Max retries exceeded. Skipping URL: {url}")
                    url = None
                    break

    logging.info(f"Fetched {len(results)} records from {endpoint} endpoint.")
    return results

# Function to drop tables
def drop_tables(engine):
    logging.info("Dropping tables in the database.")
    with engine.connect() as connection:
        for table_name, drop_statement in DROP_TABLES_SQL.items():
            try:
                connection.execute(text(drop_statement))
                logging.info(f"Successfully dropped {table_name} table.")
            except Exception as e:
                logging.error(f"Error dropping {table_name} table: {e}")

# Function to create tables 
def create_tables(engine):
    logging.info("Creating tables in the database.")
    with engine.connect() as connection:
        for table_name, create_statement in CREATE_TABLES_SQL.items():
            try:
                connection.execute(text(create_statement))
                logging.info(f"Successfully created {table_name} table.")
            except Exception as e:
                logging.error(f"Error creating {table_name} table: {e}")

# Function to transform data
def transform_data(data, table_name):
    # Convert the data to a DataFrame
    df = pd.DataFrame(data)
    
    # Convert 'origin' and 'location' columns to JSON strings if they exist
    if 'origin' in df.columns:
        df['origin'] = df['origin'].apply(json.dumps)
    if 'location' in df.columns:
        df['location'] = df['location'].apply(json.dumps)
    
    # Convert array columns to JSON strings if they exist
    array_columns = ['episode', 'residents', 'characters']
    for column in array_columns:
        if column in df.columns:
            df[column] = df[column].apply(json.dumps)
    
    return df

# Load data to PostgreSQL using SQLAlchemy with logging
def load_data(df, table_name, engine):
    logging.info(f"Loading data into {table_name} table.")
    df.to_sql(table_name, engine, if_exists='replace', index=False, method='multi', chunksize=100)
    logging.info(f"Successfully loaded data into {table_name} table.")

# Main ETL function with error handling and logging
def etl_process():
    logging.info("ETL process started.")
    
    engine = create_engine(DATABASE_URL)

    create_tables(engine)
    
    for endpoint, table in [('character', 'characters'), ('location', 'locations'), ('episode', 'episodes')]:
        data = extract_data(endpoint)
        df = transform_data(data, table)
        load_data(df, table, engine)
        
    logging.info("ETL process completed.")

if __name__ == '__main__':
    start_time = datetime.now()
    etl_process()
    end_time = datetime.now()
    logging.info(f"ETL process execution time: {end_time - start_time}")