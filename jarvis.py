"""Mahi Jarvis - voice-first desktop assistant.

Run locally on the laptop. Speak a command; Jarvis listens, performs the
requested action, and replies with speech. No chat UI is required.
"""

import os
import platform
import subprocess
import webbrowser
from urllib.parse import quote_plus

import pyttsx3
import speech_recognition as sr


class MahiJarvis:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts = pyttsx3.init()
        self.tts.setProperty("rate", 175)
        self.running = True

    def speak(self, text):
        print("Mahi:", text)
        self.tts.say(text)
        self.tts.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.6)
            print("Listening...")
            audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=12)
        try:
            return self.recognizer.recognize_google(audio, language="en-IN")
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            self.speak("Speech recognition is unavailable right now.")
            return ""

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
        webbrowser.open(url)
        self.speak(f"Opening {song} on {site}.")

    def open_target(self, target):
        target = target.strip()
        sites = {
            "youtube": "https://www.youtube.com/",
            "spotify": "https://open.spotify.com/",
            "google": "https://www.google.com/",
            "github": "https://github.com/",
            "instagram": "https://www.instagram.com/",
        }
        if target.lower() in sites:
            webbrowser.open(sites[target.lower()])
            self.speak(f"Opening {target}.")
            return
        if target.startswith(("http://", "https://")):
            webbrowser.open(target)
            self.speak("Opening the website.")
            return
        self.run_command(target)

    def run_command(self, command):
        command = command.strip()
        if not command:
            self.speak("Please tell me what to run.")
            return
        try:
            subprocess.Popen(command, shell=True)
            self.speak("Done. I started that command.")
        except Exception as exc:
            self.speak(f"I couldn't start it: {exc}")

    def handle(self, request):
        text = request.strip()
        lower = text.lower()
        if not text:
            self.speak("I didn't catch that. Please say the command again.")
            return

        if lower in {"exit", "quit", "shutdown jarvis", "close jarvis", "goodbye"}:
            self.speak("Goodbye. Shutting down.")
            self.running = False
            return

        if lower.startswith("play "):
            rest = text[5:].strip()
            low = rest.lower()
            if " on spotify" in low:
                self.play_song(rest[:low.rfind(" on spotify")], "spotify")
            elif " on youtube" in low:
                self.play_song(rest[:low.rfind(" on youtube")], "youtube")
            else:
                self.play_song(rest)
            return

        if lower.startswith("song "):
            self.play_song(text[5:])
            return

        if lower.startswith("open "):
            self.open_target(text[5:])
            return

        if lower.startswith("search "):
            query = text[7:].strip()
            if query:
                webbrowser.open("https://www.google.com/search?q=" + quote_plus(query))
                self.speak(f"Searching for {query}.")
            else:
                self.speak("Tell me what you want to search.")
            return

        if lower.startswith("command "):
            self.run_command(text[8:])
            return

        if lower.startswith("run "):
            self.run_command(text[4:])
            return

        # Voice command-first behavior: any other spoken phrase is treated
        # as the user's requested laptop command.
        self.run_command(text)

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
                self.speak("I can't access the microphone. Please check the microphone permission.")
                self.running = False


if __name__ == "__main__":
    MahiJarvis().start()
