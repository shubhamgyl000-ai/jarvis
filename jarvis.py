import datetime, json, os, platform, re, subprocess, webbrowser
from pathlib import Path

import psutil
import pyautogui
import pyttsx3
import requests
import speech_recognition as sr
from bs4 import BeautifulSoup

BASE = Path(__file__).parent
MEMORY_FILE = BASE / "memory.json"
LEARNED_FILE = BASE / "learned.json"
LOG_FILE = BASE / "jarvis.log"

WAKE_NAMES = ("jarvis", "mahi", "hey jarvis", "hey mahi")
STOP_NAMES = ("shutdown jarvis", "shutdown mahi", "exit jarvis", "exit mahi")

recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
engine = pyttsx3.init()
engine.setProperty("rate", 170)

def log(message):
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now().isoformat()}] {message}\n")

def speak(text):
    print("Mahi:", text)
    engine.say(text)
    engine.runAndWait()

def load(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default

def save(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def choose_female_voice():
    try:
        voices = engine.getProperty("voices")
        for voice in voices:
            blob = f"{voice.name} {voice.id}".lower()
            if any(x in blob for x in ("female", "zira", "hazel", "susan")):
                engine.setProperty("voice", voice.id)
                return voice.id
    except Exception:
        pass
    return None

FEMALE_VOICE = choose_female_voice()

def extract_wake(text):
    value = text.lower().strip()
    for wake in sorted(WAKE_NAMES, key=len, reverse=True):
        if wake in value:
            return value.replace(wake, "", 1).strip(" ,.-")
    return None

def learn_web(topic):
    try:
        q = requests.utils.quote(topic)
        url = "https://www.google.com/search?q=" + q
        response = requests.get(url, timeout=8,
                                headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        snippets = []
        for node in soup.select("div"):
            text = node.get_text(" ", strip=True)
            if 80 < len(text) < 600 and text not in snippets:
                snippets.append(text)
            if len(snippets) >= 8:
                break
        learned = load(LEARNED_FILE, [])
        learned.append({
            "topic": topic,
            "time": datetime.datetime.now().isoformat(),
            "snippets": snippets,
        })
        save(LEARNED_FILE, learned[-100:])
        return snippets[:3]
    except Exception as exc:
        log(f"web search failed: {exc}")
        return []

def open_app(name):
    aliases = {
        "notepad": "notepad.exe", "calculator": "calc.exe", "calc": "calc.exe",
        "paint": "mspaint.exe", "cmd": "cmd.exe", "explorer": "explorer.exe",
        "chrome": "chrome.exe", "edge": "msedge.exe",
    }
    target = aliases.get(name.lower(), name)
    try:
        subprocess.Popen(target, shell=True)
        return True
    except Exception as exc:
        log(f"open_app failed: {exc}")
        return False

def execute(command):
    c = command.lower().strip()
    if c in STOP_NAMES:
        return "SHUTDOWN"
    if c.startswith("open "):
        target = command[5:].strip()
        if open_app(target):
            return f"Opened {target}."
        webbrowser.open("https://www.google.com/search?q=" + requests.utils.quote(target))
        return f"I opened a web search for {target}."
    if c.startswith("search "):
        query = command[7:].strip()
        return "I searched the web and stored the available results." if learn_web(query) else "The web search failed."
    if c.startswith("remember "):
        memory = load(MEMORY_FILE, {"notes": []})
        memory.setdefault("notes", []).append(command[9:].strip())
        save(MEMORY_FILE, memory)
        return "Saved to memory."
    if "system status" in c:
        return f"CPU {psutil.cpu_percent()} percent, RAM {psutil.virtual_memory().percent} percent."
    if c.startswith("type "):
        pyautogui.write(command[5:], interval=0.02)
        return "Typed it."
    if c.startswith("run "):
        # Explicit run remains available; only use trusted commands locally.
        subprocess.Popen(command[4:], shell=True)
        return "Command started."
    return "I heard you. That natural-language action still needs an AI tool adapter."

def listen(timeout=None):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.25)
        audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=8)
    return recognizer.recognize_google(audio).lower()

def main():
    speak("Mahi is online. Jarvis AI system ready.")
    while True:
        try:
            heard = listen()
        except Exception as exc:
            log(f"listener error: {exc}")
            continue
        command = extract_wake(heard)
        if command is None:
            continue
        speak("Yes, I am listening.")
        if command:
            result = execute(command)
            if result == "SHUTDOWN":
                speak("Shutting down. Take care.")
                return
            speak(result)
        while True:
            try:
                cmd = listen(timeout=5)
            except Exception as exc:
                log(f"command listener error: {exc}")
                continue
            if cmd in STOP_NAMES:
                speak("Shutting down. Take care.")
                return
            result = execute(cmd)
            if result == "SHUTDOWN":
                speak("Shutting down. Take care.")
                return
            speak(result)

if __name__ == "__main__":
    main()
