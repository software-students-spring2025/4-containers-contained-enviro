"""Machine learning module for speech recognition and similarity prediction."""
import speech_recognition as sr
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

recognizer = sr.Recognizer()

# print("Available microphones:")
# print(sr.Microphone.list_microphone_names())
try:
    with sr.Microphone() as source:
        print("Adjusting noise...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Recording for 4 seconds...")
        recorded_audio = recognizer.listen(source, timeout=4)
        print("Done recording.")
except sr.WaitTimeoutError:
    print("listening timed out while waiting for phrase to start")

try:
    print("Recognizing the text...")
    text = recognizer.recognize_google(recorded_audio, language="en-US")
    text = text.lower()
    print(f"Decoded Text: {text}")
    recommendations = get_recommendations_from_description(text, v, v_matrix, movies)
    print(recommendations)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand the audio.")
except sr.RequestError:
    print("Could not request results from Google Speech Recognition service.")
except NameError as ne:
    print(ne)
