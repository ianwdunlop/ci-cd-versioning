from lib.common import ci_server_host, ci_server_port, get_ci_token
import os

def setup_go_private():
    with open(f"{os.getenv('HOME')}/.netrc", 'a') as netrc:
        netrc.write(f"""
machine {ci_server_host}
        login gitlab-ci-token
        password {get_ci_token()}
        """)
    print(f"export GOPRIVATE={ci_server_host}:{ci_server_port}/*")