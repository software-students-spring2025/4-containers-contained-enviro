"""Machine learning client for similarity recommendation."""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


class MLC:  # pylint: disable=too-few-public-methods
    """This is the Machine Learning Client class"""

    def __init__(self, descriptions):
        """Takes data and fits a tf-idf vectorizer with it"""
        self.tfidf = TfidfVectorizer()
        self.tfidf_matrix = self.tfidf.fit_transform(descriptions)

    def get_recommendations(self, description, df, threshold=0.1):
        """Returns movies sorted by similarity to provided description."""
        desc_vector = self.tfidf.transform([description])
        cosine_sim = linear_kernel(desc_vector, self.tfidf_matrix).flatten()
        sim_scores = [
            (i, score) for i, score in enumerate(cosine_sim) if score >= threshold
        ]
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        result_df = df.iloc[[i for i, _ in sim_scores]].copy()
        result_df["similarity"] = [score for _, score in sim_scores]

        return result_df[["title", "similarity", "description"]]
