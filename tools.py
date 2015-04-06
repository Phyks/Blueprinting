#!/usr/bin/env python3
import os


def list_directory(path, filter=lambda x: True):
    """
    List all files in path directory. Works recursively

    Filter is an optional callback. If set, the found items will be appended
    to the returned list only if filter evaluated on them is True.

    Return a list of files with path relative to path parent dir.
    """
    files_list = []
    for root, dirs, files in os.walk(path):
        for i in files:
            file = os.path.join(root, i)
            if filter(file):
                files_list.append(file)
    return files_list
