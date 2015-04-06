#!/usr/bin/env python3
import pacman


if __name__ == "__main__":
    packages = pacman.list_installed_packages()
    aur_packages = pacman.list_installed_aur_packages()
    modified_config_files = pacman.list_modified_config_files()
    new_config_files = pacman.list_new_config_files()
