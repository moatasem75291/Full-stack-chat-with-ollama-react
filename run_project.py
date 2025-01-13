import subprocess
import time
import os


def run_docker_containers():
    containers = [
        {
            "path": r"F:\Fixed Solutions\January\first_week\projects\chat_with_ollama\backend",  # Put your own Path to the project
            "command": "docker run -p 7077:7077 chat_with_ollama",
        },
        {
            "path": r"F:\Fixed Solutions\January\first_week\projects\chat_with_ollama\frontend",  # Put your own Path to the project
            "command": "docker run -p 7066:7066 chat_ui_with_ollama",
        },
    ]

    for container in containers:
        print(f"Navigating to: {container['path']}")
        os.chdir(container["path"])

        print("Waiting 4 seconds before container launch...")
        time.sleep(4)

        cmd = f"start cmd /k {container['command']}"
        print(f"Running: {cmd}")
        subprocess.Popen(cmd, shell=True)


if __name__ == "__main__":
    run_docker_containers()
