# modules/scan.py

import subprocess
import shutil

def detect_installed_tools():
    tools = {}
    for tool in ["nmap", "rustscan", "masscan"]:
        tools[tool] = shutil.which(tool) is not None
    return tools

def run_port_scan(target: str, method: str = None):
    print(f"📡 Target detected: {target}")
    tools = detect_installed_tools()

    if not any(tools.values()):
        print("❌ No port scanning tools (nmap, rustscan, masscan) found. Please install at least one.")
        return

    # Auto-choose a method if not specified
    if method is None:
        method = "rustscan" if tools["rustscan"] else "nmap"

    print(f"🛠️ Using: {method}\n")

    try:
        if method == "nmap":
            cmd = f"nmap -sS -T3 -p- {target}"
        elif method == "rustscan":
            cmd = f"rustscan -a {target} -- -sS"
        elif method == "masscan":
            cmd = f"sudo masscan {target} -p1-65535 --rate=1000"
        else:
            print(f"❌ Unknown scan method '{method}'")
            return

        print(f"🔧 Running: {cmd}\n")
        subprocess.run(cmd, shell=True)

    except Exception as e:
        print(f"❌ Scan failed: {e}")
