"""Machine learning client for similarity recommendation."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd

movies = pd.read_csv('movies.csv')

v = TfidfVectorizer()
v_matrix = v.fit_transform(movies['description'].values.astype('U'))

def get_recommendations_from_description(description, tfidf, tfidf_matrix, df, threshold=0.1):
    """Returns movies sorted by similarity to provided description."""
    desc_vector = tfidf.transform([description])
    cosine_sim = linear_kernel(desc_vector, tfidf_matrix).flatten()
    sim_scores = [(i, score) for i, score in enumerate(cosine_sim) if score >= threshold]
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    result_df = df.iloc[[i for i, _ in sim_scores]].copy()
    result_df['similarity'] = [score for _, score in sim_scores]

    return result_df[['title', 'similarity', 'description']]
