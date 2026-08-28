import webbrowser

import pyttsx3
import requests
import speech_recognition as sr
from google import genai

import Library
import os
from dotenv import load_dotenv


load_dotenv()
recognizer = sr.Recognizer()
newsapi = os.getenv("NEWS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

def speak(text, Jarvis_Type=True):
    if(Jarvis_Type == False):
        print("Jarvis: ", text)
    else:
        print(text)

    engine = pyttsx3.init("sapi5")
    engine.setProperty("rate", 185)
    engine.say(text)
    engine.runAndWait()

def ask_gemini(question):
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=question
        )

        return response.text

    except (ValueError, RuntimeError) as e:
        print("Gemini Error:", e)
        return "Sorry, I am having trouble connecting to my AI system."

def Process_Command(c):
    command = c.lower()

    if "open google" in command:
        webbrowser.open("https://google.com")
    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")
    elif command.startswith("play"):
        song = command[5:].strip()
        if song in Library.music:
            webbrowser.open(Library.music[song])
        else:
            speak("Sorry, I don't have that song in my library.")
    elif "news" in command:
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apikey={newsapi}", timeout=10)

            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])

                if not articles:
                    speak("I couldn't find any news right now.")
                else:
                    for article in articles:
                        title = article.get("title")
                        if title:
                            speak(title)
            else:
                speak("Sorry, I couldn't retrieve the news.")

        except requests.RequestException as e:
            print("News Error:", e)
            speak("Sorry, I couldn't connect to the news service.")

    else:
        response = ask_gemini(c)
        speak(response)

if __name__ == "__main__":


    speak("Initializing Jarvis.........")


    # Second sentence — has "Jarvis:"
    speak("What is Your Name ? - Please Enter Your Name Here.........", False)

    # Ask for name
    name = input("Name: ")

    # Greeting
    speak(f"Hi {name}, I am 'Jarvis', Please Activate me First for Assist by Saying my Name: 'Jarvis'", False)

    while True:



        print("Recognizing........")
        try:
            with sr.Microphone() as source:
                print("Adjusting for background noise...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)

                print("Listening.........")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            text = recognizer.recognize_google(audio)
            if(text.lower() == "jarvis"):
                print("You: ", text)
                speak("Yeah")
                with sr.Microphone() as source:
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
                    text = recognizer.recognize_google(audio)
                    print("You: ", text.lower())
                    Process_Command(text)
            else:
                print("Jarvis not activated.")
        except sr.WaitTimeoutError:
            print("Listening timed out.")

        except sr.UnknownValueError:
            print("I couldn't understand what you said.")

        except sr.RequestError as e:
            print("Speech recognition service error:", e)
