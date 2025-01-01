import subprocess
import os
from datetime import datetime, timedelta

log_file = "log.txt"

# Start from Jan 1 2025
start_date = datetime(2025, 1, 1)
end_date = datetime(2026, 6, 19)

current = start_date
i = 1

while current <= end_date:
    date_str = current.strftime("%Y-%m-%d")

    with open(log_file, "a") as f:
        f.write(f"commit on {date_str} - {i}\n")

    subprocess.run(["git", "add", "."])

    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = f"{date_str} 12:00:00"
    env["GIT_COMMITTER_DATE"] = f"{date_str} 12:00:00"

    subprocess.run(
        ["git", "commit", "-m", f"day {i}"],
        env=env
    )

    current += timedelta(days=1)
    i += 1

print("All done! Now run: git push -u origin main")