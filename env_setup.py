#!/usr/bin/env python3
"""Bootstrap the environment setup."""
try:
    import jgt_tools.env_setup

    jgt_tools.env_setup.main()
except ModuleNotFoundError:
    import subprocess

    # if jgt_tools is not importable, one of two things has happened:
    # either you are inside a "naked" virtualenv,
    # or you are not inside the virutalenv at all.
    # Installing and calling `env-setup` via subcommand and `poetry run`
    # will ensure the "right thing" happens in either situation.
    proc = subprocess.run(["poetry", "version"], stdout=subprocess.PIPE)
    package_name = "." if proc.stdout.split()[0] == b"jgt-tools" else "jgt_tools"
    subprocess.check_call(["poetry", "run", "pip", "install", package_name])
    subprocess.check_call(["poetry", "run", "env-setup"])
