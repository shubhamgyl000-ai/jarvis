# Jarvis AI Assistant

Windows-first always-on voice assistant. After Windows starts Jarvis in the background, say "Hey Jarvis" without clicking a UI. Say "Shutdown Jarvis" to exit Jarvis.

Features:
- Wake-word listener
- Voice input/output
- Web search and a local learned-results store
- Persistent memory
- Open apps, type text, system status, explicit run commands
- Computer shutdown is intentionally confirmation-gated
- Phone messaging is not silently automated; connect an approved phone/automation bridge before sending messages

Run:
1. Install Python 3.11+.
2. Install dependencies: pip install -r requirements.txt
3. Run: python jarvis.py

Automatic startup:
Create a Windows shortcut that launches pythonw.exe with jarvis.py, then put the shortcut in:
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup

For unattended startup, Windows Task Scheduler can launch Jarvis at user logon.

Security:
Jarvis has local-control capabilities. Keep it local and do not expose its command endpoint publicly. Require confirmation for destructive actions.
