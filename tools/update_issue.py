#!/usr/bin/env python3
"""
Author: KoffeinFlummi, DartRuffian
Modified from: https://github.com/acemod/ACE3/blob/master/tools/deploy.py

Updates a GitHub issue to track translation progress
"""

import os
import sys
import traceback
import subprocess as sp
from github import Github, Auth


REPO_USER = "Legion-Studios"
REPO_NAME = "ls_translations"
REPO_ISSUE = 16
REPO_PATH = f"{REPO_USER}/{REPO_NAME}"


def update_translations(repo):
    diag = sp.check_output(
        ["python3", "tools/translation_progress.py", "--markdown"])
    diag = str(diag, "utf-8")
    issue = repo.get_issue(REPO_ISSUE)
    issue.edit(body=diag)


def main():
    print("Obtaining token ...")
    try:
        token = os.environ["GITHUB_TOKEN"]
        auth = Auth.Token(token)
        repo = Github(auth=auth).get_repo(REPO_PATH)
    except:
        print("Could not obtain token.")
        print(traceback.format_exc())
        return 1
    else:
        print("Token sucessfully obtained.")

    print("\nUpdating translation issue ...")
    try:
        update_translations(repo)
    except:
        print("Failed to update translation issue.")
        print(traceback.format_exc())
        return 1
    else:
        print("Translation issue successfully updated.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
