import os
import pandas as pd



"""# Loading csv files for similarity analysis (using the nltk files with preprocessing"""


folder_path = '/content/drive/MyDrive/ML Project 1/secondDraft/Results/with_preprocessing/nltk/'
os.chdir(folder_path)

files = [file for file in os.listdir() if file.endswith('.csv')]

files

files.remove('grunau.com.csv')
files

dataFrameDict = {}
for file in files:
  website = file.replace(".csv", "")
  dataFrameDict[website] = pd.read_csv(file)
  dataFrameDict[website] = dataFrameDict[website].dropna(subset=['Word'])

dataFrameDict

dataFrameDict['flfireprevention.com'].isna().sum()

# dataFrameDict['flfireprevention.com'] = dataFrameDict['flfireprevention.com'].dropna(subset=['Word'])

"""# Keyword extraction on the entire merged corpus"""

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

from collections import defaultdict

mergedDict = {}

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(mainDictTextCombined)

# Get feature names (keywords) from the vectorizer
feature_names = vectorizer.get_feature_names_out()

# Create a dictionary to store keywords and their TF-IDF scores
keyword_scores = {}
for idx, keyword in enumerate(feature_names):
    keyword_scores[keyword] = tfidf_matrix[0, idx]

word_count = defaultdict(int)
for document_idx in range(len(mainDictTextCombined)):
    for word_idx, keyword in enumerate(feature_names):
        # Get the TF-IDF value for the current word in the current document
        tfidf_value = tfidf_matrix[document_idx, word_idx]
        # If the TF-IDF value is non-zero, update the word count
        if tfidf_value > 0:
            word_count[keyword] += 1

mean_keyword_scores = {}
for feature_idx, feature_name in enumerate(feature_names):
    mean_keyword_scores[feature_name] = tfidf_matrix[:, feature_idx].mean()

# Sort keywords based on TF-IDF scores in descending order
sorted_keywords = sorted(keyword_scores.items(), key=lambda x: x[1], reverse=True)

mean_sorted_keywords = sorted(mean_keyword_scores.items(), key=lambda x: x[1], reverse=True)

word_count

word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

word_count

sorted_keywords[:20]

mean_sorted_keywords

"""# defining the vocabulary"""

vocab = ['system', 'fire', 'servic', 'protect', 'secur', 'alarm', 'extinguish', 'emerg', 'provid', 'safeti', 'suppress', 'solut', \
         'communic', 'inspect', 'design', 'control', 'custom', 'maintain', 'build', 'instal', 'life', 'qualiti', 'monitor', \
         'time', 'need', 'sprinkler', 'safe', 'hazard', 'repair']

#('compliant', 7), ('coverag', 7), ('weld', 0.03821743615219447), ('facil', 0.037614701930036326),('integr', 0.03364754618479582),
#('prevent', 0.026370621767525897), ('detect', 0.026163357996416094), ('pipe', 0.026130083281141765), ('mainten', 0.02609573354334175),
#('properti', 0.022903589793425723), ('ensur', 0.022180407469347768), ('fighter', 0.021383649356995597), ('station', 0.019276358161324045),
#('support', 0.018898594455086258),

len(vocab)

len(set(vocab))

from collections import Counter
Counter(vocab)



"""**saving the vocabulary**"""

import json

with open("/content/drive/MyDrive/ML Project 1/secondDraft/Results/vocab", "w") as fp:
  json.dump(vocab, fp)

with open("/content/drive/MyDrive/ML Project 1/secondDraft/Results/vocab", "r") as fp:
  vocab_loaded = json.load(fp)
vocab_loaded

vocab == vocab_loaded

['a','c'] == ['c', 'a']

['a','c'] == ['a', 'c']

"""# Jaccard similarity"""

def jaccard_similarity(set1, set2):
    intersection = len(set(set1) & set(set2))
    union = len(set(set1) | set(set2))
    return intersection / union

jaccard_scores=[]
for k1,v1 in dataFrameDict.items():
  for k2,v2 in dataFrameDict.items():
    #if k1!=k2:
      df1_words = set(v1['Word'])
      df2_words = set(v2['Word'])
      similarity = jaccard_similarity(df1_words, df2_words)
      print("Jaccard Similarity:", k1, ' len: ', len(v1), '\t\t', k2, ' len: ', len(v2) , '\t\t', similarity*100)
      jaccard_scores.append([k1, len(v1), k2, len(v2), similarity*100])

jaccard_scores





# testing with average
# for k1,v1 in dataFrameDict.items():
#   for k2,v2 in dataFrameDict.items():
#     #if k1!=k2:
#     l1=len(v1)
#     l2=len(v2)
#     avg=(l1+l2)//2
#     l1=min(avg,l1)
#     l2=min(avg,l2)
#     df1_words = set(v1['Word'][:l1])
#     df2_words = set(v2['Word'][:l2])
#     similarity = jaccard_similarity(df1_words, df2_words)
#     print("Jaccard Similarity:", k1, ' len: ', len(v1), '\t', k2, ' len: ', len(v2) , '\t', similarity*100)



#testing with min
# for k1,v1 in dataFrameDict.items():
#   for k2,v2 in dataFrameDict.items():
#     #if k1!=k2:
#     l1=len(v1)
#     l2=len(v2)
#     mn=min(l1,l2)
#     df1_words = set(v1['Word'][:mn])
#     df2_words = set(v2['Word'][:mn])
#     similarity = jaccard_similarity(df1_words, df2_words)
#     print("Jaccard Similarity:", k1, ' len: ', len(v1), '\t', k2, ' len: ', len(v2) , '\t', similarity*100)











"""# cosine similarity"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from numpy.linalg import norm

# for w,v in mean_sorted_keywords:
#   if w=='fire':
#     print(v)

"""**with the mean tfidf vector**"""

word_freq_dict_ref = dict(mean_sorted_keywords)
ref_vector = [word_freq_dict_ref.get(word, 0) for word in vocab]

ref_vector

cosine_scores = []
#cosine_scores = []
mincossim=100
for k,v in dataFrameDict.items():

  word_freq_dict = dict(zip(v['Word'], v['Score']))
  vector = [word_freq_dict.get(word, 0) for word in vocab]
  vector = np.array(vector, dtype=np.float64)
  #print(vector2)

  cosine_similarity = round(np.dot(ref_vector, vector) / (norm(ref_vector) * norm(vector)),4)
  print(k, '\t', cosine_similarity*100)
  cosine_scores.append([k,cosine_similarity*100])
  mincossim=min(mincossim,cosine_similarity)

print(mincossim)
#cosine_scores

cosine_scores

cosine_scores_sorted = sorted(cosine_scores, key=lambda x: x[1])

"""**plot with the reference vector**"""

import matplotlib.pyplot as plt

# Your data in the form of a list

# Extracting website names and percentages from the list
websites = []
percentages = []

for item in cosine_scores_sorted:
    websites.append(item[0])
    percentages.append(item[1])  # Converting percentage to float

# Plotting the bar chart
plt.figure(figsize=(10, 6))

# Bar color logic: bars with percentages below 50 will be red, others blue
colors = ['red' if percentage < 51.5 else 'skyblue' for percentage in percentages]

bars = plt.bar(websites, percentages, color=colors)
plt.xlabel('Websites')
plt.ylabel('Percentages')
plt.title('Similarity to the reference vector taken from the mean of tfidf values on the entire corpus')
plt.xticks(rotation=90)  # Rotate x-axis labels for better visibility

for bar, percentage in zip(bars, percentages):
    plt.text(bar.get_x() + bar.get_width() / 2 - 0.15, bar.get_height() + 1, f'{percentage:.2f}%', ha='center')

plt.tight_layout()  # Ensure labels are not cut off in the output

plt.savefig('/content/drive/MyDrive/ML Project 1/secondDraft/Results/similarity_scores/with_reference/barplot.png', bbox_inches='tight')

plt.show()









"""**with each other**"""

cosine_scores_dict = {}
#cosine_scores = []
mincossim=100
for k1,v1 in dataFrameDict.items():
  cosine_scores = []
  for k2,v2 in dataFrameDict.items():
    word_freq_dict1 = dict(zip(v1['Word'], v1['Score']))
    vector1 = [word_freq_dict1.get(word, 0) for word in vocab]
    vector1 = np.array(vector1, dtype=np.float64)
    #print(vector1)

    word_freq_dict2 = dict(zip(v2['Word'], v2['Score']))
    vector2 = [word_freq_dict2.get(word, 0) for word in vocab]
    vector2 = np.array(vector2, dtype=np.float64)
    #print(vector2)

    cosine_similarity = round(np.dot(vector1, vector2) / (norm(vector1) * norm(vector2)),4)
    print(k1, '\t', k2, '\t', cosine_similarity*100)
    cosine_scores.append([k2,cosine_similarity*100])
    mincossim=min(mincossim,cosine_similarity)

  cosine_scores_dict[k1] = cosine_scores

mincossim*100

#!python --version

sorted(cosine_scores, key=lambda x:x[2], reverse=True)



cosine_scores_dict

cosine_scores_dict_sorted={}
for k,v in cosine_scores_dict.items():
  cosine_scores_dict_sorted[k] = sorted(v, key=lambda x:x[1], reverse=True)

cosine_scores_dict_sorted



"""# Plotting the cosine similarity between the clients"""

#!pip install matplotlib

import matplotlib.pyplot as plt
folder_path = '/content/drive/MyDrive/ML Project 1/secondDraft/Results/similarity_scores/for_among_distributors/'
# Extracting names and corresponding values for each key
for key, value in cosine_scores_dict_sorted.items():
    names = [item[0] for item in value]
    values = [item[1] for item in value]

    # Creating a bar plot for each key with clickable names
    plt.figure(figsize=(12, 7))
    plt.barh(names, values, color='skyblue')
    plt.xlabel('Percentage')
    plt.title(key)

    # Making names clickable
    for i, name in enumerate(names):
        plt.text(values[i], i, f' {values[i]}%', va='center')

    plt.gca().invert_yaxis()  # Invert y-axis to display the highest percentage at the top
    plt.savefig(folder_path + f'{key}_lineplot.png', bbox_inches='tight')
    plt.show()

# !pip install plotly

# import plotly.express as px

# # Create an empty list to store the data for the plot
# plot_data = []

# # Extracting names and corresponding values for each key
# for key, value in cosine_scores_dict_sorted.items():
#     names = [item[0] for item in value]
#     values = [item[1] for item in value]

#     # Create a dictionary for each key to store data for the plot
#     plot_dict = {'Key': key, 'Names': names, 'Values': values}
#     plot_data.append(plot_dict)

# # Create a DataFrame from the list of dictionaries
# import pandas as pd
# df = pd.DataFrame(plot_data)

# # Create an interactive bar plot using plotly express
# fig = px.bar(df, x='Values', y='Names', orientation='h', color='Key',
#              labels={'Values': 'Percentage', 'Names': 'Company Names'},
#              title='Clickable Bar Plot with Company Names')

# # Show the plot
# fig.show()

"""# similarity for wiza sites"""

folder_path = '/content/drive/MyDrive/ML Project 1/secondDraft/Results/identifying_potentials/nltk/'
os.chdir(folder_path)

files = [file for file in os.listdir() if file.endswith('.csv')]

len(files)

files.remove('hd-home.com.csv')

len(files)

wizadataFrameDict = {}
for file in files:
  website = file.replace(".csv", "")
  wizadataFrameDict[website] = pd.read_csv(file)
  wizadataFrameDict[website] = wizadataFrameDict[website].dropna(subset=['Word'])

wizadataFrameDict

wiza_cosine_scores = []
#cosine_scores = []
count_above_65=0
for k,v in wizadataFrameDict.items():

  word_freq_dict = dict(zip(v['Word'], v['Score']))
  vector = [word_freq_dict.get(word, 0) for word in vocab]
  vector = np.array(vector, dtype=np.float64)
  #print(vector2)

  cosine_similarity = round(np.dot(ref_vector, vector) / (norm(ref_vector) * norm(vector)),4)
  print(k, '\t', cosine_similarity*100)
  wiza_cosine_scores.append([k,cosine_similarity*100])
  if cosine_similarity*100 > 65:
    count_above_65+=1

print(count_above_65)
#cosine_scores

wiza_cosine_scores

wiza_cosine_scores_sorted = sorted(wiza_cosine_scores, key=lambda x: x[1],reverse=True)
wiza_cosine_scores_sorted

import csv

# Path to save the CSV file
csv_file_path = '/content/drive/MyDrive/ML Project 1/secondDraft/Results/similarity_scores/wiza_with_reference/wiza_sim_ref.csv'

# Writing the data to the CSV file
with open(csv_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Website', 'Percentage'])  # Writing header
    csv_writer.writerows(wiza_cosine_scores_sorted)  # Writing data rows



"""**plotting**"""

import matplotlib.pyplot as plt

# Your data in the form of a list

# Extracting website names and percentages from the list
websites = []
percentages = []

for item in wiza_cosine_scores_sorted:
    websites.append(item[0])
    percentages.append(item[1])  # Converting percentage to float

# Plotting the bar chart
plt.figure(figsize=(15, 12))

# Bar color logic: bars with percentages below 50 will be red, others blue
colors = ['red' if percentage < 65 else 'skyblue' for percentage in percentages]

plt.bar(websites, percentages, color=colors)
plt.xlabel('Websites')
plt.ylabel('Percentages')
plt.title('Similarity of wiza sites to the reference vector taken from the mean of tfidf values on the entire distributor corpus')
plt.xticks(rotation=90)  # Rotate x-axis labels for better visibility

# for bar, percentage in zip(bars, percentages):
#     plt.text(bar.get_x() + bar.get_width() / 2 - 0.15, bar.get_height() + 1, f'{percentage:.2f}%', ha='center')

# Adding a dotted line at the 65% cutoff
plt.axhline(y=65, color='gray', linestyle='--', linewidth=1)

plt.tight_layout()  # Ensure labels are not cut off in the output

plt.savefig('/content/drive/MyDrive/ML Project 1/secondDraft/Results/similarity_scores/wiza_with_reference/barplot.png', bbox_inches='tight')

plt.show()



"""# wiza_with_all_distributors"""

cosine_scores_dict = {}
cosine_scores_dict_avg = {}
#cosine_scores = []
mincossim=100
for k1,v1 in wizadataFrameDict.items():
  cosine_scores = []
  sm=0
  cnt=0
  word_freq_dict1 = dict(zip(v1['Word'], v1['Score']))
  vector1 = [word_freq_dict1.get(word, 0) for word in vocab]
  vector1 = np.array(vector1, dtype=np.float64)
  #print(vector1)
  for k2,v2 in dataFrameDict.items():
    word_freq_dict2 = dict(zip(v2['Word'], v2['Score']))
    vector2 = [word_freq_dict2.get(word, 0) for word in vocab]
    vector2 = np.array(vector2, dtype=np.float64)
    #print(vector2)

    cosine_similarity = round(np.dot(vector1, vector2) / (norm(vector1) * norm(vector2)),4)
    #print(k1, '\t', k2, '\t', cosine_similarity*100)
    cosine_scores.append([k2,cosine_similarity*100])
    #mincossim=min(mincossim,cosine_similarity)
    sm+=cosine_similarity*100
    cnt+=1
  cosine_scores_dict[k1] = sorted(cosine_scores, key=lambda x:x[1], reverse=True)
  cosine_scores_dict_avg[k1] = sm/cnt

  #cosine_scores_dict[k1] = cosine_scores

cosine_scores_dict_avg

cosine_scores_dict_avg = dict(sorted(cosine_scores_dict_avg.items(), key=lambda item: item[1], reverse=True))
cosine_scores_dict_avg

"""**saving dict**"""

csv_file_path = '/content/drive/MyDrive/ML Project 1/secondDraft/Results/similarity_scores/wiz_with_all_distributors/avg.csv'

# Writing the dictionary to the CSV file
with open(csv_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Key', 'Value'])  # Writing header
    for key, value in cosine_scores_dict_avg.items():
        csv_writer.writerow([key, value])  # Writing key-value pairs

cosine_scores_dict

# Path to save the CSV file
csv_file_path = '/content/drive/MyDrive/ML Project 1/secondDraft/Results/similarity_scores/wiz_with_all_distributors/results_with_every_distributor.csv'

# Writing the dictionary to the CSV file
with open(csv_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Website', 'Comparedwebsite', 'Percentage'])  # Writing header
    for main_website, subwebsites in cosine_scores_dict.items():
        for subwebsite, percentage in subwebsites:
            csv_writer.writerow([main_website, subwebsite, percentage])  # Writing data rows



"""**ploting**"""

import matplotlib.pyplot as plt

# Your data in the form of a list

# Extracting website names and percentages from the list
websites = []
percentages = []

for k,v in cosine_scores_dict_avg.items():
    websites.append(k)
    percentages.append(v)  # Converting percentage to float

# Plotting the bar chart
plt.figure(figsize=(16, 9))

# Bar color logic: bars with percentages below 50 will be red, others blue
colors = ['red' if percentage < 52 else 'skyblue' for percentage in percentages]

bars = plt.bar(websites, percentages, color=colors)
plt.xlabel('Websites')
plt.ylabel('Percentages')
plt.title('Average Similarity after comparing to the 15 distributors')
plt.xticks(rotation=90)  # Rotate x-axis labels for better visibility

# for bar, percentage in zip(bars, percentages):
#     plt.text(bar.get_x() + bar.get_width() / 2 - 0.15, bar.get_height() + 1, f'{percentage:.2f}%', ha='center')

plt.tight_layout()  # Ensure labels are not cut off in the output

plt.axhline(y=52, color='gray', linestyle='--', linewidth=1)

plt.savefig('/content/drive/MyDrive/ML Project 1/secondDraft/Results/similarity_scores/wiz_with_all_distributors/barplot.png', bbox_inches='tight')

plt.show()