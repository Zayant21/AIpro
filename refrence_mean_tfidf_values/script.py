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
            password='929268',
            database='aipro'
        )
        
        return connection
    except mysql.connector.Error as err:
        flash(f"An error occurred while connecting to the database: {err}")
        return None


def get_csv_files_in_directory(directory):
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    return [os.path.splitext(f)[0] for f in csv_files]

expected_column_names = [
    'Word',
    'Score'
]

connection = connect_to_database()
cursor = connection.cursor()
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
                #print(data)

                for row in data:
                    cursor.execute(
                        """
                        INSERT INTO reference_mean_tfidf_values( word, score)
                        VALUES (%s, %s)
                        """,
                        (row['Word'], row['Score'])
                        )
                connection.commit()
                cursor.close()
                connection.close()


# calling the funtion main funtion
process_file()
