# GitHub Workflow (Windows PowerShell)

## Configure Git once
```powershell
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

## Create a GitHub repository
Create a public repository named `BBAT104_TQM_<RegNo>` on GitHub. Do not initialize it with another README if you are pushing this existing repository.

## Connect and push
Run these commands from the project folder, replacing the URL with your repository URL:
```powershell
git remote add origin https://github.com/YOUR-USERNAME/BBAT104_TQM_YOUR-REGNO.git
git push -u origin main
```

## Make future meaningful commits
```powershell
git status
git add parking_app/service.py tests/test_service.py
git commit -m "test: cover full parking capacity"
git push
```

Commit after a logical change and verify it works. Do not create empty or misleading commits. Before submission, replace placeholders, run tests, capture screenshots, and verify your remote repository shows the history.
