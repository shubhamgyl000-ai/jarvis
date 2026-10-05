"""Minimal Jarvis: play a requested song or run a command."""
import os
import platform
import subprocess
import webbrowser
from urllib.parse import quote_plus


def play_song(query: str) -> str:
    """Open a YouTube search for a song."""
    url = "https://www.youtube.com/results?search_query=" + quote_plus(query)
    webbrowser.open(url)
    return f"Opening music search for: {query}"


def run_command(command: str) -> str:
    """Run a command supplied by the user."""
    if not command.strip():
        return "No command supplied."
    subprocess.Popen(command, shell=True)
    return f"Running command: {command}"


def handle(request: str) -> str:
    text = request.strip()
    lower = text.lower()
    if lower.startswith("play "):
        return play_song(text[5:].strip())
    if lower.startswith("song "):
        return play_song(text[5:].strip())
    if lower.startswith("command "):
        return run_command(text[8:].strip())
    return "Say 'play <song>' or 'command <command>'."


if __name__ == "__main__":
    print("Jarvis ready. Use: play <song> | command <command>")
    while True:
        request = input("> ").strip()
        if request.lower() in {"exit", "quit", "shutdown jarvis"}:
            break
        print(handle(request))
