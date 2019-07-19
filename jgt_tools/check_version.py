"""Ensure version bump."""
import subprocess
import os

import github3


MISSING_VERSION_BUMP_MSG = "Code files changed with no corresponding version bump!"


def _any_py_files_changed(file_names):
    return any(file_name.endswith(".py") for file_name in file_names)


def _version_changed(pyproject_diff):
    return "+version = " in pyproject_diff


def travis_check_version():
    """Verify the version is changed if any code files are changed."""

    token = os.getenv("GH_TOKEN")
    if not token:
        raise ValueError('No "GH_TOKEN" value found in environment!')
    gh = github3.login(token=token)
    org, repo = os.getenv("TRAVIS_REPO_SLUG").split("/")
    issue_id = os.getenv("TRAVIS_PULL_REQUEST")
    pr = gh.issue(org, repo, issue_id).pull_request()

    files = [(f.name, f.patch) for f in pr.files()]

    pyproject_diff = [f.patch for f in files if f.name == "pyproject.toml"]
    pyproject_diff = pyproject_diff[0] if pyproject_diff else ""

    if _any_py_files_changed([f.name for f in files]) and not _version_changed(
        pyproject_diff
    ):
        print(MISSING_VERSION_BUMP_MSG)
        exit(1)


def local_check_version():
    """Verify the version is changed if any code files are changed."""
    changed_files = subprocess.check_output(
        ["git", "diff", "master", "--name-only"], universal_newlines=True
    ).splitlines()

    pyproject_diff = subprocess.check_output(
        ["git", "diff", "master", "pyproject.toml"], universal_newlines=True
    )

    if _any_py_files_changed(changed_files) and not _version_changed(pyproject_diff):
        print(MISSING_VERSION_BUMP_MSG)
        exit(1)


def check_version():
    """Determine Travis or local check, then run."""
    if os.getenv("TRAVIS_PULL_REQUEST"):
        return travis_check_version()
    return local_check_version()
