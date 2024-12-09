import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

VERSION = '0.1'
threshold = 0.6 

def find(user_input, commands):
    keys = list(commands.keys())
    
    vectorizer = TfidfVectorizer().fit(keys)
    key_vectors = vectorizer.transform(keys)
    user_vector = vectorizer.transform([user_input])
    
    similarities = cosine_similarity(user_vector, key_vectors).flatten()
    best_match_index = np.argmax(similarities)
    confidence = similarities[best_match_index]
    
    if confidence >= threshold:
        return keys[best_match_index], commands[keys[best_match_index]], confidence
    else:
        return None, None, confidence
