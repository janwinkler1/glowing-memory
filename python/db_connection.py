import psycopg2
import os 

# Database connection parameters - replace with your details
params = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST'),
    'port': os.environ.get('DB_PORT')
}

# Connect to the PostgreSQL database
conn = psycopg2.connect(**params)
cursor = conn.cursor()

# Create tables
commands = [
    """
    DROP TABLE IF EXISTS activity CASCADE;
    DROP TABLE IF EXISTS repositories CASCADE;
    """,
    """
    CREATE TABLE repositories (
        repo_id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL UNIQUE,
        url VARCHAR(255)
    );
    """,
    """
    CREATE TABLE activity (
        activity_id SERIAL PRIMARY KEY,
        repo_id INT NOT NULL,
        timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        stars INT,
        forks INT,
        release_date TIMESTAMP,
        created_at TIMESTAMP,
        last_updated TIMESTAMP,
        FOREIGN KEY (repo_id) REFERENCES repositories(repo_id)
    );
    """
]

for command in commands:
    cursor.execute(command)

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()
