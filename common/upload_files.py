#! /usr/bin/env python
import glob
import os

import requests
from requests.models import HTTPError

def upload_files(pattern: str, tag: str, ci_token: str):
    api_url = os.getenv('CI_API_V4_URL')
    project_id = os.getenv('CI_PROJECT_ID')
    for file in glob.glob(pattern, recursive=True):
        f = open(file, 'rb')
        response = requests.post(f"{api_url}/projects/{project_id}/uploads", 
                                files={'file': f},
                                headers={"PRIVATE-TOKEN": ci_token})
        f.close()
        if response.status_code >= 400:
            raise HTTPError

        link = response.json()['full_path']
        response = requests.post(f"{api_url}/projects/{project_id}/releases/{tag}/assets/links",
                                    data={"name": file, "url": link},
                                    headers={"PRIVATE-TOKEN": ci_token})

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("glob")
    parser.add_argument("tag")
    args = parser.parse_args()

    ci_token = os.getenv("CI_TOKEN")
    if not ci_token:
        raise EnvironmentError("missing environment variable CI_TOKEN")
    
    upload_files(args.glob, args.tag, ci_token)
