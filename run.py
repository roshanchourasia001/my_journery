import subprocess
import os
from datetime import datetime, timedelta

log_file = "log.txt"
start_date = datetime.now() - timedelta(days=365)

for i in range(365):
    day = start_date + timedelta(days=i)
    date_str = day.strftime("%Y-%m-%d")

    with open(log_file, "a") as f:
        f.write(f"commit on {date_str}\n")

    subprocess.run(["git", "add", "."])

    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = f"{date_str} 12:00:00"
    env["GIT_COMMITTER_DATE"] = f"{date_str} 12:00:00"

    subprocess.run(
        ["git", "commit", "-m", f"day {i+1}"],
        env=env
    )

print("All done! Now run: git push -u origin main")