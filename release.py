#!/usr/bin/python3
# Helper script to create and publish a new `berserk` release.
# Based on `release.py` from `python-chess`.
# THIS IS A COMMENT USED TO FORCE A PR FOR TESTING PURPOSES

import argparse
import os
import sys
import subprocess
import time
import re

from typing import Literal
from datetime import datetime


UN_RELEASED = "To be released\n--------------"


def system(command: str | list[str]):
    print(command)
    if isinstance(command, str):
        exit_code = subprocess.run(command, shell=True, check=True).returncode
    else:
        exit_code = subprocess.run(command, check=True).returncode
    if exit_code != 0:
        print(f"Command failed with exit code {exit_code}: {command}")
        sys.exit(exit_code)


def check_git(branch: str):
    print("--- CHECK GIT ----------------------------------------------------")
    system("git diff --exit-code")
    system("git diff --cached --exit-code")

    system("git fetch origin")
    behind = int(
        subprocess.check_output(
            ["git", "rev-list", "--count", f"{branch}..origin/{branch}"]
        )
    )
    if behind > 0:
        print(f"{branch} is {behind} commit(s) behind origin/{branch}")
        sys.exit(1)


def test():
    print("--- TEST ---------------------------------------------------------")
    system("make test")


def _update_changelog(modifier_callback: str):
    # line = f"{tagname} ({datetime.now().strftime('%Y-%m-%d')})"
    with open("CHANGELOG.rst", "r") as changelog_file:
        changelog = changelog_file.read()
    changelog = modifier_callback(changelog)
    with open("CHANGELOG.rst", "w") as changelog_file:
        changelog_file.write(changelog)


def update_changelog(tagname: str):
    print("--- UPDATING CHANGELOG ----------------------------------------------")
    # include today's date in format yyyy-mm-dd
    # to match format v0.13.2 (2023-12-04)
    line = f"{tagname} ({datetime.now().strftime('%Y-%m-%d')})"

    def modifier(changelog: str) -> str:
        return changelog.replace(UN_RELEASED, line + "\n" + "-" * len(line))

    _update_changelog(modifier)


def check_docs():
    print("--- CHECK DOCS ---------------------------------------------------")
    system("make docs")


def _get_current_version(must_be_dev=True) -> str:
    """the dev version is always latest version + patch + dev
    eg: last published version 0.13.2 so dev is 0.13.3.dev0
    """
    version = (
        subprocess.check_output(["uv", "version"])
        .decode("utf-8")
        .replace("'", "")
        .strip()
    )
    # berserk 0.13.3.dev0
    assert "berserk" in version
    if must_be_dev:
        assert "dev" in version
    return version.split()[1].partition(".dev")[0]


def _decrement_patch(version: str) -> str:
    print(f"Decrementing patch version of {version}")
    major, minor, patch = [int(x) for x in version.split(".")]
    assert patch > 0
    return f"{major}.{minor}.{patch - 1}"


# major: Increase the major version (e.g., 1.2.3 => 2.0.0)
# minor: Increase the minor version (e.g., 1.2.3 => 1.3.0)
# patch: Increase the patch version (e.g., 1.2.3 => 1.2.4)
# stable: Move from a pre-release to stable version (e.g., 1.2.3b4.post5.dev6 => 1.2.3)
# alpha: Increase the alpha version (e.g., 1.2.3a4 => 1.2.3a5)
# beta: Increase the beta version (e.g., 1.2.3b4 => 1.2.3b5)
# rc: Increase the rc version (e.g., 1.2.3rc4 => 1.2.3rc5)
# post: Increase the post version (e.g., 1.2.3.post5 => 1.2.3.post6)
# dev: Increase the dev version (e.g., 1.2.3a4.dev6 => 1.2.3.dev7)
def bump_version(bump: Literal["major", "minor", "patch"]) -> str:
    last_published_version = _decrement_patch(_get_current_version())
    system(f"uv version {last_published_version}")
    system(f"uv version --bump {bump}")
    new_version = _get_current_version(must_be_dev=False)
    print(f"Bumped version: {last_published_version} -> {new_version}")
    tagname = f"v{new_version}"
    return tagname


def get_changelog_section() -> str:
    version_regex = r"v\d+\.\d+\."
    changelog_regex = f"({version_regex}" + r"[\s\S]*?)" + version_regex

    with open("CHANGELOG.rst", "r") as changelog_file:
        content = changelog_file.read()
    return re.search(changelog_regex, content).group(1)


def tag_and_push(tagname: str, branch: str, changelog_section: str):
    print("--- TAG AND PUSH -------------------------------------------------")
    release_filename = f"release-{tagname}.txt"
    with open(release_filename, "w") as release_txt:
        release_txt.write(changelog_section)

    print(f"tagname = {tagname}, ctrl+C to abort, sleeping 5 seconds...")
    time.sleep(5)

    system("git add -u")
    system(["git", "commit", "-m", f"releasing {tagname}\n\n{changelog_section}"])
    # TODO signed commit
    if branch == "master":
        system(f"git tag {tagname} -F {release_filename}")
        system(f"git push --atomic origin {branch} {tagname}")


def go_to_dev(branch: str):
    print("--- GO TO DEV ----------------------------------------------------")
    system("uv version --bump patch")
    version = _get_current_version(must_be_dev=False)
    dev_version = f"{version}.dev0"
    system(f"uv version {dev_version}")

    def modifier(changelog: str) -> str:
        title = "========="
        return changelog.replace(title, f"{title}\n\n{UN_RELEASED}\n\n")

    _update_changelog(modifier)
    system("git add -u")
    system(f'git commit -m "Bump to dev version: {dev_version}"')
    system(f"git push origin {branch}")


def build():
    print("--- build ---------------------------------------------------------")
    system("make build")


# def github_release(tagname):
#     print("--- GITHUB RELEASE -----------------------------------------------")
#     print(f"https://github.com/niklasf/python-chess/releases/new?tag={tagname}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bump",
        choices=["major", "minor", "patch", "none"],
        required=True,
        help="type of version bump; use 'none' to build current version without bumping or releasing",
    )
    parser.add_argument(
        "--branch",
        choices=["testpypi", "master"],
        required=True,
        help="which branch to push to",
    )
    args = parser.parse_args()
    check_docs()
    test()
    check_git(args.branch)
    if args.bump != "none":
        tagname = bump_version(args.bump)
        update_changelog(tagname)
        # RUN AFTER UPDATING CHANGELOG
        changelog_section = get_changelog_section()
        tag_and_push(tagname, args.branch, changelog_section)
    build()
    if args.bump != "none":
        go_to_dev(args.branch)
