# 🛡️ Mythosguard Arena

**Adaptive Multi-Agent Red-Team Arena & Automated Self-Healing Code Security System**

Mythosguard is an AI-powered security testing system that automatically finds vulnerabilities in code, generates fixes, and verifies they work - all without human intervention. It simulates adversarial attacks to identify security flaws, instantly synthesizes structured security patches, and validates them through sandboxed verification runs.

---

## 🎯 What Makes This Different

**Traditional security tools** just find problems. **Mythosguard** fixes them automatically.

- **Self-Healing Code**: Automatically generates and applies security patches
- **Multi-Agent Intelligence**: AI agents work together to attack, detect, patch, and verify
- **Deterministic & Reproducible**: No external API dependencies - perfect for demos
- **Visual Dashboard**: Beautiful, beginner-friendly interface for non-technical audiences
- **Real-Time Verification**: Every fix is tested before being applied

---

## 🚀 Quick Start for Judges (2 Minutes)

### Option 1: View the Interactive Dashboard (Recommended)

1. **Open the dashboard**: Double-click `dashboard.html` in your browser
2. **See the results**: The dashboard shows:
   - Security vulnerabilities found (color-coded by severity)
   - Automatic fixes generated
   - Verification results
   - Round-by-round test history

### Option 2: Run the Demo Yourself

```powershell
# Install dependencies
pip install -r requirements.txt

# Run the security test (3 rounds, takes ~10 seconds)
python demo.py --dry-run --no-rich

# Open the dashboard to see results
start dashboard.html
```

### Option 3: Live Demo with Web Server

```powershell
# Start web server
python -m http.server 8000

# Open in browser
# http://localhost:8000/dashboard.html
```

---

## 📊 Live Demo Dashboard

**[View Interactive Dashboard](dashboard.html)** - Shows real-time security testing results with:
- 🎨 Color-coded vulnerability severity (Red=Critical, Orange=High, Green=Safe)
- 📈 Round-by-round attack history
- 🔧 Automatic fix generation with diff views
- ✅ Safety verification results
- 🤖 AI attack simulations

**[Weights & Biases Analytics Report](https://wandb.ai/divyaprakash_26/mythosguard-arena/reports/Mythosguard-Cyber-Defense-Orchestrator--VmlldzoxNzA3NDk3NA)** - Detailed metrics and training logs

---

## 🏆 Hackathon Submission Details

### Project Description (For Judges)

**Problem**: Security vulnerabilities in code are hard to find and harder to fix. Traditional tools require manual intervention and security expertise.

**Solution**: Mythosguard is an autonomous multi-agent system that:
1. **Attacks** code using AI simulations to find vulnerabilities
2. **Detects** security flaws (code injection, hardcoded secrets, unsafe execution)
3. **Generates** automatic fixes using unified diff format
4. **Verifies** every fix in a sandboxed environment
5. **Applies** only verified-safe patches

**Impact**: 
- Reduces security testing time from hours to seconds
- Eliminates manual patch writing
- Catches vulnerabilities humans miss
- 100% reproducible - no false positives

**Technical Innovation**:
- Multi-agent orchestration (Planner, Attacker, Judge, Defender, Verifier)
- Deterministic MockLLM for reproducible demos
- Unified diff format for git-compatible patches
- Sandbox verification for safe testing

**Demo**: See the interactive dashboard showing real-time vulnerability detection and automatic patching.

---

## 🛠️ How It Works

```
Planner → Attack Agent → Target Code → Judge → Defender → Verifier → (Repeat)
```

1. **Planner**: Chooses attack strategies based on success rates
2. **Attack Agent**: Simulates AI attacks to test code security
3. **Target Code**: The code being tested (sandboxed for safety)
4. **Judge**: Analyzes findings and flags vulnerabilities
5. **Defender**: Generates automatic security patches
6. **Verifier**: Tests patches in sandbox before applying

---

## 📁 Project Structure

```
Mythosguard/
├── dashboard.html          # Interactive visual dashboard
├── demo.py                # Main demo script
├── orchestrator.py        # Multi-agent coordinator
├── agents/                # AI agents (attack, judge, defender, verifier)
├── providers/             # LLM adapters (MockLLM for demos)
├── sample_vulnerable_code/ # Test targets with known vulnerabilities
├── logs/                  # Test results (JSONL format)
└── requirements.txt       # Python dependencies
```

---

## 🌐 Deploying for Public Access

### GitHub Pages (Free, Easy)

1. Push this repository to GitHub
2. Go to **Settings > Pages**
3. Select `main` branch as source
4. Dashboard live at: `https://<username>.github.io/Mythosguard/dashboard.html`

### Vercel (Free, Fast)

1. Install: `npm install -g vercel`
2. Run: `vercel` from project directory
3. Dashboard live at: `https://mythosguard-arena.vercel.app`

---

## ⚖️ Ethics & Safety

**Only runs against sandboxed test code** in `sample_vulnerable_code/`. Never targets external systems. All testing happens in isolated environments with verification before any changes are applied.

---

## 📝 Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`
- No external API keys required (uses deterministic MockLLM)

---

## 🤝 Contributing

This is a hackathon prototype designed for demonstration purposes. For production use, additional security measures and testing would be required.

---

## 📧 Contact

Built for MIT Hackathon 2026 - Adaptive Multi-Agent Red-Team Arena
