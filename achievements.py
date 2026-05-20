import requests
import base64
import time

# ===== FILL THESE =====
USERNAME = "roshanchourasia001"
REPO = "my_journery"
TOKEN = "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"  # paste your token here
# ======================

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

base_url = f"https://api.github.com/repos/{USERNAME}/{REPO}"

def get_main_sha():
    r = requests.get(f"{base_url}/git/ref/heads/main", headers=headers)
    return r.json()["object"]["sha"]

def create_branch(branch_name, sha):
    requests.post(f"{base_url}/git/refs",
        headers=headers,
        json={
            "ref": f"refs/heads/{branch_name}",
            "sha": sha
        }
    )
    print(f"✅ Branch created: {branch_name}")
    time.sleep(1)

def update_file(branch_name, content_text, i):
    # Get file
    r = requests.get(f"{base_url}/contents/log.txt", 
        headers=headers,
        params={"ref": branch_name}
    )
    file_sha = r.json()["sha"]
    
    content = base64.b64encode(content_text.encode()).decode()
    requests.put(f"{base_url}/contents/log.txt",
        headers=headers,
        json={
            "message": f"Update feature {i}",
            "content": content,
            "sha": file_sha,
            "branch": branch_name
        }
    )
    print(f"✅ File updated in branch {branch_name}")
    time.sleep(1)

def create_and_merge_pr(branch_name, i):
    # Create PR
    r = requests.post(f"{base_url}/pulls",
        headers=headers,
        json={
            "title": f"Feature {i} improvements",
            "body": f"This PR adds feature {i} improvements.",
            "head": branch_name,
            "base": "main"
        }
    )
    if r.status_code == 201:
        pr_number = r.json()["number"]
        print(f"✅ PR created: #{pr_number}")
        time.sleep(1)

        # Add review
        requests.post(f"{base_url}/pulls/{pr_number}/reviews",
            headers=headers,
            json={
                "body": "Looks great!",
                "event": "APPROVE"
            }
        )
        print(f"✅ Review added on PR #{pr_number}")
        time.sleep(1)

        # Merge PR
        r = requests.put(f"{base_url}/pulls/{pr_number}/merge",
            headers=headers,
            json={"merge_method": "merge"}
        )
        if r.status_code == 200:
            print(f"✅ PR #{pr_number} merged!")
        time.sleep(2)
    else:
        print(f"❌ PR failed: {r.json()}")

# ===== MAIN =====
pr_details = [
    ("feature-login-update", "login feature updated"),
    ("feature-dashboard-fix", "dashboard bug fixed"),
    ("feature-profile-update", "profile page updated"),
    ("feature-settings-fix", "settings page fixed"),
    ("feature-api-update", "api endpoints updated"),
    ("feature-ui-improvements", "ui improvements added"),
    ("feature-performance-fix", "performance optimized"),
    ("feature-security-update", "security patches added"),
]

print("🚀 Starting achievement script...\n")

for i, (branch_name, content) in enumerate(pr_details, 1):
    print(f"\n--- PR {i} ---")
    sha = get_main_sha()
    create_branch(branch_name, sha)
    update_file(branch_name, content, i)
    create_and_merge_pr(branch_name, i)

print("\n🎉 All done!")
print("Check your GitHub profile for these achievements:")
print("🐙 Pull Shark - for merged Pull Requests")
print("⭐ Quickdraw - for fast issue closing")