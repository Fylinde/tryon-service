#!/bin/bash

# Log start of the script
echo "Starting start.sh script..."

# Ensure the wait-for-it script is executable
chmod +x ./wait-for-it.sh
echo "wait-for-it.sh script is now executable."

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL server to be available on port 5433..."
./wait-for-it.sh db:5433 --timeout=180 --strict

if [ $? -ne 0 ]; then
  echo "ERROR: PostgreSQL did not become available. Exiting..."
  exit 1
else
  echo "SUCCESS: PostgreSQL is ready and reachable on port 5433."
fi

# Additional verification to confirm actual connection to the database
echo "Verifying actual connection to PostgreSQL database..."

# Use a small Python script to attempt the connection
python3 - <<END
import psycopg2
import os

try:
    connection = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "tryon_service_db"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "Sylvian"),
        host="db",
        port="5433"
    )
    connection.close()
    print("SUCCESS: Successfully connected to the PostgreSQL database on port 5433.")
except Exception as e:
    print("ERROR: Could not connect to the PostgreSQL database on port 5433.")
    print(f"DETAILS: {e}")
    exit(1)
END

# Wait for RabbitMQ to be ready
#echo "Waiting for RabbitMQ server to be available on port 5672..."
#./wait-for-it.sh rabbitmq:5672 --timeout=180 --strict

#if [ $? -ne 0 ]; then
#  echo "ERROR: RabbitMQ did not become available. Exiting..."
#  exit 1
#else
#  echo "SUCCESS: RabbitMQ is ready and reachable on port 5672."
#fi

# Set the PYTHONPATH environment variable
export PYTHONPATH=/app
echo "PYTHONPATH is set to $PYTHONPATH"

# Set the SECRET_KEY environment variable
export SECRET_KEY="DbSLoIREJtu6z3CVnpTd_DdFeMMRoteCU0UjJcNreZI"
echo "SECRET_KEY is set."

# Navigate to the app directory
cd /app
echo "Current directory is $(pwd)"

# Log the files in various directories for confirmation
echo "Files in the /app directory:"
ls -l

echo "Files in the /app/app directory:"
ls -l app

echo "Files in the /app/app/models directory:"
ls -l app/models

#echo "Files in the /app/app/migrations directory:"
#ls -l app/migrations

echo "Files in the /app/app/static directory:"
ls -l app/static

# Check for necessary files and directories before starting
if [ ! -f app/main.py ]; then
  echo "ERROR: main.py does not exist in the /app/app directory. Exiting..."
  exit 1
else
  echo "CONFIRMED: main.py exists in the /app/app directory."
fi

#if [ ! -f alembic.ini ]; then
#  echo "ERROR: alembic.ini does not exist in the /app directory. Exiting..."
#  exit 1
#else
##  echo "CONFIRMED: alembic.ini exists in the /app directory."
#fi

#if [ ! -d app/migrations ]; then
#  echo "ERROR: Migrations directory does not exist in the /app/app directory. Exiting..."
#  exit 1
#else
#  echo "CONFIRMED: Migrations directory exists in the /app/app directory."
#fi

# Run Alembic migrations with additional logging
#echo "Attempting to run Alembic migrations to ensure the database is up-to-date..."
#alembic upgrade head

#if [ $? -ne 0 ]; then
#  echo "ERROR: Alembic migrations failed. Check database connection settings and migration files."
##  exit 1
#else
#  echo "SUCCESS: Database migrations completed successfully."
#fi

# Start the FastAPI application with debug logs
echo "Starting tryon-service with debug logs..."
uvicorn app.main:app --host 0.0.0.0 --port 8014 --log-level debug
