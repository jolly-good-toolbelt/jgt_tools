#!/usr/bin/env python3
"""Bootstrap the environment setup."""
try:
    import jgt_tools.env_setup

    jgt_tools.env_setup.main()
except ModuleNotFoundError:
    import subprocess

    subprocess.check_call(["poetry", "install"])
    subprocess.check_call(["poetry", "run", "env-setup"])
