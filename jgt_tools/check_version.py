"""Ensure version bump."""
import subprocess


def _any_py_files_changed(file_names):
    return any(file_name.endswith(".py") for file_name in file_names)


def _version_changed(pyproject_diff):
    return "+version = " in pyproject_diff


def check_version():
    """Verify the version is changed if any code files are changed."""
    changed_files = subprocess.check_output(
        ["git", "diff", "master", "--name-only"], universal_newlines=True
    ).splitlines()

    pyproject_diff = subprocess.check_output(
        ["git", "diff", "master", "pyproject.toml"], universal_newlines=True
    )

    if _any_py_files_changed(changed_files) and not _version_changed(pyproject_diff):
        print("Code files changed with no corresponding version bump!")
        exit(1)
