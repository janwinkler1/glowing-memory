import psycopg2

def write_to_db(data, db_params):
    # Database connection
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    for entry in data:
        # Check if the repository already exists
        cursor.execute("SELECT repo_id FROM repositories WHERE name = %s;", (entry['repository'],))
        result = cursor.fetchone()
        if result:
            repo_id = result[0]
        else:
            # Insert the new repository and get its ID
            cursor.execute(
                "INSERT INTO repositories (name, url) VALUES (%s, %s) RETURNING repo_id;",
                (entry['repository'], f"https://github.com/{entry['repository']}")
            )
            repo_id = cursor.fetchone()[0]

        # Insert into activity table
        cursor.execute(
            """
            INSERT INTO activity (repo_id, timestamp, stars, forks, release_date, created_at, last_updated)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """,
            (repo_id, entry['request_time'], entry['stars'], entry['forks'], 
             entry['release_date'], entry['created_at'], entry['last_updated'])
        )

    # Commit and close
    conn.commit()
    cursor.close()
    conn.close()
