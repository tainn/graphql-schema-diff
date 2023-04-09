#!/usr/bin/env python3

import difflib
import os
import subprocess
import sys
import time
from logging import Logger, getLogger
from pathlib import Path

from cordhook import Form

import logutil


def main() -> None:
    if not Path("/data/latest-version.txt").is_file():
        initilize_data()
        return

    latest_version: int = int(Path("/data/latest-version.txt").read_text())

    prev_graphql_schema: str = Path(f"/data/schema-v{latest_version}.graphql").read_text()
    new_graphql_schema: str = subprocess.run(
        f"get-graphql-schema {os.getenv('GSD_ENDPOINT')}",
        shell=True,
        capture_output=True,
        text=True,
    ).stdout

    prev_json_schema: str = Path(f"/data/schema-v{latest_version}.json").read_text()
    new_json_schema: str = subprocess.run(
        f"get-graphql-schema {os.getenv('GSD_ENDPOINT')} --json",
        shell=True,
        capture_output=True,
        text=True,
    ).stdout

    graphql_diff_build: str = ""
    json_diff_build: str = ""

    for diff in difflib.unified_diff(prev_graphql_schema.splitlines(), new_graphql_schema.splitlines()):
        graphql_diff_build += f"{diff}\n" if diff else ""

    if not graphql_diff_build:
        logger.debug(f"No diffs found, sleeping for {os.getenv('GSD_PULL_INTERVAL')} seconds")
        return

    for diff in difflib.unified_diff(prev_json_schema.splitlines(), new_json_schema.splitlines()):
        json_diff_build += f"{diff}\n" if diff else ""

    Path(f"/data/schema-v{latest_version + 1}.graphql").write_text(new_graphql_schema)
    Path(f"/data/schema-v{latest_version + 1}.json").write_text(new_json_schema)
    Path(f"/data/graphql-diff-v{latest_version + 1}.txt").write_text(graphql_diff_build)
    Path(f"/data/json-diff-v{latest_version + 1}.txt").write_text(json_diff_build)
    Path(f"/data/latest-version.txt").write_text(str(latest_version + 1))

    if os.getenv("GSD_DISCORD_WEBHOOK"):
        discord_webhook(latest_version + 1)


def initilize_data() -> None:
    Path("/data").mkdir(exist_ok=True, parents=True)
    Path("/data/latest-version.txt").write_text("1")

    subprocess.run(f"get-graphql-schema {os.getenv('GSD_ENDPOINT')} > /data/schema-v1.graphql", shell=True)
    subprocess.run(f"get-graphql-schema {os.getenv('GSD_ENDPOINT')} --json > /data/schema-v1.json", shell=True)


def discord_webhook(version: int) -> None:
    form: Form = Form()

    form.embed_color(0000000)
    form.embed_title(f"GSD")
    form.embed_description(f"New GraphQL API version change detected: **v{version}**")
    form.embed_footer(text="graphql-schema-diff")

    form.post(os.getenv("GSD_DISCORD_WEBHOOK"))


if __name__ == "__main__":
    logutil.configure()
    logger: Logger = getLogger(__name__)

    try:
        while True:
            main()
            time.sleep(int(os.getenv("GSD_PULL_INTERVAL")))
    except Exception as e:
        logger.error(f"Global exception caught: {e}")
        sys.exit(1)
