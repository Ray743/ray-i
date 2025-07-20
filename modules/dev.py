# modules/dev.py

import asyncio
import os
import re
import sys
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment and Gemini API key
load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel(model_name="gemini-2.5-flash")

# --- Language Detection ---
def detect_language_from_filename(filename: str) -> str:
    ext_map = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".html": "HTML",
        ".css": "CSS",
        ".jsx": "React (JSX)",
        ".tsx": "React (TSX)",
        ".cpp": "C++",
        ".c": "C",
        ".java": "Java",
        ".cs": "C#",
        ".php": "PHP",
        ".rb": "Ruby",
        ".go": "Go",
        ".rs": "Rust",
        ".sh": "Shell script",
        ".json": "JSON",
        ".xml": "XML",
        ".sql": "SQL",
    }
    _, ext = os.path.splitext(filename.lower())
    return ext_map.get(ext, "code")

# --- Intent Detection ---
def is_explanation_request(text: str) -> bool:
    triggers = [
        "what does this do", "explain this", "analyze", "line by line",
        "describe this code", "can you explain", "break this down"
    ]
    return any(trigger in text.lower() for trigger in triggers)

def is_codey_snippet(text: str) -> bool:
    patterns = [
        r"^\s*def\s", r"^\s*import\s", r"^\s*class\s", r"\):",
        r"^\s*for\s", r"^\s*while\s", r"^\s*if\s", r"^\s*try\s",
        r"^\s*print\(", r"=\s*lambda", r"^\s*@\w+", r"^\s*#"
    ]
    return any(re.search(p, text) for p in patterns)

# --- Setup Detection ---
def is_setup_env_request(text: str) -> bool:
    keywords = ["setup", "initialize", "create", "generate"]
    stacks = ["react", "tailwind", "framer", "vite", "next.js"]
    return any(k in text.lower() for k in keywords) and any(s in text.lower() for s in stacks)

async def handle_env_setup(request: str):
    print("🧪 Detected environment setup intent.")

    folder = input("📁 What should the project folder be called? (default: my-app): ").strip() or "my-app"
    html_path = input("📄 (Optional) Do you have an HTML file to import from? Leave blank to skip: ").strip()

    steps = [
        f"npm create vite@latest {folder} -- --template react",
        f"cd {folder}",
        "npm install",
        "npm install -D tailwindcss postcss autoprefixer",
        "npx tailwindcss init -p",
        "npm install framer-motion",
        "echo '@tailwind base;' > src/index.css",
        "echo '@tailwind components;' >> src/index.css",
        "echo '@tailwind utilities;' >> src/index.css",
    ]

    if html_path and os.path.exists(html_path):
        with open(html_path, "r") as html:
            html_content = html.read().strip()
        jsx_note = "\n\n# ⚠️ Convert this manually into JSX and insert into App.jsx\n"
        steps.append(f"echo '{jsx_note}{html_content}' > {folder}/src/__from_html.html")

    setup_script = "\n".join(steps)

    with open("setup.sh", "w") as f:
        f.write("#!/bin/bash\nset -e\n\n" + setup_script)

    os.chmod("setup.sh", 0o755)
    print("🛠️ Setup script created as `setup.sh`.\n")
    run_now = input("🚀 Run it now? (y/n): ").strip().lower()
    if run_now == "y":
        os.system("bash setup.sh")

# --- Code Generator ---
async def generate_code_to_file(request: str, filename: str):
    language = detect_language_from_filename(filename)
    prompt = (
        f"You are an expert {language} developer. Generate code based on the following user request:\n\n"
        f"{request.strip()}\n\n"
        f"Write valid code that belongs in the file: {filename}.\n"
        f"Use best practices for that language. Be complete but concise. No explanations."
    )

    print(f"\U0001F4A1 Generating code for {filename}...\n")
    try:
        response = model.generate_content(prompt)
        code = response.text.strip()

        with open(filename, "w") as f:
            f.write(code)

        print(f"✅ Code written to '{filename}' successfully.\n")

        run = input(f"🚀 Do you want to run '{filename}' now? (y/n): ").lower()
        if run == "y":
            run_cmd = f"python {filename}" if filename.endswith(".py") else f"echo 'Running {filename} not supported yet'"
            os.system(run_cmd)

        edit = input(f"📝 Open '{filename}' in VS Code or nano? (v/n/skip): ").lower()
        if edit == "v":
            os.system(f"code {filename}")
        elif edit == "n":
            os.system(f"nano {filename}")

    except Exception as e:
        print(f"❌ Failed to generate code: {e}")

# --- Refactor Code ---
async def refactor_file_with_gemini(filename: str, task: str):
    if not os.path.exists(filename):
        print(f"❌ File '{filename}' not found.")
        return

    with open(filename, "r") as f:
        content = f.read()

    prompt = (
        f"You are an expert developer. Here's a task for you:\n\n"
        f"{task.strip()}\n\n"
        f"Refactor the following file content accordingly:\n\n"
        f"{content}"
    )

    print(f"\U0001F4A1 Refactoring '{filename}' based on: {task}...\n")

    try:
        response = model.generate_content(prompt)
        new_code = response.text.strip()

        with open(filename, "w") as f:
            f.write(new_code)

        print(f"✅ File '{filename}' updated successfully.\n")
    except Exception as e:
        print(f"❌ Refactoring failed: {e}")

# --- Main Dev Shell ---
async def run_dev_shell():
    print("👨‍💻 Ray Dev Mode activated.")
    print("Type natural language to generate, explain, or refactor code.")
    print("Examples:")
    print("• write a todo app in app.jsx")
    print("• generate a basic SQL schema")
    print("• refactor app.py to use async")
    print("• explain this code (paste it in)")
    print("Type 'exit' to quit.\n")

    buffer = []

    while True:
        try:
            command = input("dev> ").strip()

            if command.lower() in ["exit", "quit"]:
                print("👋 Exiting Dev Mode.")
                break

            if is_setup_env_request(command):
                await handle_env_setup(command)
                continue

            if any(command.lower().startswith(x) for x in ["write", "create", "generate"]):
                if " in " in command:
                    parts = command.rsplit(" in ", 1)
                    request, filename = parts
                    filename = filename.strip()
                else:
                    request = command
                    filename = input("📄 What filename should I save the code in (e.g. `main.py`)? ").strip()
                    default_ext = {
                        "python": "py", "react": "jsx", "html": "html", "javascript": "js",
                        "typescript": "ts", "java": "java", "c++": "cpp", "c#": "cs", "php": "php"
                    }
                    name = filename.lower().replace(" ", "")
                    if "." not in name:
                        ext = default_ext.get(name, "txt")
                        filename = f"{name}.{ext}"
                        print(f"📁 No file extension given — assuming '{filename}'")

                await generate_code_to_file(request, filename)
                continue

            if command.lower().startswith("refactor "):
                match = re.match(r"refactor (.+) to (.+)", command.lower())
                if match:
                    filename, task = match.groups()
                    await refactor_file_with_gemini(filename.strip(), task.strip())
                else:
                    print("⚠️ Usage: refactor <filename> to <task>")
                continue

            if is_codey_snippet(command):
                buffer.append(command)
                print("📋 Ray-i detected code... paste more lines or press Enter to analyze")
                while True:
                    line = input("... ").strip()
                    if line == "":
                        break
                    buffer.append(line)
                code = "\n".join(buffer)
                buffer.clear()
                await explain_code_with_gemini(code)
                continue

            if is_explanation_request(command):
                print("📋 Paste the code you want explained (end with empty line):")
                lines = []
                while True:
                    line = input("... ").strip()
                    if line == "":
                        break
                    lines.append(line)
                code_snippet = "\n".join(lines)
                await explain_code_with_gemini(code_snippet)
                continue

            print("💡 Ray-i is thinking... (This may take a few seconds)\n")
            print(f"🛠️ Running: {command}\n")

            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await process.communicate()
            output = (stdout + stderr).decode().strip()
            print(output)

            if stderr:
                print("\n🧠 Ray-i is analyzing the error...\n")
                await explain_error_with_gemini(command, output)

        except KeyboardInterrupt:
            print("\n❌ Ray Dev interrupted.")
            break

# --- Gemini Helpers ---
async def explain_error_with_gemini(command: str, output: str):
    prompt = (
        f"You are a helpful coding assistant. Analyze the following command output "
        f"and explain any errors. Suggest concrete fixes if needed.\n\n"
        f"Command: {command}\n\nOutput:\n{output}"
    )
    try:
        response = model.generate_content(prompt)
        print("💡 Ray-i Suggests:\n", response.text.strip())
    except Exception as e:
        print("❌ Failed to analyze with Gemini:", e)

async def explain_code_with_gemini(code: str):
    prompt = (
        "You're an expert programming mentor. Explain the following code **line-by-line**, "
        "clearly and simply for beginners:\n\n"
        f"{code}"
    )
    try:
        response = model.generate_content(prompt)
        print("\n🧠 Ray-i Explains:\n")
        print(response.text.strip())
    except Exception as e:
        print("❌ Failed to explain code with Gemini:", e)
