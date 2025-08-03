# github_uploader.py
import os
from dotenv import load_dotenv
from github import Github
from pathlib import Path

# טוען את הטוקן מה-.env
load_dotenv()
token = os.getenv("GITHUB_TOKEN")
repo_name = "gpt_assistant"  # שם הריפו שלך

if not token:
    print("❌ לא נמצא GITHUB_TOKEN בקובץ .env")
    exit()

g = Github(token)
user = g.get_user()

# מוצא את הריפו שלך
repo = None
for r in user.get_repos():
    if r.name == repo_name:
        repo = r
        break

if repo is None:
    print(f"❌ לא נמצא ריפוזיטורי בשם {repo_name}")
    exit()

# כל הקבצים להעלאה
def get_files_to_upload(folder_path):
    paths = []
    for path in Path(folder_path).rglob("*"):
        if path.is_file() and not any(skip in str(path) for skip in ["__pycache__", ".git", ".env", ".DS_Store"]):
            paths.append(path)
    return paths

# מעלה כל קובץ לגיטהאב
def upload_files_to_github(repo, folder_path):
    files = get_files_to_upload(folder_path)
    for file_path in files:
        relative_path = file_path.relative_to(folder_path).as_posix()
        try:
            contents = repo.get_contents(relative_path)
            repo.update_file(contents.path, f"🔄 Update {relative_path}", file_path.read_text(encoding="utf-8"), contents.sha)
            print(f"✅ Updated: {relative_path}")
        except:
            repo.create_file(relative_path, f"🆕 Add {relative_path}", file_path.read_text(encoding="utf-8"))
            print(f"🆕 Created: {relative_path}")

# ⬆️ מפעיל את ההעלאה
upload_files_to_github(repo, Path("."))
