"""GitHub-side smoke diagnostics for Jarvis/Mahi.
This intentionally does not access the user's laptop.
"""
import os
import sys
import platform

def main():
    print("Jarvis GitHub smoke check")
    print("Python:", sys.version.split()[0])
    print("Runner OS:", platform.system())
    print("CI:", os.getenv("CI", "false"))
    print("GitHub Actions:", os.getenv("GITHUB_ACTIONS", "false"))
    print("Status: runner environment is available")

if __name__ == "__main__":
    main()
