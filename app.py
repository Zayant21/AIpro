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
    return render_template('index.html')

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
                return jsonify({"error": "No valid header row found in the CSV file."})

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
            connection.commit()
            cursor.execute("SELECT * FROM site_data")
            rows = cursor.fetchall()

            column_names = [desc[0] for desc in cursor.description] 
            result_dict = [dict(zip(column_names, row)) for row in rows]
            entries = [row['company_domain'] for row in result_dict]

            cursor = connection.cursor(dictionary=True)

            ############ Chart Data without Preprocessing ############
            cursor.execute("SELECT * FROM  keybert_relevance_table_wo")
            keybert_relevance_table_wo_rows = cursor.fetchall()
            
            cursor.execute("SELECT * FROM  spacey_tfidf_table_wo")
            spacey_tfidf_table_wo_rows = cursor.fetchall()

            cursor.execute("SELECT * FROM  rake_unconstrained_table_wo")
            rake_unconstrained_table_wo_rows = cursor.fetchall()

            cursor.execute("SELECT * FROM  nltk_word_table_wo")
            nltk_word_table_wo_rows = cursor.fetchall()

            cursor.execute("SELECT * FROM  textrank_phrase_table_wo")
            textrank_phrase_table_wo_rows = cursor.fetchall()

            cursor.execute("SELECT * FROM  yake_phrase_table_wo")
            yake_phrase_table_wo_rows = cursor.fetchall()

            cursor.execute("SELECT * FROM  pke_word_table_wo")
            pke_word_table_wo_rows = cursor.fetchall()


            ############## Chart Data with Preprocessing #############
            cursor.execute("SELECT * FROM  keybert_relevance_table")
            keybert_relevance_table_rows = cursor.fetchall()
            
            cursor.execute("SELECT * FROM  spacey_tfidf_table")
            spacey_tfidf_table_rows = cursor.fetchall()

            cursor.execute("SELECT * FROM  rake_unconstrained_table")
            rake_unconstrained_table_rows = cursor.fetchall()

            cursor.execute("SELECT * FROM  nltk_word_table")
            nltk_word_table_rows = cursor.fetchall()

            cursor.execute("SELECT * FROM  textrank_phrase_table")
            textrank_phrase_table_rows = cursor.fetchall()

            cursor.execute("SELECT * FROM  yake_phrase_table")
            yake_phrase_table_rows = cursor.fetchall()

            cursor.execute("SELECT * FROM  pke_word_table")
            pke_word_table_rows = cursor.fetchall()
            

            cursor.close()
            connection.close()

            ############ Chart Dict without Preprocessing ############
            keybert_relevance_dict_wo = {}
            spacey_tfidf_dict_wo = {}
            rake_unconstrained_dict_wo = {}
            nltk_word_dict_wo = {}
            textrank_phrase_dict_wo = {}
            yake_phrase_dict_wo = {}
            pke_phrase_dict_wo = {}

            ############ Chart Dict with Preprocessing ############
            keybert_relevance_dict = {}
            spacey_tfidf_dict = {}
            rake_unconstrained_dict = {}
            nltk_word_dict = {}
            textrank_phrase_dict = {}
            yake_phrase_dict = {}
            pke_phrase_dict = {}

            for row in keybert_relevance_table_wo_rows:
                domain_id = row['domain_id']
                word = row['word']
                relevance = row['score']
                id = row['id']

                if domain_id not in keybert_relevance_dict_wo:
                    keybert_relevance_dict_wo[domain_id] = []

                keybert_relevance_dict_wo[domain_id].append({
                    'word': word,
                    'relevance': relevance,
                    'id': id
                })

            for row in spacey_tfidf_table_wo_rows:
                domain_id = row['domain_id']
                word = row['word']
                tfidf = row['score']
                id = row['id']

                if domain_id not in spacey_tfidf_dict_wo:
                    spacey_tfidf_dict_wo[domain_id] = []

                spacey_tfidf_dict_wo[domain_id].append({
                    'word': word,
                    'tfidf': tfidf,
                    'id': id
                })

            for row in rake_unconstrained_table_wo_rows:
                domain_id = row['domain_id']
                key_phrase = row['word']
                score = row['score']
                id = row['id']

                if domain_id not in rake_unconstrained_dict_wo:
                    rake_unconstrained_dict_wo[domain_id] = []

                rake_unconstrained_dict_wo[domain_id].append({
                    'key_phrase': key_phrase,
                    'score': score,
                    'id': id
                })

            for row in nltk_word_table_wo_rows:
                domain_id = row['domain_id']
                word = row['word']
                score = row['score']
                id = row['id']

                if domain_id not in nltk_word_dict_wo:
                    nltk_word_dict_wo[domain_id] = []

                nltk_word_dict_wo[domain_id].append({
                    'word': word,
                    'score': score,
                    'id': id
                })
            
            for row in textrank_phrase_table_wo_rows:
                domain_id = row['domain_id']
                phrase = row['word']
                score = row['score']
                id = row['id']

                if domain_id not in textrank_phrase_dict_wo:
                    textrank_phrase_dict_wo[domain_id] = []

                textrank_phrase_dict_wo[domain_id].append({
                    'phrase': phrase,
                    'score': score,
                    'id': id
                })

            for row in yake_phrase_table_wo_rows:
                domain_id = row['domain_id']
                phrase = row['word']
                score = row['score']
                id = row['id']

                if domain_id not in yake_phrase_dict_wo:
                    yake_phrase_dict_wo[domain_id] = []

                yake_phrase_dict_wo[domain_id].append({
                    'phrase': phrase,
                    'score': score,
                    'id': id
                })

            for row in pke_word_table_wo_rows:
                domain_id = row['domain_id']
                phrase = row['word']
                score = row['score']
                id = row['id']

                if domain_id not in pke_phrase_dict_wo:
                    pke_phrase_dict_wo[domain_id] = []

                pke_phrase_dict_wo[domain_id].append({
                    'phrase':phrase,
                    'score': score,
                    'id': id
                })

            for row in keybert_relevance_table_rows:
                domain_id = row['domain_id']
                word = row['word']
                relevance = row['score']
                id = row['id']

                if domain_id not in keybert_relevance_dict:
                    keybert_relevance_dict[domain_id] = []

                keybert_relevance_dict[domain_id].append({
                    'word': word,
                    'relevance': relevance,
                    'id': id
                })

            for row in spacey_tfidf_table_rows:
                domain_id = row['domain_id']
                word = row['word']
                tfidf = row['score']
                id = row['id']

                if domain_id not in spacey_tfidf_dict:
                    spacey_tfidf_dict[domain_id] = []

                spacey_tfidf_dict[domain_id].append({
                    'word': word,
                    'tfidf': tfidf,
                    'id': id
                })

            for row in rake_unconstrained_table_rows:
                domain_id = row['domain_id']
                key_phrase = row['word']
                score = row['score']
                id = row['id']

                if domain_id not in rake_unconstrained_dict:
                    rake_unconstrained_dict[domain_id] = []

                rake_unconstrained_dict[domain_id].append({
                    'key_phrase': key_phrase,
                    'score': score,
                    'id': id
                })

            for row in nltk_word_table_rows:
                domain_id = row['domain_id']
                word = row['word']
                score = row['score']
                id = row['id']

                if domain_id not in nltk_word_dict:
                    nltk_word_dict[domain_id] = []

                nltk_word_dict[domain_id].append({
                    'word': word,
                    'score': score,
                    'id': id
                })
            
            for row in textrank_phrase_table_rows:
                domain_id = row['domain_id']
                phrase = row['word']
                score = row['score']
                id = row['id']

                if domain_id not in textrank_phrase_dict:
                    textrank_phrase_dict[domain_id] = []

                textrank_phrase_dict[domain_id].append({
                    'phrase': phrase,
                    'score': score,
                    'id': id
                })

            for row in yake_phrase_table_rows:
                domain_id = row['domain_id']
                phrase = row['word']
                score = row['score']
                id = row['id']

                if domain_id not in yake_phrase_dict:
                    yake_phrase_dict[domain_id] = []

                yake_phrase_dict[domain_id].append({
                    'phrase': phrase,
                    'score': score,
                    'id': id
                })
            
            for row in pke_word_table_rows:
                domain_id = row['domain_id']
                phrase = row['word']
                score = row['score']
                id = row['id']

                if domain_id not in pke_phrase_dict:
                    pke_phrase_dict[domain_id] = []

                pke_phrase_dict[domain_id].append({
                    'phrase':phrase,
                    'score': score,
                    'id': id
                })

            if (entries):
                result_dict_json = json.dumps(result_dict)  # Convert result_dict to a JSON string
                return render_template('index.html', entries=entries, result_dict=result_dict_json,keybert_relevance_dict_wo=json.dumps(keybert_relevance_dict_wo),spacey_tfidf_dict_wo=json.dumps(spacey_tfidf_dict_wo),rake_unconstrained_dict_wo=json.dumps(rake_unconstrained_dict_wo),
                nltk_word_dict_wo=json.dumps(nltk_word_dict_wo), textrank_phrase_dict_wo=json.dumps(textrank_phrase_dict_wo),yake_phrase_dict_wo=json.dumps(yake_phrase_dict_wo),pke_phrase_dict_wo=json.dumps(pke_phrase_dict_wo),
                 keybert_relevance_dict=json.dumps(keybert_relevance_dict),spacey_tfidf_dict=json.dumps(spacey_tfidf_dict),rake_unconstrained_dict=json.dumps(rake_unconstrained_dict),
                nltk_word_dict=json.dumps(nltk_word_dict), textrank_phrase_dict=json.dumps(textrank_phrase_dict),yake_phrase_dict=json.dumps(yake_phrase_dict),pke_phrase_dict=json.dumps(pke_phrase_dict))
            else:
                return render_template('index.html', message="missing 'company_domain' column.")
        else:
            return render_template('index.html', message="Upload a valid CSV file!")
    else:
        return render_template('index.html', message="No file was uploaded.")



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
                else:
                    similarity_percentage = -1 

            elif algorithm == 'jaccard':
                if np.count_nonzero(ref_vector) > 0 and np.count_nonzero(vector) > 0:
                    ref_set = set(np.where(ref_vector > 0)[0])
                    vector_set = set(np.where(vector > 0)[0])
                    similarity = jaccard_similarity(ref_set, vector_set)
                    similarity_percentage = round(similarity * 100, 2)
                else:
                    similarity_percentage = -1

            site_results[company_domain][algo] = similarity_percentage

    cursor.close()
    connection.close()
    response_data = {
        'vocab': vocab,
        'site_results': site_results
    }
    return jsonify(response_data)



def jaccard_similarity(set1, set2):
    intersection = len(set(set1) & set(set2))
    union = len(set(set1) | set(set2))
    return intersection / union



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
    app.run(port=5089)