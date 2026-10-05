"""Mahi Jarvis — polished voice-first desktop assistant.

The assistant is intentionally allow-listed for laptop actions. This avoids
turning every misunderstood sentence into an arbitrary shell command.
"""

import os
import platform
import subprocess
import webbrowser
from urllib.parse import quote_plus

import pyttsx3
import speech_recognition as sr


class MahiJarvis:
    SITES = {
        "youtube": "https://www.youtube.com/",
        "spotify": "https://open.spotify.com/",
        "google": "https://www.google.com/",
        "github": "https://github.com/",
        "instagram": "https://www.instagram.com/",
    }

    APPS_WINDOWS = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "calc": "calc.exe",
        "paint": "mspaint.exe",
        "file explorer": "explorer.exe",
        "explorer": "explorer.exe",
    }

    def __init__(self, recognizer=None, tts=None):
        self.recognizer = recognizer or sr.Recognizer()
        self.tts = tts or pyttsx3.init()
        self.tts.setProperty("rate", 175)
        self.running = True

    def speak(self, text):
        print("Mahi:", text)
        self.tts.say(text)
        self.tts.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=12)
        try:
            return self.recognizer.recognize_google(audio, language="en-IN")
        except sr.UnknownValueError:
            self.speak("I didn't catch that. Please say it again.")
            return ""
        except sr.RequestError:
            self.speak("Speech recognition is unavailable right now.")
            return ""

    def open_url(self, url, message):
        try:
            webbrowser.open(url)
            self.speak(message)
        except Exception:
            self.speak("I couldn't open that right now.")

    def play_song(self, song, service="youtube"):
        song = song.strip()
        if not song:
            self.speak("Tell me the song name.")
            return
        if service == "spotify":
            url = "https://open.spotify.com/search/" + quote_plus(song)
            site = "Spotify"
        else:
            url = "https://www.youtube.com/results?search_query=" + quote_plus(song)
            site = "YouTube"
        self.open_url(url, f"Opening {song} on {site}.")

    def open_target(self, target):
        target = target.strip()
        key = target.lower()
        if key in self.SITES:
            self.open_url(self.SITES[key], f"Opening {target}.")
            return
        if key in self.APPS_WINDOWS and platform.system() == "Windows":
            try:
                subprocess.Popen(self.APPS_WINDOWS[key], shell=False)
                self.speak(f"Opening {target}.")
            except OSError:
                self.speak(f"I couldn't open {target}.")
            return
        if target.startswith(("http://", "https://")):
            self.open_url(target, "Opening the website.")
            return
        self.speak("I can open supported websites and common Windows apps. Try saying open YouTube or open calculator.")

    def search(self, query):
        query = query.strip()
        if not query:
            self.speak("Tell me what you want to search.")
            return
        self.open_url("https://www.google.com/search?q=" + quote_plus(query),
                      f"Searching for {query}.")

    def handle(self, request):
        text = request.strip()
        lower = text.lower()
        if not text:
            self.speak("I didn't catch that. Please say the command again.")
            return

        if lower in {"exit", "quit", "shutdown jarvis", "close jarvis", "goodbye", "stop listening"}:
            self.speak("Goodbye. Shutting down.")
            self.running = False
            return

        if lower.startswith("play "):
            rest = text[5:].strip()
            low = rest.lower()
            for marker, service in ((" on spotify", "spotify"), (" on youtube", "youtube")):
                if marker in low:
                    self.play_song(rest[:low.rfind(marker)], service)
                    return
            self.play_song(rest)
            return

        if lower.startswith("song "):
            self.play_song(text[5:])
            return

        if lower.startswith("open "):
            self.open_target(text[5:])
            return

        if lower.startswith("search "):
            self.search(text[7:])
            return

        if lower in {"what can you do", "help", "commands"}:
            self.speak("You can ask me to play a song, open a website or Windows app, search Google, or stop listening.")
            return

        if lower in {"hello", "hi", "hey", "good morning", "good evening"}:
            self.speak("Hello! I'm Mahi. What would you like me to do?")
            return

        self.speak("I can help with songs, websites, Google searches, and supported laptop apps. Please say open, play, or search followed by what you need.")

    def start(self):
        self.speak("Hi, I'm Mahi. I'm ready for your voice command.")
        while self.running:
            try:
                request = self.listen()
                if request:
                    print("You:", request)
                    self.handle(request)
            except sr.WaitTimeoutError:
                self.speak("I didn't hear a command.")
            except KeyboardInterrupt:
                self.running = False
            except OSError:
                self.speak("I can't access the microphone. Please check microphone permission.")
                self.running = False


if __name__ == "__main__":
    MahiJarvis().start()
