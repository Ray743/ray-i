# modules/daemon.py
import asyncio
import os
from datetime import datetime

INPUT_FILE = "ray_input.txt"

async def run_daemon():
    print("📡 Ray Daemon started. Listening for file triggers (ray_input.txt)...")
    last_seen = ""

    while True:
        if os.path.exists(INPUT_FILE):
            with open(INPUT_FILE, "r") as f:
                task = f.read().strip()

            if task and task != last_seen:
                last_seen = task
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"\n🧠 [{timestamp}] Ray-i picked up: {task}")
                
                # Run the Ray command directly (using alias or symlink)
                os.system(f'/mnt/c/Users/Clinet/Documents/ray-bash/ray {task}')

                
                # Clear the file to prevent re-execution
                open(INPUT_FILE, "w").close()

        await asyncio.sleep(1)  # Feel responsive without high CPU usage
