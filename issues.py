import requests
import random
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

issues_titles = [
    "Add blog section", "Fix comment system", "Improve post editor",
    "Add tags feature", "Fix image upload", "Add category filter",
    "Improve SEO settings", "Fix broken RSS feed", "Add related posts",
    "Optimize page speed", "Fix meta tags", "Add sitemap generation"
]

print("Creating issues...")
issue_numbers = []
for title in issues_titles:
    r = requests.post(f"{base_url}/issues",
        headers=headers,
        json={"title": title, "body": "This needs to be fixed."}
    )
    if r.status_code == 201:
        issue_numbers.append(r.json()["number"])
        print(f"✅ Issue created: {title}")
    time.sleep(1)

print("\nClosing some issues...")
for num in issue_numbers[:6]:
    requests.patch(f"{base_url}/issues/{num}",
        headers=headers,
        json={"state": "closed"}
    )
    print(f"✅ Issue #{num} closed")
    time.sleep(1)

print("\nCreating branch and pull request...")
# Get main branch SHA
r = requests.get(f"{base_url}/git/ref/heads/main", headers=headers)
sha = r.json()["object"]["sha"]

# Create new branch
branch_name = "feature-update"
requests.post(f"{base_url}/git/refs",
    headers=headers,
    json={
        "ref": f"refs/heads/{branch_name}",
        "sha": sha
    }
)
print(f"✅ Branch created: {branch_name}")
time.sleep(1)

# Get file to update
r = requests.get(f"{base_url}/contents/log.txt", headers=headers)
file_sha = r.json()["sha"]

# Update file in new branch
import base64
content = base64.b64encode(b"updated content for PR").decode()
requests.put(f"{base_url}/contents/log.txt",
    headers=headers,
    json={
        "message": "Update log.txt",
        "content": content,
        "sha": file_sha,
        "branch": branch_name
    }
)
print("✅ File updated in branch")
time.sleep(1)

# Create Pull Request
r = requests.post(f"{base_url}/pulls",
    headers=headers,
    json={
        "title": "Feature update",
        "body": "This PR adds new improvements.",
        "head": branch_name,
        "base": "main"
    }
)
if r.status_code == 201:
    pr_number = r.json()["number"]
    print(f"✅ Pull Request created: #{pr_number}")

    # Add review comment
    time.sleep(1)
    requests.post(f"{base_url}/pulls/{pr_number}/reviews",
        headers=headers,
        json={
            "body": "Looks good to me!",
            "event": "APPROVE"
        }
    )
    print("✅ Code review added")

    # Merge PR
    time.sleep(1)
    requests.put(f"{base_url}/pulls/{pr_number}/merge",
        headers=headers,
        json={"merge_method": "merge"}
    )
    print("✅ Pull Request merged")

print("\n🎉 All done! Check your GitHub profile activity chart!")