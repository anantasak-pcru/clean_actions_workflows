import http.client
import os
import requests
import pprint
from dotenv import load_dotenv

load_dotenv()

repository = os.environ["REPOSITORY"]
token = os.environ["GITHUB_TOKEN"]
status = os.environ["STATUS"]

actions_url = "https://api.github.com/repos/{repo}/actions/runs?status={status}&per_page=10".format(repo=repository, status=status)
delete_url = "https://api.github.com/repos/{}/actions/runs/".format(repository)

header = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Accept": "application/vnd.github.v3+json"
}

print("🚀 Start working...")

while True:
    res = requests.get(url=actions_url,headers=header)
    if(res.status_code != 200):
        raise Exception("Can't feed Workflows")
    workflow_runs = res.json()['workflow_runs']
    if(len(workflow_runs) == 0): break
    for work in workflow_runs:
        run_id = str(work['id'])
        url = delete_url + run_id
        res=requests.delete(url=url, headers=header)
        if(res.status_code == 204):
            print("🗑️ Deleted {} success.".format(run_id))

print("🎉 Clean success...")


