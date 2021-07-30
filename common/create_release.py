#! /usr/bin/python3

import os
import requests
from requests.models import HTTPError

def create_release(tag: str, log: str, ci_token: str):
    
    # These are gitlab builtin CI variables.
    project_id = os.getenv("CI_PROJECT_ID")
    api_url = os.getenv("CI_API_V4_URL")
    
    response = requests.post(f"{api_url}/projects/{project_id}/releases", 
                json={"name": tag, "tag_name": tag, "description": f"##Changelog\n\n{log}"},
                headers={"PRIVATE-TOKEN": ci_token})
    print(response.json())
    if response.status_code >= 400:
        raise HTTPError

if __name__ == "__main__":
    tag = os.getenv("RELEASE_TAG")
    if not tag:
        raise EnvironmentError("missing environment variable RELEASE_TAG")


    git_log = os.getenv("GIT_LOG")
    if not git_log:
        raise EnvironmentError("missing environment variable GIT_LOG")


    ci_token = os.getenv("CI_TOKEN")
    if not ci_token:
        raise EnvironmentError("missing environment variable CI_TOKEN")
    
    create_release(tag, git_log, ci_token)