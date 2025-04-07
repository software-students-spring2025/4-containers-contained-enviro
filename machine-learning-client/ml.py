# Using MEDIUM article as base for speech recognition
import speech_recognition as sr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd

movies = pd.read_csv('movies.csv')

recognizer = sr.Recognizer()

try:
    # print("Available microphones:")
    # print(sr.Microphone.list_microphone_names())
    with sr.Microphone() as source:
        print("Adjusting noise...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Recording for 4 seconds...")
        recorded_audio = recognizer.listen(source, timeout=4)
        print("Done recording.")
except Exception as ex:
    print("Error during recording:", ex)
    print("Please check your microphone settings.")

try:
    print("Recognizing the text...")
    text = recognizer.recognize_google(recorded_audio, language="en-US")
    text = text.lower()
    print("Decoded Text: {}".format(text))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand the audio.")
except sr.RequestError:
    print("Could not request results from Google Speech Recognition service.")
except Exception as ex:
    print("Error during recognition:", ex)

tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(movies['description'].values.astype('U'))

def get_recommendations_from_description(description, tfidf, tfidf_matrix, df):
    desc_vector = tfidf.transform([description])
    cosine_sim = linear_kernel(desc_vector, tfidf_matrix).flatten()
    sim_scores = list(enumerate(cosine_sim))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sim_scores[:10]]
    return df[['title', 'star_rating', 'description']].iloc[top_indices]

recommendations = get_recommendations_from_description(text, tfidf, tfidf_matrix, movies)
print(recommendations)