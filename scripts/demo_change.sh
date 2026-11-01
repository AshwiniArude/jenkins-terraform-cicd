#!/bin/bash
# Same as demo_change.ps1 for Git Bash / macOS / Linux. Run from the project root.
MSG="${1:-Live demo: change pushed at $(date +%H:%M:%S) - auto-deployed by Jenkins}"
sed -i.bak "s|^WELCOME_MESSAGE = .*|WELCOME_MESSAGE = \"${MSG}\"|" app/app.py && rm -f app/app.py.bak
git add app/app.py
git commit -m "Demo: update welcome message"
git push origin main
echo "Pushed. Watch Jenkins - a new build should start within seconds."
