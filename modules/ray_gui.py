# ray_gui.py

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import asyncio
import os
from dotenv import load_dotenv
import google.generativeai as genai
import pyttsx3  # 🔊 Voice engine

# --- Load Environment & Gemini ---
load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# --- Voice Engine Setup ---
voice_engine = pyttsx3.init()
voice_engine.setProperty("rate", 140)  # Slower for deep effect
voices = voice_engine.getProperty("voices")

# Try to select deep male voice (like Optimus Prime)
for v in voices:
    if "male" in v.name.lower() or "baritone" in v.name.lower():
        voice_engine.setProperty("voice", v.id)
        break

def speak(text):
    voice_engine.say(text)
    voice_engine.runAndWait()

# --- Language Detection ---
def detect_language_from_filename(filename):
    ext_map = {
        ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript", ".html": "HTML",
        ".css": "CSS", ".jsx": "React (JSX)", ".tsx": "React (TSX)", ".cpp": "C++",
        ".java": "Java", ".sh": "Shell", ".php": "PHP", ".rb": "Ruby",
    }
    _, ext = os.path.splitext(filename.lower())
    return ext_map.get(ext, "code")

# --- Code Generator ---
def generate_code(request, filename):
    language = detect_language_from_filename(filename)
    prompt = (
        f"You are an expert {language} developer. Generate code based on the request below.\n"
        f"Request: {request.strip()}\n"
        f"Save the code into a file named {filename}. Respond with only the code."
    )
    try:
        response = model.generate_content(prompt)
        code = response.text.strip()
        with open(filename, "w") as f:
            f.write(code)
        speak(f"Code saved to {filename}.")
        return code
    except Exception as e:
        error_msg = f"❌ Error: {e}"
        speak("Something went wrong.")
        return error_msg

# --- GUI App ---
class RayGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ray-i Dev GUI")
        self.geometry("850x600")
        self.configure(bg="#1e1e1e")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.create_generate_tab()
        self.create_explain_tab()

    def create_generate_tab(self):
        self.generate_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.generate_tab, text="🛠️ Generate Code")

        self.gen_request = tk.Text(self.generate_tab, height=6)
        self.gen_request.pack(padx=10, pady=5, fill="x")

        self.filename_entry = tk.Entry(self.generate_tab)
        self.filename_entry.pack(padx=10, fill="x")
        self.filename_entry.insert(0, "main.py")

        self.gen_button = tk.Button(
            self.generate_tab, text="Generate & Save", command=self.handle_generate
        )
        self.gen_button.pack(pady=5)

        self.gen_output = tk.Text(self.generate_tab)
        self.gen_output.pack(padx=10, pady=5, fill="both", expand=True)

    def create_explain_tab(self):
        self.explain_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.explain_tab, text="🧠 Explain Code")

        self.explain_input = tk.Text(self.explain_tab, height=10)
        self.explain_input.pack(padx=10, pady=5, fill="x")

        self.explain_button = tk.Button(
            self.explain_tab, text="Explain", command=self.handle_explain
        )
        self.explain_button.pack(pady=5)

        self.explain_output = tk.Text(self.explain_tab)
        self.explain_output.pack(padx=10, pady=5, fill="both", expand=True)

    def handle_generate(self):
        request = self.gen_request.get("1.0", "end").strip()
        filename = self.filename_entry.get().strip()

        if not request or not filename:
            messagebox.showwarning("Missing Info", "Please provide both request and filename.")
            return

        self.gen_output.delete("1.0", "end")
        code = generate_code(request, filename)
        self.gen_output.insert("1.0", code)

    def handle_explain(self):
        code = self.explain_input.get("1.0", "end").strip()
        if not code:
            messagebox.showwarning("No Code", "Please paste some code to explain.")
            return

        prompt = (
            "You're an expert programming mentor. Explain the following code line-by-line clearly:\n\n"
            f"{code}"
        )
        try:
            response = model.generate_content(prompt)
            explanation = response.text.strip()
            self.explain_output.delete("1.0", "end")
            self.explain_output.insert("1.0", explanation)
            speak("Here's the explanation.")
        except Exception as e:
            error_msg = f"❌ Error: {e}"
            self.explain_output.insert("1.0", error_msg)
            speak("Failed to explain code.")

if __name__ == "__main__":
    app = RayGUI()
    app.mainloop()
