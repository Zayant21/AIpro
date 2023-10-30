from flask import Flask, render_template, request, jsonify, redirect, url_for
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from numpy.linalg import norm
from mysql.connector import errors
import mysql.connector
import pandas as pd
import csv
import io
import json 

app = Flask(__name__)
app.debug = True

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
        



@app.route('/')
def hello_world():
    result_dict = {}
    chart_data_wo = {} 
    chart_data = {} 
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM site_data")
    rows = cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description] 
    result_dict = [dict(zip(column_names, row)) for row in rows]

    cursor = connection.cursor(dictionary=True)

    chart_data_wo = {
        'keybert_relevance': get_chart_data(cursor, 'keybert_relevance_table_wo'),
        'spacey_tfidf': get_chart_data(cursor, 'spacey_tfidf_table_wo'),
        'rake_unconstrained': get_chart_data(cursor, 'rake_unconstrained_table_wo'),
        'nltk_word': get_chart_data(cursor, 'nltk_word_table_wo'),
        'textrank_phrase': get_chart_data(cursor, 'textrank_phrase_table_wo'),
        'yake_phrase': get_chart_data(cursor, 'yake_phrase_table_wo'),
        'pke_phrase': get_chart_data(cursor, 'pke_word_table_wo')
    }

    # Get chart data with preprocessing
    chart_data = {
        'keybert_relevance': get_chart_data(cursor, 'keybert_relevance_table'),
        'spacey_tfidf': get_chart_data(cursor, 'spacey_tfidf_table'),
        'rake_unconstrained': get_chart_data(cursor, 'rake_unconstrained_table'),
        'nltk_word': get_chart_data(cursor, 'nltk_word_table'),
        'textrank_phrase': get_chart_data(cursor, 'textrank_phrase_table'),
        'yake_phrase': get_chart_data(cursor, 'yake_phrase_table'),
        'pke_phrase': get_chart_data(cursor, 'pke_word_table')
    }

    cursor.close()
    connection.close()

    if result_dict:
        return render_template('index.html', result_dict=json.dumps(result_dict),
            chart_data_wo=json.dumps(chart_data_wo), chart_data=json.dumps(chart_data))

    return render_template('index.html', result_dict=json.dumps(result_dict), chart_data_wo=json.dumps(chart_data_wo), chart_data=json.dumps(chart_data))


expected_column_names_1 = [
    'company_domain',
    'line_count_before',
    'line_count_after',
    'word_count_before',
    'word_count_after',
    'scrapped_links'
]

@app.route('/', methods=['POST'])
def process_file():
    result_dict = {}
    chart_data_wo = {} 
    chart_data = {}

    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM site_data")
    rows = cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description] 
    result_dict = [dict(zip(column_names, row)) for row in rows]
    cursor = connection.cursor(dictionary=True)

    chart_data_wo = {
        'keybert_relevance': get_chart_data(cursor, 'keybert_relevance_table_wo'),
        'spacey_tfidf': get_chart_data(cursor, 'spacey_tfidf_table_wo'),
        'rake_unconstrained': get_chart_data(cursor, 'rake_unconstrained_table_wo'),
        'nltk_word': get_chart_data(cursor, 'nltk_word_table_wo'),
        'textrank_phrase': get_chart_data(cursor, 'textrank_phrase_table_wo'),
        'yake_phrase': get_chart_data(cursor, 'yake_phrase_table_wo'),
        'pke_phrase': get_chart_data(cursor, 'pke_word_table_wo')
    }

    # Get chart data with preprocessing
    chart_data = {
        'keybert_relevance': get_chart_data(cursor, 'keybert_relevance_table'),
        'spacey_tfidf': get_chart_data(cursor, 'spacey_tfidf_table'),
        'rake_unconstrained': get_chart_data(cursor, 'rake_unconstrained_table'),
        'nltk_word': get_chart_data(cursor, 'nltk_word_table'),
        'textrank_phrase': get_chart_data(cursor, 'textrank_phrase_table'),
        'yake_phrase': get_chart_data(cursor, 'yake_phrase_table'),
        'pke_phrase': get_chart_data(cursor, 'pke_word_table')
    }

    cursor.close()
    connection.close()

    if 'myfile' in request.files:
        file = request.files['myfile']
        if file.filename.endswith('.csv'):

            csv_data = csv.reader(file.stream.read().decode('utf-8').splitlines())
            header_row = None
            header_format = None
                    
            for row in csv_data:
                if all(col_name in row for col_name in expected_column_names_1):
                    header_row = row
                    header_format = 1
                    break
                        
            if header_row is None:
                return render_template('index.html',result_dict=json.dumps(result_dict),chart_data_wo=json.dumps(chart_data_wo), chart_data=json.dumps(chart_data), 
                                       message="Error: Upload CSV with valid headers!")

            columns_to_keep = [col_name for col_name in header_row if col_name in expected_column_names_1]

            data_rows = [row for row in csv_data if any(row)]
            #csv_data = list(csv.reader(csvfile))
            df = pd.DataFrame(data_rows, columns=header_row)
            df = df[columns_to_keep]
            pd.set_option('display.max_columns', None)
            data = df.to_dict(orient="records")

            connection = connect_to_database()
            cursor = connection.cursor()
            for row in data:
                cursor.execute(
                    """
                    INSERT INTO site_data (company_domain, line_count_before, line_count_after, word_count_before, word_count_after,scrapped_links)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    line_count_before = VALUES(line_count_before),
                    line_count_after = VALUES(line_count_after),
                    word_count_before = VALUES(word_count_before),
                    word_count_after = VALUES(word_count_after)
                    """,
                    (row['company_domain'], row['line_count_before'], row['line_count_after'], 
                    row['word_count_before'], row['word_count_after'], row['scrapped_links'])
                )
                entries = [row['company_domain'] for row in data]
            connection.commit()
            cursor.close()
            connection.close()

            if entries:
                return render_template('index.html', entries=entries, result_dict=json.dumps(result_dict),
                    chart_data_wo=json.dumps(chart_data_wo), chart_data=json.dumps(chart_data))
            else:
                return render_template('index.html',result_dict=json.dumps(result_dict),
                    chart_data_wo=json.dumps(chart_data_wo), chart_data=json.dumps(chart_data), message="Error: Upload CSV with valid headers!")
        else:
            return render_template('index.html',result_dict=json.dumps(result_dict),
                    chart_data_wo=json.dumps(chart_data_wo), chart_data=json.dumps(chart_data), message="Upload a valid CSV file!")
    else:
        return render_template('index.html',result_dict=json.dumps(result_dict),
                    chart_data_wo=json.dumps(chart_data_wo), chart_data=json.dumps(chart_data), message="No file was uploaded.")



@app.route('/similarity_comparison', methods=['POST'])
def reference_comparision():
    data = request.get_json()
    datatype = data.get('datatype')
    algorithm = data.get('algorithm')

    connection = connect_to_database() 
    cursor = connection.cursor()

    cursor.execute("SELECT word FROM vocabulary")
    vocabulary = cursor.fetchall()
    vocab = [row[0] for row in vocabulary]

    cursor.execute("SELECT word, score FROM reference_mean_tfidf_values")
    reference_mean_tfidf_values = cursor.fetchall()
    word_freq_dict_ref = dict(reference_mean_tfidf_values)
    ref_vector = [word_freq_dict_ref.get(word, 0) for word in vocab]
    ref_vector = np.array(ref_vector, dtype=np.float64)

    cursor.execute("SELECT  id,  company_domain FROM site_data")
    site_data = cursor.fetchall()

    if (datatype == 'PreProcessed'):
        cursor.execute("SELECT algorithm FROM algorithms_list WHERE is_pre_processed = 1")
        algorithms_list = cursor.fetchall()
    else:
        cursor.execute("SELECT algorithm FROM algorithms_list WHERE is_pre_processed = 0")
        algorithms_list = cursor.fetchall()
    algorithms_list = [row[0] for row in algorithms_list]

    site_results = {}
    for row in site_data:
        id, company_domain = row
        if company_domain not in site_results:
            site_results[company_domain] = {}
        for algo in algorithms_list:
            cursor.execute("SELECT word, score FROM {} WHERE domain_id = %s".format(algo), (id,))
            table_data = cursor.fetchall()
            word_freq_dict = dict(table_data)
            vector = [word_freq_dict.get(word, 0) for word in vocab]
            vector = np.array(vector, dtype=np.float64)
    
            if algorithm == 'cosine':
                if np.count_nonzero(ref_vector) > 0 and np.count_nonzero(vector) > 0:
                    cosine_similarity = round(np.dot(ref_vector, vector) / (norm(ref_vector) * norm(vector)), 4)
                    similarity_percentage = round(cosine_similarity * 100, 2)
                elif not word_freq_dict:
                    similarity_percentage = -1
                else:
                    similarity_percentage = 0

            elif algorithm == 'jaccard':
                if np.count_nonzero(ref_vector) > 0 and np.count_nonzero(vector) > 0:
                    ref_set = set(np.where(ref_vector > 0)[0])
                    vector_set = set(np.where(vector > 0)[0])
                    similarity = jaccard_similarity(ref_set, vector_set)
                    similarity_percentage = round(similarity * 100, 2)
                elif not word_freq_dict:
                    similarity_percentage = -1
                else:
                    similarity_percentage = 0

            site_results[company_domain][algo] = similarity_percentage

    cursor.close()
    connection.close()
    response_data = {
        'vocab': vocab,
        'site_results': site_results
    }
    return jsonify(response_data)


@app.route('/get_vocabulary_data')
def get_vocabulary_data():
    connection = connect_to_database() 
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM vocabulary')
    vocabulary_data = cursor.fetchall()
    connection.close()
    return jsonify(vocabulary_data)

@app.route('/add_vocab_word', methods=['POST'])
def add_word():
    data = request.get_json()
    new_word = data['word']

    connection = connect_to_database() 
    cursor = connection.cursor()
    try:
        cursor.execute('INSERT INTO vocabulary (word) VALUES (%s)', (new_word,))
        connection.commit()
        connection.close()
        return jsonify({'success': True})
    except:
        connection.rollback()
        connection.close()
        return jsonify({'success': False})

@app.route('/remove_vocab_word/<word>', methods=['DELETE'])
def remove_word(word):
    connection = connect_to_database() 
    cursor = connection.cursor()
    try:
        cursor.execute('DELETE FROM vocabulary WHERE word=%s', (word,))
        connection.commit()
        connection.close()
        return jsonify({'success': True})
    except:
        connection.rollback()
        connection.close()
        return jsonify({'success': False})



def jaccard_similarity(set1, set2):
    intersection = len(set(set1) & set(set2))
    union = len(set(set1) | set(set2))
    return intersection / union

def get_chart_data(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    data_dict = {}

    for row in rows:
        domain_id = row['domain_id']
        word = row['word']
        score = row['score']
        id = row['id']

        if domain_id not in data_dict:
            data_dict[domain_id] = []

        data_dict[domain_id].append({
            'word': word,
            'score': score,
            'id': id
        })

    return data_dict

@app.after_request
# Get rid of stored cache
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r



if __name__ == '__main__':
    app.run(port=5080)