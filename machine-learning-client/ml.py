# Using MEDIUM article
import speech_recognition as sr

recognizer = sr.Recognizer()

while True:
    try:
        print("Available microphones:")
        print(sr.Microphone.list_microphone_names())

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
        print("Decoded Text: {}".format(text))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
    except Exception as ex:
        print("Error during recognition:", ex)
        
    if "stop" in text:
        print("Exited")
        break