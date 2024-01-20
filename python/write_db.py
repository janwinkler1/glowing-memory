import psycopg2


def write_to_db(data, db_params):
    """
    Writes a list of repository data into the PostgreSQL database.

    Parameters:
    data (list): A list of dictionaries, each containing information about a repository.
    db_params (dict): Database connection parameters including dbname, user, password, host, and port.
    """
    # Establishing a connection to the PostgreSQL database
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    for entry in data:
        # Query to check if the repository already exists in the database
        cursor.execute(
            "SELECT repo_id FROM repositories WHERE name = %s;", (entry["repository"],)
        )
        result = cursor.fetchone()

        # If the repository exists, get its ID, otherwise insert it and get the new ID
        if result:
            repo_id = result[0]
        else:
            # Inserting a new repository record and fetching its ID
            cursor.execute(
                "INSERT INTO repositories (name, url) VALUES (%s, %s) RETURNING repo_id;",
                (entry["repository"], f"https://github.com/{entry['repository']}"),
            )
            repo_id = cursor.fetchone()[0]

        # Inserting a new activity record associated with the repository
        cursor.execute(
            """
            INSERT INTO activity (repo_id, timestamp, stars, forks, release_date, created_at, last_updated)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """,
            (
                repo_id,
                entry["request_time"],
                entry["stars"],
                entry["forks"],
                entry["release_date"],
                entry["created_at"],
                entry["last_updated"],
            ),
        )

    # Committing the transaction to the database
    conn.commit()

    # Closing the cursor and connection to the database
    cursor.close()
    conn.close()
