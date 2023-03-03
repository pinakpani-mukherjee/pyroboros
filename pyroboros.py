from git import Repo
import os
import toml
import pip
import tempfile
from typing import List
import re

# Get information about what repos we are using
# Before running main, we check if we match dependencies
# If we match, we go ahead with the build
# If not, we download the new git dependencies
# Update the result to the requirements.txt file
# Run Main


class Pyroboros:
    def __init__(self, org_name: str, repo_name: str, pat: str) -> None:
        self.org_name = org_name
        self.repo_name = repo_name
        self.pat = pat

    def get_repository_tags(self) -> List[str]:
        url = "https://" + self.pat + ":x-oauth-basic@github.com/"
        if "/" not in self.repo_name:
            url += self.org_name + "/"
        url += self.repo_name
        tmp_dir = tempfile.mkdtemp()
        repo = Repo.clone_from(url, tmp_dir)
        tags = sorted(
            repo.tags, key=lambda t: t.commit.committed_datetime, reverse=True
        )
        return tags

    def search_for_specific_tag(self, list_of_tags: List, tag_format: str = "v.n.n.n"):
        regex_value = tag_format.replace("n", "[A-Za-z0-9]+").replace(".", "\.")
        pattern = re.compile(regex_value, re.IGNORECASE)
        for tag in list_of_tags:
            if pattern.match(str(tag)):
                return tag

    def get_latest_prod_tag(self, prod_tag_format: str):
        tags = self.get_repository_tags()
        return self.search_for_specific_tag(
            list_of_tags=tags, tag_format=prod_tag_format
        )

    def get_latest_dev_tag(self, dev_tag_format: str):
        tags = self.get_repository_tags()
        return self.search_for_specific_tag(
            list_of_tags=tags, tag_format=dev_tag_format
        )


if __name__ == "__main__":
    tags = get_repository_tags(
        org_name="Arkhon-Tech",
        repo_name="arkhon-bot-flows",
        pat=os.environ["pyroboros_key"],
    )
    print(search_for_specific_tag(list_of_tags=tags, tag_format="vn.n.n-base"))
