import os
import git
import subprocess
import time

repo_path = "konnect-app/"

branch = "main"

def restart_server():
    os.system("kill -9 $(lsof -t -i:3000)")
    os.chdir(repo_path)
    subprocess.Popen(["npm", "run", "dev", "--", "--port=3000"])
    os.chdir("..")



if not os.path.exists(repo_path):
    git.Repo.clone_from("git@github.com:Felixdiamond/konnect-app.git", repo_path)


subprocess.run(["npm", "install"], cwd=repo_path)


restart_server()

repo = git.Repo(repo_path)

last_commit = None

while True:
    repo.remote().pull(branch)

    current_commit = next(repo.iter_commits(f"origin/{branch}"), None)

    if current_commit and current_commit != last_commit:
        print("New commits detected, pulling updates...")
        repo.remote().pull(branch)
        print("Updates pulled, restarting npm server...")
        restart_server()
        last_commit = current_commit
    else:
        print("No new commits, checking again in 60 seconds...")

    time.sleep(60)