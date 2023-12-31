# Obsidian Daily Commit Log

[Git hook](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks) that logs git commits into daily [obsidian](https://obsidian.md/) note automatically.

![image](https://github.com/mile95/obsidian-daily-commit-log/assets/8545435/b3427ffe-2226-4423-b6a2-cb03ad215953)

## Installation

	./installation.sh

## Setup

1. Set the `OBSIDIAN_VAULT_PATH` env variable in to the full vault path
1. set the `OBSIDIAN_DAILY_NOTE_BASE_PATH` env variable to the relative daily notes folder. For instance `/daily`. Leave empty if daily notes exist in the root.
1. set the `OBSIDIAN_DAILY_NOTE_TEMPLATE_PATH` env variable to the relative path for the daily template file. For instance `/templates/daily`.
1. Make sure the daily note has a section starting with: `## Commits`
1. Make sure the daily note follows `YYYY-MM-DD` format
