# app.py
from flask import Flask, render_template, request, jsonify
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from nltk.corpus import stopwords

app = Flask(__name__)

# Download NLTK stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Load the 20 Newsgroups dataset
newsgroups = fetch_20newsgroups(subset='all')
documents = newsgroups.data

# Perform LSA
vectorizer = TfidfVectorizer(stop_words=list(stop_words), max_features=5000)
X = vectorizer.fit_transform(documents)

n_components = 100
svd = TruncatedSVD(n_components=n_components)
lsa = svd.fit_transform(X)

def perform_search(query):
    query_vec = vectorizer.transform([query])
    query_lsa = svd.transform(query_vec)
    
    # Calculate cosine similarity
    similarity = cosine_similarity(lsa, query_lsa).flatten()
    
    # Sort documents by similarity
    sorted_indexes = np.argsort(similarity)[::-1]
    
    top_docs = []
    for idx in sorted_indexes[:5]:
        doc = documents[idx]
        score = similarity[idx]
        top_docs.append({"document": doc[:200] + "...", "score": float(score)})
    
    return top_docs

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.json['query']
    results = perform_search(query)
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)