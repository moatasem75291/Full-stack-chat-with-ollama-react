import os
import subprocess
import time


def run_apps():
    apps = [
        {
            "path": r"F:\Fixed Solutions\January\first_week\projects\chat_with_ollama\frontend",
            "commands": [f"start cmd /k npm run dev"],
        },
        {
            "path": r"F:\Fixed Solutions\January\first_week\projects\chat_with_ollama\backend",
            "commands": [
                f"start cmd /k deactivate",
                f".venv\\Scripts\\activate && python app.py",
            ],
        },
    ]

    for app in apps:
        print(f"Running in path: {app['path']}")
        os.chdir(app["path"])
        for command in app["commands"]:
            print(f"Running command: {command}")
            subprocess.run(app["commands"], shell=True)
        print("Waiting 3 seconds before running the next app...")
        time.sleep(3)


if __name__ == "__main__":
    run_apps()
