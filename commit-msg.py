#!/usr/bin/env python3

import sys
import os
import subprocess
import datetime
import shutil
from pathlib import Path


def verify_config() -> None:
    for key in [
        "OBSIDIAN_VAULT_PATH",
        "OBSIDIAN_DAILY_NOTE_BASE_PATH",
        "OBSIDIAN_DAILY_NOTE_TEMPLATE_PATH",
    ]:
        try:
            os.environ[key]
        except KeyError:
            print(f"Error: Environment Variable {key} not set")
            sys.exit(1)


def get_commit_msg() -> str:
    commit_msg_file = sys.argv[1]
    msg = ""
    with open(commit_msg_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("#"):
                break
            msg += line
        return msg.replace("\n", " ")


def get_repo_name() -> str:
    repo_dir = (
        subprocess.Popen(
            ["git", "rev-parse", "--show-toplevel"], stdout=subprocess.PIPE
        )
        .communicate()[0]
        .rstrip()
        .decode("utf-8")
    )

    return repo_dir.split("/")[-1]


def get_daily_file() -> str:
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    if "~" in os.environ["OBSIDIAN_VAULT_PATH"]:
        return f"{os.path.expanduser(os.environ['OBSIDIAN_VAULT_PATH'])}{os.environ['OBSIDIAN_DAILY_NOTE_BASE_PATH']}/{current_date}.md"
    return f"{os.environ['OBSIDIAN_VAULT_PATH']}{os.environ['OBSIDIAN_DAILY_NOTE_BASE_PATH']}/{current_date}.md"


def create_daily_if_missing(daily_file: str) -> None:
    potential_file = Path(daily_file)
    if not potential_file.is_file():
        template_file = ""
        if "~" in os.environ["OBSIDIAN_VAULT_PATH"]:
            template_file = f"{os.path.expanduser(os.environ['OBSIDIAN_VAULT_PATH'])}{os.environ['OBSIDIAN_DAILY_NOTE_TEMPLATE_PATH']}.md"
        else:
            template_file = f"{os.environ['OBSIDIAN_VAULT_PATH']}{os.environ['OBSIDIAN_DAILY_NOTE_TEMPLATE_PATH']}.md"
        shutil.copyfile(template_file, daily_file)


def log_commit_to_daily_note(commit_msg: str, repo: str, daily_file_path: str) -> None:
    with open(daily_file_path, "r") as file:
        lines = file.readlines()

    commit_section_index = None
    for i, line in enumerate(lines):
        if line.strip() == "## Commits":
            commit_section_index = i
            break

    if commit_section_index is None:
        raise Exception("No ## Commits section in the daily note")

    now = datetime.datetime.now().strftime("%H:%M:%S")
    commit_log = f"-  `{commit_msg}` **in** `{repo}` **at** {now} \n"
    lines.insert(commit_section_index + 1, commit_log)

    with open(daily_file_path, "w") as file:
        file.writelines(lines)


def main() -> int:
    verify_config()
    commit_msg = get_commit_msg()
    repo = get_repo_name()
    daily_file_path = get_daily_file()
    create_daily_if_missing(daily_file_path)

    log_commit_to_daily_note(commit_msg, repo, daily_file_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
