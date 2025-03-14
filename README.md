# ⚡ Cybersecurity Lab Automation

Welcome to **Cybersecurity Lab Automation** — an intelligent Python-powered system that transforms the way you complete cybersecurity labs on Kali Linux. Say goodbye to repetitive tasks and hello to smart, streamlined automation with multi-agent teamwork handling everything from strategy to reporting.

## 🚀 What It Does

This system doesn’t just automate commands—it *thinks* for you. Leveraging a multi-agent architecture, it reads your lab instructions, plans a strategy, selects intelligent commands, explains *why* they matter, and compiles evidence into a detailed report. All on autopilot.

Whether you’re tackling passive reconnaissance or complex exploitation, this tool accelerates your workflow while keeping you in control.

---

## 🧠 How It Works

A fleet of specialized agents collaborate behind the scenes:

1. **Lab Instruction Parser**: Understands the entire lab document—goals, tasks, and requirements.
2. **Lab Strategy Planner**: Maps out the smartest plan of attack.
3. **Context Analyzer**: Extracts key details like targets, ports, and protocols.
4. **Command Generator**: Crafts and customizes the best commands for the job.
5. **Explanation Generator**: Tells you *why* each move matters.
6. **Output Analyzer**: Makes sense of the results through a security lens.
7. **Evidence Collector**: Gathers proof and critical findings.
8. **Report Generator**: Delivers polished, professional reports—ready for submission or review.

---

## 🛠️ Setup in Minutes

1. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. On macOS? Add Microsoft Remote Desktop for RDP (if needed):
   ```bash
   brew install --cask microsoft-remote-desktop
   ```

3. Check your `config.py`:
   - SSH/RDP connection details for your Kali VM
   - OpenAI API key for intelligent language processing
   - Flexible command templates you can tweak anytime

---

## ⚙️ How to Use It

1. Launch the automation:
   ```bash
   python main.py
   ```

2. Feed it your lab instructions:
   - Paste a full lab document (preferred)
   - Or enter step-by-step instructions interactively

3. Sit back as the system:
   ✅ Connects to your Kali VM  
   ✅ Analyzes the lab and defines goals  
   ✅ Plans and executes commands dynamically  
   ✅ Collects evidence and interprets outputs  
   ✅ Generates comprehensive reports (Markdown)  
   ✅ Takes screenshots along the way  
   ✅ Saves everything neatly in `lab_logs/`

---

## 🔥 Features You’ll Love

- **Full Lab Document Analysis**: Understands and processes entire lab scenarios.
- **Smart Strategy Planning**: Crafts a logical, efficient approach for lab completion.
- **Context-Aware Commands**: Generates commands tailored to your exact setup.
- **Real-Time Explanations**: Understand the *why* behind every action.
- **Intelligent Output Analysis**: Reviews command results with a security-first mindset.
- **Evidence Gathering**: Collects proof and insights at every step.
- **Auto-Generated Reports**: Beautifully structured reports with all findings.
- **Customizable Templates**: Adaptable commands for any lab style.
- **Reliable SSH Connections**: Robust error-handling keeps you connected.
- **Organized Logs**: Comprehensive, structured logs and screenshots.

---

## 📝 Example Lab It Can Tackle

Here's a sample lab document to show what the system can handle:

```markdown
# Lab 2: Identifying a Target Host on the Lumon Industries Network

## Scenario  
Your team at Lumon Industries suspects insider threats. Passive network monitoring will help you track suspicious browsing activity and identify the culprit.

### Objective  
- Monitor DNS queries  
- Profile HTTP/S behavior  
- Pinpoint the rogue host  

### Goals  
✅ Observe DNS and HTTP/S traffic  
✅ Correlate browsing behavior  
✅ Identify the suspicious IP  
```

---

## 🧪 Test Drive (No VM Needed!)

Want to try it out without a VM?  
Run the simulation:
```bash
python test.py
```

It’ll walk through command generation, document parsing, and report creation—no VM required.

---

## 🌐 Where to Find the Magic  
Check out all the logs, screenshots, and reports in the `lab_logs/` directory. Your findings, command history, and a professional lab report await!

---

## 🤝 Contribute / Feedback  
Got ideas to make it better? Open an issue or submit a pull request!  
Security pros and Pythonistas welcome. 🎉
