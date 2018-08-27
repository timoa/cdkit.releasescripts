#!/usr/bin/env python
"""Generate release notes

USAGE:
./releaseNotes.py

"""
import os
import sys
import subprocess

__author__ = "Damien Laureaux"
__email__ = "dev@timoa.com"


def create_file(filename):
    """ Create a file with write rights and UTF-8 encoding

    Args:
        param1 (string): Filename
    Returns:
        Return a file object
    """
    return open(filename, mode="w", encoding="utf-8")


# Retrieve last commit hash and save to text file
LAST_COMMIT = create_file("last_commit.txt")
GIT_LAST_COMMIT = subprocess.Popen(
    ["git", "rev-parse", "--short", "HEAD"], stdout=LAST_COMMIT)

# Generate release notes
if "GO_PIPELINE_NAME" in os.environ:
    CURRENT = "Build/" + os.environ["GO_PIPELINE_NAME"] + "/current"

    # Create release_notes.txt
    RELEASE_NOTE = create_file("release_notes.txt")

    print("Generate release notes (" + CURRENT + ")")

    # retrieve commit messages and save to text file
    GIT_LOGS = subprocess.Popen(["git", "log", CURRENT + "..HEAD",
                                 "--pretty=format:\"- %s\"", "--no-merges"],
                                stdout=subprocess.PIPE)

    # filter out non-User Stories related commits (NOUS = NO User Stories)
    FILTER_LOGS = subprocess.Popen(
        ["grep", "-i", "'US[0-9]\{5\}\|DE[0-9]\{5\}\|TA[0-9]\{5\}\|NOUS'"],
        stdin=GIT_LOGS.stdout,
        stdout=RELEASE_NOTE)

    # Close release_notes.txt
    RELEASE_NOTE.close()

else:
    sys.exit("Missing environment variable: GO_PIPELINE_NAME")

sys.exit()
