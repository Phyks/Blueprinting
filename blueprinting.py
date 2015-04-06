#!/usr/bin/env python3
import pacman


if __name__ == "__main__":
    packages = pacman.list_installed_packages()
    config_files = pacman.list_modified_config_files()
