"""Machine learning client for similarity recommendation."""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('wordnet')
nltk.download('stopwords')

class MLC:  # pylint: disable=too-few-public-methods
    """This is the Machine Learning Client class"""

    def __init__(self, descriptions):
        """Takes data and fits a tf-idf vectorizer with it"""
        self.tfidf = TfidfVectorizer()
        lemmatized_descriptions = [self.lemmatize_text(text) for text in descriptions]
        self.tfidf_matrix = self.tfidf.fit_transform(lemmatized_descriptions)

    def lemmatize_text(self, text):
        """Lemmatizes the input text using NLTK's WordNet Lemmatizer"""
        lemmatizer = WordNetLemmatizer()
        stop_words = set(stopwords.words('english'))
        
        words = text.split()
        lemmatized_text = " ".join([
            lemmatizer.lemmatize(word.lower()) for word in words if word.lower() not in stop_words
        ])
        
        return lemmatized_text

    def get_recommendation(self, description, df, threshold=0.1):
        """Returns movies sorted by similarity to provided description."""
        lemmatized_description = self.lemmatize_text(description)
        desc_vector = self.tfidf.transform([lemmatized_description])
        cosine_sim = linear_kernel(desc_vector, self.tfidf_matrix).flatten()

        sim_scores = [
            (i, score) for i, score in enumerate(cosine_sim) if score >= threshold
        ]
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        result_df = df.iloc[[i for i, _ in sim_scores]].copy()
        result_df["similarity"] = [score for _, score in sim_scores]

        if result_df.empty:
            return "No match found"

        return result_df[["title", "similarity", "description"]]