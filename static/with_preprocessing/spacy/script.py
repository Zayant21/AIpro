from mysql.connector import errors
import mysql.connector
import pandas as pd
import csv
import io
import os

directory = '.'

def connect_to_database():
    try:
        #Try connecting to the first database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='dp5RAtele',
            database='AIPro'
        )
        
        return connection
    except mysql.connector.Error as err:
        flash(f"An error occurred while connecting to the database: {err}")
        return None


def get_csv_files_in_directory(directory):
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    return [os.path.splitext(f)[0] for f in csv_files]


connection = connect_to_database()
cursor = connection.cursor()

if get_csv_files_in_directory(directory):
    for row in get_csv_files_in_directory(directory):
        cursor.execute(
            """
            INSERT IGNORE INTO site_data (company_domain)
            VALUES (%s)
            """,
            (row,)
        )
    connection.commit()
    cursor.close()
    connection.close()


expected_column_names = [
    'Word',
    'Score'
]


def process_file():
    if not get_csv_files_in_directory(directory):
        print("error: No CSV files found in the directory.")

    for csv_file in get_csv_files_in_directory(directory):
        
        file_name = os.path.join(directory, f"{csv_file}.csv")
        print(file_name)
        if file_name.endswith('.csv'):
            with open(file_name, 'r', encoding='utf-8') as file:
                csv_data = csv.reader(file)
                header_row = None
                header_format = None
                        
                for row in csv_data:
                    if all(col_name in row for col_name in expected_column_names):
                        header_row = row
                        header_format = 1
                        break
                            
                if header_row is None:
                    print("error: No valid header is found in file ",file_name )

                columns_to_keep = [col_name for col_name in header_row if col_name in expected_column_names]

                data_rows = [row for row in csv_data if any(row)]
                df = pd.DataFrame(data_rows, columns=header_row)
                df = df[columns_to_keep]
                pd.set_option('display.max_columns', None)
                data = df.to_dict(orient="records")


                connection = connect_to_database()
                cursor = connection.cursor()
                cursor.execute("SELECT id FROM site_data WHERE company_domain = %s", (csv_file,))
                result = cursor.fetchall()

                if result:
                    site_data_id = result[0][0]
                else:
                    site_data_id = None

                if site_data_id is not None:
                    for row in data:
                        cursor.execute(
                            """
                            INSERT INTO spacey_tfidf_table(domain_id, word, tfidf)
                            VALUES (%s, %s, %s)
                            """,
                            (site_data_id, row['Word'], row['Score'])
                        )
                    connection.commit()
                    cursor.close()
                    connection.close()


# calling the funtion main funtion
process_file()
