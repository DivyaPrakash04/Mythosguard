# 🚀 Quick Start Guide for Hackathon Judges

## Option 1: View the Interactive Dashboard (Easiest - 30 seconds)

1. **Double-click** `dashboard.html` to open it in your browser
2. **See the demo**: The dashboard shows:
   - Security vulnerabilities found (color-coded: Red=Critical, Orange=High, Green=Safe)
   - Automatic fixes generated with code diffs
   - Safety verification results
   - Round-by-round attack history

**That's it!** No installation required.

---

## Option 2: Run the Demo Yourself (2 minutes)

### Step 1: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 2: Run the Security Test
```powershell
python demo.py --dry-run --no-rich
```
This runs 3 rounds of security testing (takes ~10 seconds).

### Step 3: View Results
```powershell
start dashboard.html
```

---

## Option 3: Live Demo with Web Server

```powershell
# Start web server
python -m http.server 8000

# Open in browser
# http://localhost:8000/dashboard.html
```

---

## 📊 What You'll See

The dashboard displays:
- **Overview Tab**: Metrics (rounds run, vulnerabilities found, patches generated, fixes verified)
- **Target Code Tab**: The code being tested with known vulnerabilities
- **Arena Rounds Tab**: Round-by-round results with collapsible details
- **About Tab**: How the system works

---

## 🎯 Key Features to Highlight

1. **Self-Healing Code**: Automatically generates and applies security patches
2. **Multi-Agent Intelligence**: AI agents work together (Planner, Attacker, Judge, Defender, Verifier)
3. **Deterministic**: No external API dependencies - 100% reproducible
4. **Visual Dashboard**: Beginner-friendly interface with color coding
5. **Real-Time Verification**: Every fix is tested before being applied

---

## 📈 Analytics

**[Weights & Biases Report](https://wandb.ai/divyaprakash_26/mythosguard-arena/reports/Mythosguard-Cyber-Defense-Orchestrator--VmlldzoxNzA3NDk3NA)** - Detailed metrics and training logs

---

## ⚡ Troubleshooting

**Dashboard won't load?**
- Try Option 1 (double-click dashboard.html)
- If that fails, use Option 3 (web server)

**Demo won't run?**
- Make sure Python 3.8+ is installed
- Run `pip install -r requirements.txt`

**No results showing?**
- Run `python demo.py --dry-run --no-rich` first
- Then refresh the dashboard

---

## 🎬 Demo Script for Presentation

```powershell
# 1. Clear old logs
Remove-Item logs\rounds.jsonl

# 2. Run fresh demo
python demo.py --dry-run --no-rich

# 3. Open dashboard
start dashboard.html

# 4. Navigate to "Arena Rounds" tab
# 5. Click on rounds to expand details
# 6. Show the color legend in "Overview" tab
```

---

## 🏆 Why This Matters

- **Problem**: Security vulnerabilities are hard to find and fix
- **Solution**: AI-powered automatic vulnerability detection and patching
- **Impact**: Reduces security testing from hours to seconds
- **Innovation**: Multi-agent orchestration with self-healing code

---

**Total time to see results: 30 seconds (Option 1) or 2 minutes (Option 2)**
