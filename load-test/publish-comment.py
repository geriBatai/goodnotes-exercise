#!/usr/bin/env python

import requests
import argparse
import os
import json

class GitHubCommentPost:
    def __init__(self, repo, token, pr_number):
        self.url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    
        self.token = token


    def post_comment(self, comment):
        """ Posts comment """
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {
            "body": comment
        }
        response = requests.post(self.url, headers=headers, json=data)
        return response.json()


def get_pr_data():
    event_path = os.environ.get("GITHUB_EVENT_PATH")

    with open(event_path, "r") as f:
        event = json.load(f)

    if event is None or event["pull_request"] is None or event["repository"] is None:
        return None
        
    return {
        "pr_number":  event["pull_request"]["number"],
        "repo": event["repository"]["full_name"]
    }




if __name__ == '__main__':
    parser = argparse.ArgumentParser("Send comment to GitHub PR")
    parser.add_argument("-f", "--filename", help="filename to the content of a comment to post")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    pr = get_pr_data()

    if token is None or pr is None:
        print("Could not determine GitHub PR, are you running the script from GitHub action?", file=sys.stderr)
        sys.exit(1)

    with open(args.filename, "r") as f:
        comment = f.read()


    print(f"comment file: {args.filename}")
    print(f"comment: {comment}")


    gh = GitHubCommentPost(pr["repo"], token, pr["pr_number"])
    gh.post_comment(comment)
