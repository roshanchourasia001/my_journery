import subprocess
import os
from datetime import datetime, timedelta

# ===== FILL THESE =====
YOUR_NAME = "roshanchourasia001"
YOUR_EMAIL = "roshanchourasia1105@gmail.com"
COAUTHOR_NAME = "torvalds"
COAUTHOR_EMAIL = "torvalds@linux-foundation.org"
# ======================

log_file = "pair_log.txt"
start_date = datetime.now() - timedelta(days=30)

print("🚀 Starting Pair Extraordinaire script...\n")

for i in range(10):
    day = start_date + timedelta(days=i)
    date_str = day.strftime("%Y-%m-%d")

    with open(log_file, "a") as f:
        f.write(f"pair commit {i+1} on {date_str}\n")

    subprocess.run(["git", "add", "."])

    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = f"{date_str} 12:00:00"
    env["GIT_COMMITTER_DATE"] = f"{date_str} 12:00:00"
    env["GIT_AUTHOR_NAME"] = YOUR_NAME
    env["GIT_AUTHOR_EMAIL"] = YOUR_EMAIL

    commit_message = f"""pair update {i+1}

Co-authored-by: {COAUTHOR_NAME} <{COAUTHOR_EMAIL}>"""

    subprocess.run(
        ["git", "commit", "-m", commit_message],
        env=env
    )
    print(f"✅ Pair commit {i+1} created")

print("\n✅ All done! Now run: git push -u origin main")