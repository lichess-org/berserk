#!/usr/bin/python3
# Helper script to create and publish a new `berserk` release.
# Based on `release.py` from `python-chess`.

import argparse
import os
import sys
import subprocess

from typing import Literal
from datetime import datetime


def system(command):
    print(command)
    exit_code = os.system(command)
    if exit_code != 0:
        sys.exit(exit_code)


def check_git():
    print("--- CHECK GIT ----------------------------------------------------")
    system("git diff --exit-code")
    system("git diff --cached --exit-code")

    system("git fetch origin")
    behind = int(
        subprocess.check_output(["git", "rev-list", "--count", "master..origin/master"])
    )
    if behind > 0:
        print(f"master is {behind} commit(s) behind origin/master")
        sys.exit(1)


def test():
    print("--- TEST ---------------------------------------------------------")
    system("make test")


def update_changelog(tagname: str):
    print("--- UPDATING CHANGELOG ----------------------------------------------")
    # include today's date in format yyyy-mm-dd
    # to match format v0.13.2 (2023-12-04)
    line = f"{tagname} ({datetime.now().strftime('%Y-%m-%d')})"
    unreleased = "To be released\n--------------"
    with open("CHANGELOG.rst", "r") as changelog_file:
        changelog = changelog_file.read()
    changelog = changelog.replace(unreleased, line + "\n" + "-" * len(line))
    with open("CHANGELOG.rst", "w") as changelog_file:
        changelog_file.write(changelog)


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


def tag_and_push(tagname: str):
    print("--- TAG AND PUSH -------------------------------------------------")
    release_filename = f"release-{tagname}.txt"

    if not os.path.exists(release_filename):
        print(f">>> Creating {release_filename} ...")
        first_section = False
        prev_line = None
        with open(release_filename, "w") as release_txt, open(
            "CHANGELOG.rst", "r"
        ) as changelog_file:
            headline = f"berserk {tagname}"
            release_txt.write(headline + os.linesep)

            for line in changelog_file:
                if not first_section:
                    if line.startswith("-------"):
                        first_section = True
                else:
                    if line.startswith("-------"):
                        break
                    else:
                        if not prev_line.startswith("------"):
                            release_txt.write(prev_line)

                prev_line = line

    with open(release_filename, "r") as release_txt:
        release = release_txt.read().strip() + os.linesep
        print(release)

    with open(release_filename, "w") as release_txt:
        release_txt.write(release)

    guessed_tagname = input(">>> Sure? Confirm tagname: ")
    if guessed_tagname != tagname:
        print(f"Actual tagname is: {tagname}")
        sys.exit(1)

    system(f"git tag {tagname} -s -F {release_filename}")
    system(f"git push --atomic origin master {tagname}")
    return tagname


def go_to_dev():
    print("--- GO TO DEV ----------------------------------------------------")
    system("uv version --bump patch")
    version = _get_current_version(must_be_dev=False)
    system(f"uv version {version}dev")
    system("git add -u")
    system('git commit -m "Bump to next development version"')
    system("git push origin master")


def build():
    print("--- build ---------------------------------------------------------")
    system("make build")


# def github_release(tagname):
#     print("--- GITHUB RELEASE -----------------------------------------------")
#     print(f"https://github.com/niklasf/python-chess/releases/new?tag={tagname}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "bump",
        choices=["major", "minor", "patch"],
        help="type of version bump",
    )
    args = parser.parse_args()
    check_docs()
    test()
    check_git()
    tagname = bump_version(args.bump)
    update_changelog(tagname)
    tag_and_push(tagname)
    while is_done := input("now release to pypi with: make publish, done when done"):
        if is_done.lower() in ["y", "yes", "done"]:
            build()
            break
    go_to_dev()
