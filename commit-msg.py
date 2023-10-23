#!/usr/bin/env python3

import sys
import os
import subprocess
import datetime
import shutil
from pathlib import Path

OBSIDIAN_VAULT_PATH = "~/Documents/bank"
OBSIDIAN_DAILY_NOTE_BASE_PATH = "/daily"
OBSIDIAN_DAILY_NOTE_TEMPLATE_PATH = "/templates/daily"


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
    if "~" in OBSIDIAN_VAULT_PATH:
        return f"{os.path.expanduser(OBSIDIAN_VAULT_PATH)}{OBSIDIAN_DAILY_NOTE_BASE_PATH}/{current_date}.md"
    return f"{OBSIDIAN_VAULT_PATH}{OBSIDIAN_DAILY_NOTE_BASE_PATH}/{current_date}.md"


def create_daily_if_missing(daily_file: str) -> None:
    potential_file = Path(daily_file_path)
    if not potential_file.is_file():
        print("No file found")
        template_file = ""
        if "~" in OBSIDIAN_VAULT_PATH:
            template_file = f"{os.path.expanduser(OBSIDIAN_VAULT_PATH)}{OBSIDIAN_DAILY_NOTE_TEMPLATE_PATH}.md"
        else:
            template_file = (
                f"{OBSIDIAN_VAULT_PATH}{OBSIDIAN_DAILY_NOTE_TEMPLATE_PATH}.md"
            )
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


commit_msg = get_commit_msg()
repo = get_repo_name()
daily_file_path = get_daily_file()
create_daily_if_missing(daily_file_path)

log_commit_to_daily_note(commit_msg, repo, daily_file_path)
