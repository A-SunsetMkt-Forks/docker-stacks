#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import json
import os
from pathlib import Path
from typing import Any

THIS_DIR = Path(__file__).parent.resolve()
REPOSITORY_OWNER = os.environ["REPOSITORY_OWNER"]


def generate_matrix() -> dict[str, Any]:
    dockerfiles = sorted(file.name for file in THIS_DIR.glob("*.dockerfile"))
    runs_on = ["ubuntu-24.04", "ubuntu-22.04-arm"]
    return {
        "dockerfile": dockerfiles,
        "runs-on": runs_on,
        "exclude": [
            {"dockerfile": "oracledb.dockerfile", "runs-on": "ubuntu-22.04-arm"}
        ],
    }


if __name__ == "__main__":
    print("matrix=" + json.dumps(generate_matrix()))
