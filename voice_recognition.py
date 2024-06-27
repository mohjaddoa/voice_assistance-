import speech_recognition as sr 
import pyaudio
from gtts import gTTS
import playsound
import os
import streamlit as st


def get_audio():
    recorder = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.write("Say something ....")
            audio = recorder.listen(source)
            recorder.adjust_for_ambient_noise(source, duration=0.5)
        text = recorder.recognize_google(audio)
        # text = recorder.recognize_bing(audio)

        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

def speech(text):
    try:
        language = "en"
        output = gTTS(text=text, lang=language, slow=False)
        filename = "sounds/output.mp3"
        output.save(filename)
        playsound.playsound(filename)
        os.remove(filename)  # Deletes the audio file after playing
    except Exception as e:
        print(f"Error: {e}")

try:
    os.mkdir('sounds')
except FileExistsError:
    pass  # Directory already exists

# speech('This is AI assistance, How can I help You?')
# text = get_audio()
# if text:
#     speech("You said " + text)
