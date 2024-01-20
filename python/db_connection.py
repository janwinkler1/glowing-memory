import psycopg2
import os

# Database connection parameters - sourced from environment variables
params = {
    "dbname": os.environ.get("DB_NAME"),     # Database name
    "user": os.environ.get("DB_USER"),       # Database user
    "password": os.environ.get("DB_PASSWORD"),  # Database password
    "host": os.environ.get("DB_HOST"),       # Database host (e.g., localhost)
    "port": os.environ.get("DB_PORT"),       # Database port (e.g., 5432 for PostgreSQL)
}

# Establish a connection to the PostgreSQL database
# Note: Ensure the environment variables are correctly set in the .env file
conn = psycopg2.connect(**params)
cursor = conn.cursor()

# SQL commands to create the database schema
commands = [
    """
    DROP TABLE IF EXISTS activity CASCADE;
    DROP TABLE IF EXISTS repositories CASCADE;
    """,
    """
    CREATE TABLE repositories (
        repo_id SERIAL PRIMARY KEY,  # Unique identifier for each repository
        name VARCHAR(255) NOT NULL UNIQUE,  # Repository name
        url VARCHAR(255)  # Repository URL
    );
    """,
    """
    CREATE TABLE activity (
        activity_id SERIAL PRIMARY KEY,  # Unique identifier for each activity record
        repo_id INT NOT NULL,  # Corresponding repository ID
        timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  # Timestamp of the activity
        stars INT,  # Number of stars
        forks INT,  # Number of forks
        release_date TIMESTAMP,  # Release date of the repository
        created_at TIMESTAMP,  # Creation date of the repository
        last_updated TIMESTAMP,  # Last updated timestamp
        FOREIGN KEY (repo_id) REFERENCES repositories(repo_id)  # Foreign key linking to repositories table
    );
    """,
]

# Execute each command to create the tables
for command in commands:
    cursor.execute(command)

# Commit the changes to the database
conn.commit()

# Close the cursor and connection to clean up
cursor.close()
conn.close()

