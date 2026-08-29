import pyodbc
import csv
import time
import os

# --- 1. CONFIGURATION ---
# Connection details are loaded from environment variables so credentials
# are never committed to the repository.
SERVER = os.getenv("SQL_SERVER", "YOUR_SQL_SERVER")
DATABASE = os.getenv("SQL_DATABASE", "YOUR_DATABASE")
USERNAME = os.getenv("SQL_USERNAME", "YOUR_SQL_USERNAME")
PASSWORD = os.getenv("SQL_PASSWORD")

INPUT_DIR = os.getenv("DW_INPUT_DIR", "LDS Data 2025-2026/DW_Import/")

if not PASSWORD:
    raise RuntimeError(
        "SQL_PASSWORD is not set. Configure SQL_SERVER, SQL_DATABASE, "
        "SQL_USERNAME and SQL_PASSWORD as environment variables before running."
    )

connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER};DATABASE={DATABASE};"
    f"UID={USERNAME};PWD={PASSWORD}"
)


def get_connection():
    print("Connecting to SQL Server...")
    conn = pyodbc.connect(connection_string)
    print("Connection established successfully.\n")
    return conn


def upload_table(cursor, table_name, file_name, sql_query, batch_size=1000):
    print(f"Starting upload for table: {table_name}")

    file_path = os.path.join(INPUT_DIR, file_name)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    print(f"Reading file: {file_name}")
    start_time = time.time()

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header

        batch_data = []
        total_rows = 0

        for row in reader:
            cleaned_row = [None if x == "" else x for x in row]
            batch_data.append(cleaned_row)

            if len(batch_data) >= batch_size:
                cursor.executemany(sql_query, batch_data)
                total_rows += len(batch_data)
                batch_data = []
                print(f"Uploaded {total_rows} rows...", end="\r")

        if batch_data:
            cursor.executemany(sql_query, batch_data)
            total_rows += len(batch_data)

    elapsed = time.time() - start_time
    print(f"\nCompleted upload for {table_name}")
    print(f"Total rows uploaded: {total_rows}")
    print(f"Time taken: {elapsed:.2f} seconds\n")


def main():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        print("Beginning data upload process...\n")

        sql_time = """
            INSERT INTO Dim_Time
            (id_time, year, month, day, quarter, season)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        upload_table(cursor, "Dim_Time", "Dim_Time.csv", sql_time)
        conn.commit()
        print("Dim_Time committed successfully.\n")

        sql_artist = """
            INSERT INTO Dim_Artist
            (id_artist, name, gender, birth_place, country, region, h3_index, latitude, longitude)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        upload_table(cursor, "Dim_Artist", "Dim_Artist.csv", sql_artist)
        conn.commit()
        print("Dim_Artist committed successfully.\n")

        sql_track = """
            INSERT INTO Dim_Track
            (id_track, title, song_category, featured_artists, explicit,
             duration_ms, bpm, n_tokens, language,
             n_sentences, char_per_tok, avg_token_per_clause, swear_IT, swear_EN)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        upload_table(cursor, "Dim_Track", "Dim_Track.csv", sql_track)
        conn.commit()
        print("Dim_Track committed successfully.\n")

        sql_fact = """
            INSERT INTO Fact_Streams
            (id_track, id_artist, id_time, streams, popularity)
            VALUES (?, ?, ?, ?, ?)
        """
        upload_table(cursor, "Fact_Streams", "Fact_Streams.csv", sql_fact)
        conn.commit()
        print("Fact_Streams committed successfully.\n")

        print("All data uploaded successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()
        print("Database connection closed.")


if __name__ == "__main__":
    main()
