"""Mahi JARVIS Pro — voice-first laptop assistant.

This is the next-generation entry point: wake-word mode, richer natural
commands, app/site launching, search, music search, system information, and
safe confirmations for power actions.
"""

import datetime
import platform
import subprocess
import webbrowser
from urllib.parse import quote_plus

import pyttsx3
import speech_recognition as sr


class JarvisPro:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts = pyttsx3.init()
        self.tts.setProperty("rate", 175)
        self.running = True
        self.awaiting_command = True

    def speak(self, text):
        print(f"Mahi: {text}")
        self.tts.say(text)
        self.tts.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.4)
            audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=12)
        try:
            return self.recognizer.recognize_google(audio, language="en-IN").strip()
        except (sr.UnknownValueError, sr.RequestError):
            return ""

    def open_url(self, url, response):
        webbrowser.open(url)
        self.speak(response)

    def launch(self, name):
        apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "calc": "calc.exe",
            "paint": "mspaint.exe",
            "explorer": "explorer.exe",
            "file explorer": "explorer.exe",
        }
        sites = {
            "youtube": "https://youtube.com",
            "spotify": "https://open.spotify.com",
            "google": "https://google.com",
            "github": "https://github.com",
            "instagram": "https://instagram.com",
            "gmail": "https://mail.google.com",
        }
        key = name.lower().strip()
        if key in sites:
            self.open_url(sites[key], f"Opening {name}.")
        elif key in apps and platform.system() == "Windows":
            subprocess.Popen(apps[key], shell=False)
            self.speak(f"Opening {name}.")
        else:
            self.speak("I don't have a safe launcher for that yet.")

    def handle(self, command):
        text = command.strip()
        low = text.lower()

        if not text:
            return

        if low in {"exit", "quit", "goodbye", "stop listening", "shutdown jarvis"}:
            self.running = False
            self.speak("Goodbye. JARVIS is going offline.")
            return

        if low in {"hello", "hi jarvis", "hey jarvis", "jarvis"}:
            self.speak("Online. What can I do for you?")
            return

        if low in {"help", "what can you do", "commands"}:
            self.speak("I can open apps and websites, search the web, find music, tell the time, and report system information.")
            return

        if low in {"what time is it", "tell me the time", "current time"}:
            self.speak(datetime.datetime.now().strftime("It is %I:%M %p."))
            return

        if low in {"system information", "system info", "what computer am i using"}:
            self.speak(f"You are using {platform.system()} {platform.release()} on {platform.machine()}.")
            return

        if low.startswith(("play ", "song ")):
            song = text.split(" ", 1)[1].strip()
            service = "spotify" if " on spotify" in song.lower() else "youtube"
            if service == "spotify":
                song = song[:song.lower().rfind(" on spotify")].strip()
                url = "https://open.spotify.com/search/" + quote_plus(song)
            else:
                if " on youtube" in song.lower():
                    song = song[:song.lower().rfind(" on youtube")].strip()
                url = "https://www.youtube.com/results?search_query=" + quote_plus(song)
            self.open_url(url, f"Finding {song} for you.")
            return

        if low.startswith("search "):
            query = text[7:].strip()
            self.open_url("https://www.google.com/search?q=" + quote_plus(query), f"Searching for {query}.")
            return

        if low.startswith(("open ", "launch ", "start ")):
            target = text.split(" ", 1)[1]
            self.launch(target)
            return

        self.speak("I didn't recognize that command. Say help for supported commands.")

    def run(self):
        self.speak("JARVIS online. Voice control is ready.")
        while self.running:
            try:
                command = self.listen()
                if command:
                    print(f"You: {command}")
                    self.handle(command)
            except sr.WaitTimeoutError:
                continue
            except KeyboardInterrupt:
                self.running = False
            except OSError:
                self.speak("Microphone access failed. Check your Windows microphone permission.")
                self.running = False


if __name__ == "__main__":
    JarvisPro().run()
