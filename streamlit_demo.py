"""Streamlit dashboard for Mythosguard demo visualization."""
import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd

# Page config
st.set_page_config(
    page_title="Mythosguard - Red-Team Arena",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
    }
    .vuln-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 3px;
        font-size: 0.875rem;
        font-weight: bold;
        margin-right: 0.5rem;
    }
    .vuln-eval { background-color: #dc3545; color: white; }
    .vuln-password { background-color: #fd7e14; color: white; }
    .vuln-exec { background-color: #6f42c1; color: white; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🛡️ Mythosguard</div>', unsafe_allow_html=True)
st.markdown("### Adaptive Multi-Agent Red-Team Arena", unsafe_allow_html=True)
st.markdown("---")

# Sidebar controls
st.sidebar.header("Demo Controls")

# Load logs
log_path = "logs/rounds.jsonl"
if os.path.exists(log_path):
    with open(log_path, 'r') as f:
        logs = [json.loads(line) for line in f.readlines()]
else:
    logs = []

if not logs:
    st.warning("No logs found. Run the demo first: `python demo.py --dry-run`")
    st.stop()

# Filter controls
show_rounds = st.sidebar.slider("Number of Rounds to Show", 1, len(logs), min(3, len(logs)))
selected_seed = st.sidebar.selectbox("Filter by Seed", ["All"] + list(set([log.get("seed", 42) for log in logs if "seed" in log])))

# Filter logs
display_logs = logs[-show_rounds:] if selected_seed == "All" else [log for log in logs if log.get("seed") == selected_seed][-show_rounds:]

# Metrics
col1, col2, col3, col4 = st.columns(4)
total_vulns = sum(len(log.get("findings", [])) for log in display_logs)
total_patches = sum(1 for log in display_logs if log.get("patch"))
verified = sum(1 for log in display_logs if log.get("verification", {}).get("passed"))

with col1:
    st.metric("Total Rounds", len(display_logs))
with col2:
    st.metric("Vulnerabilities Found", total_vulns)
with col3:
    st.metric("Patches Generated", total_patches)
with col4:
    st.metric("Verified Fixes", verified)

st.markdown("---")

# Show vulnerable code
st.subheader("🎯 Target: sample_vulnerable_code/vuln.py")
with st.expander("View Vulnerable Code", expanded=True):
    vuln_code = """# Sample vulnerable file for Mythosguard demo
import os

def compute(user_input):
    # insecure: uses eval on user input
    return eval(user_input)

password = "hunter2"  # hardcoded password (intentional vuln)
"""
    st.code(vuln_code, language="python")

# Show rounds
st.subheader("📊 Round-by-Round Analysis")

for i, log in enumerate(display_logs, 1):
    round_num = log.get("round", i)
    timestamp = log.get("timestamp", "N/A")
    strategy = log.get("strategy", "N/A")
    
    with st.expander(f"Round {round_num} - {strategy} - {timestamp}", expanded=(i == 1)):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔍 Findings")
            findings = log.get("findings", [])
            if findings:
                for finding in findings:
                    vuln_type = finding.get("type", "unknown")
                    line = finding.get("line", "N/A")
                    line_text = finding.get("line_text", "")
                    
                    badge_class = f"vuln-{vuln_type}"
                    st.markdown(f"""
                    <span class="vuln-badge {badge_class}">{vuln_type.upper()}</span>
                    <strong>Line {line}:</strong> {line_text}
                    """, unsafe_allow_html=True)
            else:
                st.info("No vulnerabilities found")
        
        with col2:
            st.markdown("#### ⚖️ Verdict")
            verdict = log.get("verdict", {})
            success = verdict.get("success", False)
            vuln_types = verdict.get("types", [])
            count = verdict.get("count", 0)
            
            if success:
                st.markdown('<div class="success-box">✅ Vulnerabilities Detected</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="warning-box">⚠️ No Vulnerabilities Found</div>', unsafe_allow_html=True)
            
            st.markdown(f"- **Types:** {', '.join(vuln_types)}")
            st.markdown(f"- **Count:** {count}")
        
        # Attack prompt
        attack_prompt = log.get("attack_prompt")
        if attack_prompt:
            st.markdown("#### 🤖 Attack Prompt (MockLLM)")
            st.info(attack_prompt)
        
        # Patch
        patch = log.get("patch")
        if patch:
            st.markdown("#### 🔧 Generated Patch")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Patch Details:**")
                st.markdown(f"- **ID:** `{patch.get('id', 'N/A')}`")
                st.markdown(f"- **Action:** `{patch.get('action', 'N/A')}`")
                st.markdown(f"- **Matcher:** `{patch.get('matcher', 'N/A')}`")
                st.markdown(f"- **Created by:** {patch.get('created_by', 'N/A')}")
            
            with col2:
                st.markdown("**Code Change:**")
                st.code(patch.get("new_code", "N/A"), language="python")
            
            st.markdown("**Unified Diff:**")
            diff_text = patch.get("diff", "")
            st.code(diff_text, language="diff")
        
        # Verification
        verification = log.get("verification", {})
        if verification:
            st.markdown("#### ✅ Verification")
            passed = verification.get("passed")
            post_findings = verification.get("post_findings", [])
            git_check = verification.get("git_check_ok", False)
            
            if passed:
                st.markdown('<div class="success-box">✅ Patch Verified - Vulnerability Removed</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="warning-box">⚠️ Verification Failed</div>', unsafe_allow_html=True)
            
            st.markdown(f"- **Git Apply Check:** {'✅ Passed' if git_check else '❌ Failed'}")
            st.markdown(f"- **Remaining Findings:** {len(post_findings)}")
            
            if post_findings:
                st.markdown("**Remaining Vulnerabilities:**")
                for finding in post_findings:
                    vuln_type = finding.get("type", "unknown")
                    line = finding.get("line", "N/A")
                    st.markdown(f"- {vuln_type} at line {line}")
        
        # Strategy weights
        weights = log.get("weights", {})
        if weights:
            st.markdown("#### 📈 Strategy Weights")
            weights_df = pd.DataFrame(list(weights.items()), columns=["Strategy", "Weight"])
            st.bar_chart(weights_df.set_index("Weight"))

# Strategy evolution
st.markdown("---")
st.subheader("📈 Strategy Evolution Over Time")

if len(display_logs) > 1:
    weights_history = []
    for log in display_logs:
        weights = log.get("weights", {})
        weights["round"] = log.get("round", 0)
        weights_history.append(weights)
    
    weights_df = pd.DataFrame(weights_history)
    if not weights_df.empty:
        st.line_chart(weights_df.set_index("round"))

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    <p>🛡️ Mythosguard - Adaptive Multi-Agent Red-Team Arena</p>
    <p>Deterministic MockLLM • No External API Dependencies • Reproducible Demos</p>
</div>
""", unsafe_allow_html=True)

# Run new demo button
st.sidebar.markdown("---")
st.sidebar.header("Actions")
if st.sidebar.button("🔄 Run New Demo"):
    st.sidebar.info("Run: `python demo.py --dry-run` then refresh this page")
