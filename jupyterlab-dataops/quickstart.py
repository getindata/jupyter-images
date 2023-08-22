import pathlib
import random
import re
import string
import subprocess
import sys
from typing import Any, List, Tuple

DP_INIT_LINK = "https://gitlab.com/bdtw-mdp-workshop/dp-init"
GITLAB_REPOSITORY_BASE_URL = "https://gitlab.com/bdtw-mdp-workshop/"
DP_TEMPLATE_NAME = "bdtw-mdp-workshop"
GCP_PROJECT_ID = "bdtw-mdp-workshop"


def dbt_username_from_gitlab_username(gitlab_username: str) -> str:
    username = gitlab_username.split("@")[0]
    username = re.sub(r"\W+", "_", username)  # remove non-alphanumeric-characters
    if not username[0].isalpha():  # BigQuery name has to start with either letter or underscore
        username = f"{random.choice(string.ascii_lowercase)}_{username}"
    return username

def dbt_project_name(gitlab_project_name: str) -> str:
    return gitlab_project_name.replace("-", "_")


def gitlab_repository_link(gitlab_repository_name: str) -> Tuple[str, str]:
    if gitlab_repository_name.startswith("http") or gitlab_repository_name.startswith("git"):
        gitlab_link = gitlab_repository_name
        project_name = gitlab_repository_name.split("/")[-1]
        if project_name.endswith(".git"):
            project_name = project_name[:-4]
    else:
        gitlab_link = f"{GITLAB_REPOSITORY_BASE_URL}{gitlab_repository_name}"
        project_name = gitlab_repository_name
    return gitlab_link, project_name


def subprocess_run_quiet(
    process_args: List[str], **kwargs: Any
):
    return subprocess.run(
        process_args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **kwargs
    )


def quickstart(gitlab_username: str, email: str, gitlab_repository_name: str) -> None:
    repo_link, gitlab_project_name = gitlab_repository_link(gitlab_repository_name)
    print(f"GitLab username: {gitlab_username}\nGitLab repository link: {repo_link}\n")

    subprocess_run_quiet(["git", "config", "--global", "credential.helper", "cache"])
    subprocess_run_quiet(["git", "config", "--global", "user.name", gitlab_username])
    subprocess_run_quiet(["git", "config", "--global", "user.email", email])

    dbt_username = dbt_username_from_gitlab_username(gitlab_username)
    print(f"dbt username: {dbt_username}")

    print("Running 'dp init'...")
    subprocess_run_quiet(["dp", "init", DP_INIT_LINK], text=True, input=dbt_username)

    print(f"Running 'git clone {repo_link}'...")
    subprocess_run_quiet(["git", "clone", repo_link])
    if not (pathlib.Path.cwd() / gitlab_project_name).exists():
        print(f"Unexpected problem: directory {gitlab_project_name} does not exist!")
        sys.exit(1)

    print("Running 'dp create'...")
    dp_create_input = "\n".join(
        [
            dbt_project_name(gitlab_project_name),  # project_name
            GCP_PROJECT_ID,  # gcp_project_id
            dbt_username,  # project_owner
            dbt_username,  # dataset
        ]
    )
    subprocess_run_quiet(
        ["dp", "create", gitlab_project_name, DP_TEMPLATE_NAME], text=True, input=dp_create_input
    )

    print("Running 'dp prepare-env'...")
    subprocess_run_quiet(["dp", "prepare-env"], cwd=gitlab_project_name)

    print("Making an initial commit")
    subprocess_run_quiet(["git", "add", "."], cwd=gitlab_project_name)
    subprocess_run_quiet(["git", "commit", "-m", "\"Initial commit\""], cwd=gitlab_project_name)
    subprocess_run_quiet(["git", "push", "origin", "main", "-u"], cwd=gitlab_project_name)

    print(f"{gitlab_project_name} created. Input 'cd {gitlab_project_name}' into the terminal to access it.")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: python {__file__} gitlab_username email gitlab_repository_name")
        sys.exit(1)

    quickstart(gitlab_username=sys.argv[1], email=sys.argv[2], gitlab_repository_name=sys.argv[3])
