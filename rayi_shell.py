#!/usr/bin/env python3

from openai import OpenAI
from dotenv import load_dotenv
import os
import subprocess
from datetime import datetime

# Load API Key
load_dotenv()
client = OpenAI(api_key=os.getenv("api_key"))

cwd = os.getcwd()

print("\n🧠 Ray-i Activated.")
print("🤖 What can I do for you, bruh? 🔥")
print("💡 Type 'exit' or 'quit' to shut me down.\n")

while True:
    user_input = input("➤ ").strip()
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Shutting down... Mi stap.")
        break

    if not user_input:
        continue

    messages = [
        {
            "role": "system",
            "content": (
                "You are an advanced Linux shell expert. Your job is to read a human's plain English instruction "
                "and convert it into a safe, accurate bash command ONLY. Do not explain. No markdown. No comments. "
                f"Only the raw command. Assume the user is currently in this path: {cwd}"
            ),
        },
        {"role": "user", "content": user_input},
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        command = response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ GPT failed:", e)
        continue

    # Dangerous command check
    dangerous = ["rm", "shutdown", "reboot", "mkfs", ":(){:|:&};:", "dd", "curl | sh"]
    if any(d in command for d in dangerous):
        print("⛔ Ray-i: Displa command look dangerous ya. Mi no inap ranim.")
        continue

    print(f"\n🧠 Ray-i Suggests: \033[92m{command}\033[0m")
    confirm = input("⚠️  Do you want me to run this command? (y/n): ").strip().lower()
    if confirm == "y":
        try:
            subprocess.run(["sudo", "bash", "-c", command], check=True)
            with open("rayi.log", "a") as log:
                log.write(f"[{datetime.now()}] {command}\n")
        except subprocess.CalledProcessError as e:
            print("❌ Execution failed:", e)
    else:
        print("❌ Canceled.")

