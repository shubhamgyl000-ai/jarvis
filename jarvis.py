import os, subprocess, webbrowser, datetime, json, platform
from pathlib import Path
import requests
import speech_recognition as sr
import pyttsx3
import pyautogui
import psutil

BASE = Path(__file__).parent
MEMORY_FILE = BASE / "memory.json"
LEARNED_FILE = BASE / "learned.json"
WAKE, STOP = "hey jarvis", "shutdown jarvis"

engine = pyttsx3.init()
engine.setProperty("rate", 175)
recognizer = sr.Recognizer()

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

def load(path, default):
    try: return json.loads(path.read_text(encoding="utf-8"))
    except Exception: return default

def save(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def learn_web(topic):
    try:
        q = requests.utils.quote(topic)
        html = requests.get("https://www.google.com/search?q="+q, timeout=8,
                            headers={"User-Agent":"Mozilla/5.0"}).text
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        snippets = [x.get_text(" ", strip=True) for x in soup.select("div")
                    if len(x.get_text(" ", strip=True)) > 80][:8]
        learned = load(LEARNED_FILE, [])
        learned.append({"topic": topic, "time": datetime.datetime.now().isoformat(),
                        "snippets": snippets})
        save(LEARNED_FILE, learned[-100:])
        return snippets[:3]
    except Exception: return []

def open_app(name):
    aliases = {"notepad":"notepad.exe","calculator":"calc.exe","calc":"calc.exe",
               "paint":"mspaint.exe","cmd":"cmd.exe","explorer":"explorer.exe"}
    target = aliases.get(name.lower(), name)
    try:
        subprocess.Popen(target, shell=True)
        return True
    except Exception: return False

def execute(command):
    c = command.lower().strip()
    if c == STOP: return "SHUTDOWN"
    if c.startswith("open "):
        target = command[5:].strip()
        if open_app(target): return "Opened " + target
        webbrowser.open("https://www.google.com/search?q="+requests.utils.quote(target))
        return "Opened a web search for " + target
    if c.startswith("search "):
        q = command[7:].strip()
        return "I searched and learned the results." if learn_web(q) else "Search failed."
    if c.startswith("remember "):
        m = load(MEMORY_FILE, {"notes":[]})
        m["notes"].append(command[9:].strip())
        save(MEMORY_FILE, m)
        return "Saved to memory."
    if "system status" in c:
        return f"CPU {psutil.cpu_percent()} percent, RAM {psutil.virtual_memory().percent} percent."
    if c.startswith("type "):
        pyautogui.write(command[5:], interval=0.02)
        return "Typed it."
    if c.startswith("run "):
        subprocess.Popen(command[4:], shell=True)
        return "Command started."
    return "I understood the command, but that tool is not implemented yet."

def listen(timeout=None):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.4)
        audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=8)
    return recognizer.recognize_google(audio).lower()

def main():
    speak("Jarvis background listener is online.")
    while True:
        try: heard = listen()
        except Exception: continue
        if WAKE in heard:
            speak("Yes. How can I help?")
            while True:
                try: cmd = listen(timeout=5)
                except Exception: continue
                if cmd == STOP:
                    speak("Shutting down Jarvis.")
                    return
                speak(execute(cmd))

if __name__ == "__main__":
    main()
