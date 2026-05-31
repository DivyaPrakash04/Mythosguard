# 📤 GitHub Upload Instructions for Hackathon Submission

## Step 1: Initialize Git Repository (if not already done)

```powershell
cd D:\SundaiHackMITTheEngine\Mythosguard
git init
```

## Step 2: Create .gitignore File

Create a file named `.gitignore` in the project root with:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Logs
logs/*.jsonl
!logs/.gitkeep

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
```

## Step 3: Add All Files to Git

```powershell
git add .
```

## Step 4: Create Initial Commit

```powershell
git commit -m "Initial commit: Mythosguard Arena - Adaptive Multi-Agent Red-Team Arena"
```

## Step 5: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click **+** → **New repository**
3. Repository name: `Mythosguard` (or your preferred name)
4. Description: `Adaptive Multi-Agent Red-Team Arena & Automated Self-Healing Code Security System`
5. Make it **Public** (required for hackathon judges to access)
6. **Do NOT** initialize with README (we already have one)
7. Click **Create repository**

## Step 6: Link Local Repository to GitHub

```powershell
git remote add origin https://github.com/YOUR_USERNAME/Mythosguard.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 7: Enable GitHub Pages (for Dashboard)

1. Go to your repository on GitHub
2. Click **Settings** → **Pages** (left sidebar)
3. Under **Source**, select:
   - Branch: `main`
   - Folder: `/ (root)`
4. Click **Save**

Your dashboard will be live at: `https://YOUR_USERNAME.github.io/Mythosguard/dashboard.html`

## Step 8: Verify Everything Works

1. Open your GitHub repository URL
2. Check that all files are uploaded
3. Click `dashboard.html` to verify it loads
4. Test the GitHub Pages URL from Step 7

## Step 9: Update Hackathon Submission

Add these links to your hackathon submission:

**GitHub Repository:**
```
https://github.com/YOUR_USERNAME/Mythosguard
```

**Live Dashboard (GitHub Pages):**
```
https://YOUR_USERNAME.github.io/Mythosguard/dashboard.html
```

**Weights & Biases Report:**
```
https://wandb.ai/divyaprakash_26/mythosguard-arena/reports/Mythosguard-Cyber-Defense-Orchestrator--VmlldzoxNzA3NDk3NA
```

---

## 🎯 Quick Reference Commands

```powershell
# Check git status
git status

# Add new files
git add .

# Commit changes
git commit -m "Your commit message"

# Push to GitHub
git push

# Pull latest changes
git pull
```

---

## ⚠️ Important Notes

- Make sure the repository is **Public** so judges can access it
- Don't upload sensitive files (API keys, personal data)
- The `logs/` folder is excluded by .gitignore to keep repository clean
- Dashboard works both locally and on GitHub Pages

---

## 📋 Hackathon Submission Checklist

- [ ] Repository created on GitHub
- [ ] Repository is set to Public
- [ ] All files pushed to GitHub
- [ ] GitHub Pages enabled
- [ ] Dashboard loads on GitHub Pages
- [ ] W&B link added to submission
- [ ] README.md is complete and clear
- [ ] QUICK_START.md is included for judges
- [ ] Demo runs successfully from cloned repository

---

**Total time to upload: 5-10 minutes**
