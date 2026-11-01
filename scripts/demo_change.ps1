# Used in the video demo (Windows PowerShell, run from the project root).
# Edits the welcome message, commits and pushes -> GitHub webhook -> Jenkins builds & redeploys.
param(
    [string]$Message = "Live demo: change pushed at $(Get-Date -Format 'HH:mm:ss') - auto-deployed by Jenkins"
)

$file = "app/app.py"
(Get-Content $file) -replace '^WELCOME_MESSAGE = .*$', "WELCOME_MESSAGE = `"$Message`"" | Set-Content $file

git add $file
git commit -m "Demo: update welcome message"
git push origin main

Write-Host "`nPushed. Watch Jenkins - a new build should start within seconds." -ForegroundColor Green
