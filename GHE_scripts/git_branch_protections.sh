#!/bin/bash

# Aim: This script is used to set branch protection for all repos in organisation. 
# Prerequisites: 
#    - Install GitHub’s official CLI tool and login, authentication to your github. 

# Set the GitHub Org name below
printf "**Imp** :- This Script will apply changes for all repos in an ORG. \n Enter the GitHub org Name:  "
read org_name

# Delete and Create a new output log file
OP_LOGFILE=/tmp/get_branch_details.txt
rm -rf "$OP_LOGFILE" && touch "$org_name"

# Function to to get required_pull_request_reviews protection for *master* branch
branch_name="master"
get_branch_protection() {
    gh api \
        -H "Accept: application/vnd.github.v3+json" \
        repos/"$org_name"/"$repo_name"/branches/"$branch_name"/protection/required_pull_request_reviews

}

# Declare an array for branchs
declare -a BranchArray=("master" "main")

# Function to set the [master,main] branch protection using GraphQL
put_branch_protection() {
    repositoryId="$(gh api graphql -f query='{repository(owner:"'$org_name'",name:"'$repo_name'"){id}}' -q .data.repository.id)"
    gh api graphql -f query='
        mutation($repositoryId:ID!,$branch:String!,$requiredReviews:Int!) {
        createBranchProtectionRule(input: {
            repositoryId: $repositoryId
            pattern: $branch
            dismissesStaleReviews: true
            requiresApprovingReviews: true
            requiredApprovingReviewCount: $requiredReviews
        }) { clientMutationId }
        }' -f repositoryId="$repositoryId" -f branch="$branch_name" -F requiredReviews=1
}

# Set Text Formatting
bold=$(tput bold)
normal=$(tput sgr0)

# Call above funtions for all repos inside organisation
for repo_name in `gh repo list "$org_name" -L500 --no-archived --json name -q '.[].name'`
do 
    printf "*********** \n    Repository Name: ${bold}$repo_name $normal \n"
    for branch_name in ${BranchArray[@]}
    do
        printf "\n ${bold} **** Checking for ${bold}$branch_name $normal branch ----  \n \n"
        get_branch_protection | tee $OP_LOGFILE
        if grep -q "Branch not found" $OP_LOGFILE; then
            printf "\n \n  ${bold} ------------ As Branch doesn't exist. No action is needed. \n"
        elif grep -E 'dismiss_stale_reviews|require_code_owner_reviews|required_approving_review_count' $OP_LOGFILE; then
            printf "\n ${bold} ------------ Already Branch protection applied for $branch_name. \n"
        else
            printf "\n ${bold} ++ Applying for $branch_name $normal.... \n"
            put_branch_protection
            if [ $? == 0 ]; then
                printf "${bold} ++ Applied protection rule \n"
                printf " -------------------------- \n"
            else 
                printf "${bold} ------------ Setting branch Protection Failed."
                exit 1
            fi
        fi
    done
    printf "\n ${bold} **** Applying for release-wildcard $normal.... \n"
    export branch_name="release-*" && put_branch_protection
    printf "${bold} applied protection rule \n"

done