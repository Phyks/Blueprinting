#!/usr/bin/env python3
import pacman


if __name__ == "__main__":
    # Packages is a list of installed packages (or groups if all packages of a
    # group have been installed)
    packages = pacman.list_installed_packages()

    # Aur_packages is a list of all packages installed through AUR
    aur_packages = pacman.list_installed_aur_packages()

    # Modified config_files is a list of all the modified configuration files,
    # compared to packages base config
    modified_config_files = pacman.list_modified_config_files()

    # New config files is a list of all the files under /etc which are not
    # coming from any package.
    # Will list a bunch of files. Files under /etc/ssl/certs and /etc/certs can
    # be ignored.
    # Will ignore binary files under /etc by default
    new_config_files = pacman.list_new_config_files()
