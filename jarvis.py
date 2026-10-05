"""Mahi Jarvis desktop board - standard-library only, easy to host/deploy."""

import platform
import subprocess
import threading
import webbrowser
import tkinter as tk
from tkinter import scrolledtext
from urllib.parse import quote_plus


class Jarvis:
    def __init__(self):
        self.os_name = platform.system()

    def play_song(self, song, service="youtube"):
        song = song.strip()
        if not song:
            return "Please give me a song name."
        if service == "spotify":
            url = "https://open.spotify.com/search/" + quote_plus(song)
            site = "Spotify"
        else:
            url = "https://www.youtube.com/results?search_query=" + quote_plus(song)
            site = "YouTube"
        webbrowser.open(url)
        return f"Opening {song} on {site}."

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
            return f"Opening {target}."
        if target.startswith(("http://", "https://")):
            webbrowser.open(target)
            return f"Opening {target}."
        return self.run_command(target)

    def run_command(self, command):
        command = command.strip()
        if not command:
            return "Please give me a command."
        try:
            subprocess.Popen(command, shell=True)
            return f"Command started: {command}"
        except Exception as exc:
            return f"I couldn't start that command: {exc}"

    def handle(self, request):
        text = request.strip()
        lower = text.lower()

        if not text:
            return "I'm listening. Give me a command."

        if lower in {"exit", "quit", "shutdown jarvis", "close jarvis"}:
            return "__EXIT__"

        if lower.startswith("play "):
            rest = text[5:].strip()
            low = rest.lower()
            if " on spotify" in low:
                return self.play_song(rest[:low.rfind(" on spotify")], "spotify")
            if " on youtube" in low:
                return self.play_song(rest[:low.rfind(" on youtube")], "youtube")
            return self.play_song(rest, "youtube")

        if lower.startswith("song "):
            return self.play_song(text[5:].strip())

        if lower.startswith("open "):
            return self.open_target(text[5:])

        if lower.startswith("search "):
            query = text[7:].strip()
            if not query:
                return "Please tell me what to search."
            webbrowser.open("https://www.google.com/search?q=" + quote_plus(query))
            return f"Searching for {query}."

        if lower.startswith("command "):
            return self.run_command(text[8:])

        if lower.startswith("run "):
            return self.run_command(text[4:])

        return self.run_command(text)


class JarvisBoard:
    def __init__(self):
        self.jarvis = Jarvis()
        self.root = tk.Tk()
        self.root.title("Mahi • Jarvis")
        self.root.geometry("820x620")
        self.root.minsize(650, 500)
        self.root.configure(bg="#10131a")
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        header = tk.Frame(self.root, bg="#171b24", height=72)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text="MAHI • JARVIS",
            font=("Segoe UI", 21, "bold"), fg="white", bg="#171b24"
        ).pack(side="left", padx=22, pady=12)

        tk.Label(
            header, text="● ONLINE",
            font=("Segoe UI", 10, "bold"), fg="#63e6be", bg="#171b24"
        ).pack(side="right", padx=22)

        self.chat = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, font=("Segoe UI", 11),
            bg="#0d1016", fg="#e8ecf1", insertbackground="white",
            relief="flat", padx=16, pady=16
        )
        self.chat.pack(fill="both", expand=True, padx=16, pady=(16, 10))
        self.chat.configure(state="disabled")

        tk.Label(
            self.root,
            text="Try: play Kesariya on YouTube • play Believer on Spotify • open github • command notepad",
            font=("Segoe UI", 9), fg="#aeb6c2", bg="#10131a"
        ).pack(pady=(0, 8))

        bottom = tk.Frame(self.root, bg="#10131a")
        bottom.pack(fill="x", padx=16, pady=(0, 16))

        self.entry = tk.Entry(
            bottom, font=("Segoe UI", 12), bg="#171b24", fg="white",
            insertbackground="white", relief="flat"
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=12)
        self.entry.bind("<Return>", self.send)
        self.entry.focus_set()

        tk.Button(
            bottom, text="SEND", command=self.send,
            font=("Segoe UI", 10, "bold"), fg="white", bg="#2b3240",
            relief="flat", padx=20, pady=10
        ).pack(side="left", padx=(10, 0))

    def add_message(self, who, message):
        self.chat.configure(state="normal")
        self.chat.insert(tk.END, f"{who}: {message}\n\n")
        self.chat.configure(state="disabled")
        self.chat.see(tk.END)

    def send(self, _event=None):
        request = self.entry.get().strip()
        if not request:
            return
        self.entry.delete(0, tk.END)
        self.add_message("You", request)
        self.add_message("Mahi", "Working on it...")

        def work():
            result = self.jarvis.handle(request)
            self.root.after(0, lambda: self.finish(result))

        threading.Thread(target=work, daemon=True).start()

    def finish(self, result):
        if result == "__EXIT__":
            self.root.destroy()
            return
        self.chat.configure(state="normal")
        text = self.chat.get("1.0", tk.END)
        marker = "Mahi: Working on it...\n\n"
        if marker in text:
            text = text.rsplit(marker, 1)[0]
            self.chat.delete("1.0", tk.END)
            self.chat.insert(tk.END, text)
        self.chat.configure(state="disabled")
        self.add_message("Mahi", result)

    def close(self):
        self.root.destroy()


if __name__ == "__main__":
    JarvisBoard().root.mainloop()
