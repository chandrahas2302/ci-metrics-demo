import os 
import json
import subprocess
from datetime import datetime 

def run(cmd):
    try:
        return subprocess.check_output(cmd,shell=True).decode().strip()
    
    except Exception:
        return ""
    
branch  =  os.getenv("GITHUB_REF_NAME","")
is_production = int(branch in ["main","master"])

first_commit = run("git rev-list --max-parents=0 HEAD")
first_date = run(f"git show -s --format=%ci {first_commit}")

project_age_days = (
    (datetime.utcnow() - datetime.fromisoformat(first_date[:19])).days
    if first_date else 0
)

last_date = run("git show -s --format=%ci HEAD")
days_since_last_push = (
    (datetime.utcnow() - datetime.fromisoformat(last_date[:19])).days
    if last_date else 0
)

diff = run("git diff --shortstat HEAD~1")

avg_file_churn = 0
if diff:
    try:
        avg_file_churn = int(diff.split()[3]) + int(diff.split()[5])
    except Exception:
        pass

build_tool_count = int(os.path.exists("requirements.txt"))

payload = {
    "total_tasks": 10,
    "is_production": is_production,
    "failed_tasks": 0,
    "stage_count": 1,
    "task_failure_rate": 0.0,
    "project_age_days": project_age_days,
    "days_since_last_push": days_since_last_push,
    "stars_to_forks_ratio": 1.0,
    "build_tool_count": build_tool_count,
    "uses_legacy_build": 0,
    "uses_multiple_ides": 0,
    "uses_ci_and_submodules": 0,
    "avg_file_churn": avg_file_churn,
    "new_file_ratio": 0.1,
    "dependency_error_rate": 0.0,
    "compiler_error_rate": 0.0
}

    
with open("metrics.json","w") as f:
    json.dump(payload,f,indent=2)

print(json.dumps(payload,indent=2))