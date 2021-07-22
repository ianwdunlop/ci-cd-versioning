#! /usr/bin/python3

import os
import re
import requests
from requests.models import HTTPError

if os.getenv("NO_RELEASE") == "false":
    sanitized_log = re.sub('>', '&gt', re.sub('"', '&quot', re.sub('<', '&lt', re.sub('&', '&amp', os.getenv("GIT_LOG")))))
    project_id = os.getenv("CI_PROJECT_ID")
    api_url = os.getenv("CI_API_V4_URL")
    response = requests.post(f"{api_url}/projects/{project_id}/releases", 
                  json={"name": os.getenv("RELEASE_TAG"), "tag_name": os.getenv("RELEASE_TAG"), "description": f"##Changelog\n\n{sanitized_log}"},
                  headers={"PRIVATE-TOKEN": os.getenv("CI_TOKEN")})
    print(response.json())
    if response.status_code >= 400:
        raise HTTPError

    