import git
import os
import toml
import pip
import tempfile
from typing import List

# Get information about what repos we are using
# Before running main, we check if we match dependencies
# If we match, we go ahead with the build
# If not, we download the new git dependencies
# Update the result to the requirements.txt file
# Run Main
def get_repository_tags(org_name: str, repo_name: str, pat: str) -> List[str]:
    url = "https://" + pat + ":x-oauth-basic@github.com/"
    if "/" not in repo_name:
        url += org_name + "/"
    url += repo_name
    tmp_dir = tempfile.mkdtemp()
    repo = git.Repo.clone_from(url, tmp_dir)
    tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime, reverse=True)
    return tags


if __name__ == "__main__":
    print(
        get_repository_tags(
            org_name="pandas-dev",
            repo_name="pandas",
            pat=os.environ["pyroboros_key"],
        )
    )
