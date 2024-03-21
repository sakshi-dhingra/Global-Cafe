# PostgresSQL Database

## Contents of folder

- create_tables.sql is an SQL script that creates the tables for our db
- populate_sample.sql is an SQL script which populates the tables with sample data
- sample_query.sql contains some simple examples queries to the db
- test_db.py connects the db and runs a sample query

## How to run

### Postgres

- You need to have postgres installed to run the db, Windows can use the installer here https://www.postgresql.org/download/windows/ 
- Follow the defaults, give the postgres user the password 'postgres' to be the same as mine, keep port the same.
- keep all the default package downloads
- open pgAdmin 4 and create global_cafe db
- run SQL scripts to create and populate tables

### Test_db.py
- You must insall psycopg2 package
    - 'pip install psycopg2'
- edit fields in the connect() function if necessary