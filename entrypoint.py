import os
import subprocess

subprocess.run(["python", "main.py"], check=True)
subprocess.run([
    "streamlit", "run",
    "dashboard/app.py",
    "--server.port", os.getenv("PORT", "8501"),
    "--server.address", "0.0.0.0"
])
