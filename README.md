from pathlib import Path

# Define the README content
readme_content = """
# Ray-I: AI-Powered Linux Assistant for Pentesting & Automation

Ray-I is an AI-driven terminal-based assistant built in Python that leverages Google's Gemini 2.5 API to automate and assist with Linux system tasks, ethical hacking, and pentesting workflows.

> ⚡ Built for power users, hackers, and sysadmins who want to offload complex CLI commands to an intelligent agent.

---

## 🚀 Features

- 🔐 **AI-Powered Pentesting**  
  Automatically scans open ports, identifies vulnerabilities, and suggests potential exploits.

- 🖥️ **Linux System Task Automation**  
  Perform system updates, install packages, monitor logs, and more — all with natural language prompts.

- 🧠 **Gemini 2.5 Integration**  
  Uses Google’s state-of-the-art LLM to interpret your instructions and suggest real-time CLI operations.

- 💡 **Conversational CLI Interface**  
  Interact with Ray-I as if you were chatting with a terminal-savvy hacker sidekick.

- 📦 **Modular & Extensible**  
  New commands and tools can be added as modules with ease.

---

## 🛠️ Setup

1. Clone the repository
```bash
git clone https://github.com/ray743/ray-i.git
cd ray-i

2. Install dependencies
pip install -r requirements.txt

3. Configure your API Key
GEMINI_API_KEY=your_google_gemini_key

4. Run Ray-I
python ray.py


##Example COmmands:
> ray show all open ports on the system
> ray update system packages
> ray run a stealth nmap scan on 192.168.1.1
> ray ninstall vsftpd and start the service
> ray what services are vulnerable on port 445?
> ray create a reverse shell payload with msfvenom

📁 Modules
Each feature is a Python module stored in the /modules directory. You can easily add your own:
modules/
├── network_scan.py
├── system_update.py
├── reverse_shell.py
├── whois_lookup.py
└── ...

🧠 Under the Hood:
Language Model: Google Gemini 2.5 via Vertex AI API

Environment: Python 3.10+

Supported Tools: nmap, netcat, whois, iptables, msfvenom, and many more.

Security First: Commands are always previewed before execution. Use responsibly.

🛡️ Ethical Use Only
⚠️ Ray-I is intended for ethical and educational penetration testing only.
Never use Ray-I on systems you do not own or have explicit permission to test.


🤖 Author
Raynold Bobola
Port Moresby, Papua New Guinea
GitHub: @Ray743
Portfolio: ray743.github.io/portfolio

📄 License
This project is licensed under the MIT License.