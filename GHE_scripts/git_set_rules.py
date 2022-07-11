# Required Module
from github import Github
import requests

# First create a Github instance:
# using an access token
g = Github("<token>")

# Github Enterprise with custom hostname
g = Github(base_url="https://ghe.eng.fireeye.com/api/v3", login_or_token="<token>")

# REST API related stuff
headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': 'token <token>',
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = '{"dismiss_stale_reviews":true,"require_code_owner_reviews":true,"required_approving_review_count":1}'

# Function to Apply branch Protection Rule.
def add_branch_protection(own_org_name, repo_name, branch_name):
    url = ("https://ghe.eng.fireeye.com/api/v3/repos/%s" %(own_org_name)+"/%s" %(repo_name)+"/branches/%s" %(branch_name)+"/protection/required_pull_request_reviews")
    print(url)
    response = requests.patch(url, headers=headers, data=data)
    print(response)


# Then Get list of Repos in organisation with your Github objects:

# for repo in g.get_organization("sre-devops").get_repos():
#     print(repo.name)
#     print(repo.get_branch(branch="master"))
#     try:
#         g.get_repo("sre-devops"+"/"+repo.name).get_branch("master").get_required_pull_request_reviews()
#     except:
#         print("An exception occurred")
#     break

BranchList = ["master", "main"]

for repo in g.get_user("chaman-rathee").get_repos():
    print(repo.name)
    for branchName in BranchList:
        try: 
            g.get_repo("chaman-rathee"+"/"+repo.name).get_branch(branchName).get_required_pull_request_reviews()
        except Exception as e:
            eStr = str(e)
            if "Branch not found" in eStr:
                print("No Need to Apply Protection, As Branch not available.")
            if "Branch not protected" in eStr:
                print("Apply Branch Protection")
                add_branch_protection("chaman-rathee", repo.name, branchName)
        break
