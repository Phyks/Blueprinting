#!/usr/bin/env python3
import os
import subprocess
import sys

PACKAGE_BASE_PATH = "/var/cache/pacman/pkg/"
ARCH = "x86_64"


def is_installed(package):
    """
    Check whether the specified package is installed or not.
    """
    try:
        subprocess.check_output(["pacman", "-Qs", package])
        return True
    except subprocess.CalledProcessError:
        return False


def get_file_from_package(file):
    """
    Get the specified file from the corresponding package archive from pacman
    cache.

    Returns None and print an error message if unable to find the archive in the
    pacman cache.
    """
    # /var/cache/pacman/pkg/lvm2-2.02.116-1-x86_64.pkg.tar.xz
    # Find the package
    try:
        pacman_raw = subprocess.check_output(["pacman", "-Qo", file])
        pacman_raw = pacman_raw.decode("utf-8").strip()
        package, version = pacman_raw.split(" ")[-2:]
    except subprocess.CalledProcessError:
        print("Unable to find a package owning file " + file + ".",
              file=sys.stderr)
        return None
    # Remove leading / if present
    file = file.lstrip("/")
    # Get the path to the package
    package_archive = package + "-" + version + "-" + ARCH + ".pkg.tar.xz"
    package_path = PACKAGE_BASE_PATH + package_archive
    # Untar the package file
    try:
        raw = subprocess.check_output(["bsdtar", "-xOf", package_path, file],
                                      stderr=open(os.devnull, 'w'))
        raw = raw.decode("utf-8")
    except subprocess.CalledProcessError:
        try:
            package_path = package_path.replace(ARCH, "any")
            raw = subprocess.check_output(["bsdtar", "-xOf", package_path, file],
                                          stderr=open(os.devnull, 'w'))
            raw = raw.decode("utf-8")
        except subprocess.CalledProcessError:
            print("Unable to untar package archive " + package_path + ".",
                file=sys.stderr)
            return None
    return raw


def list_packages_in_group(group):
    """
    List all the packages member of a given group.
    """
    pacman_raw = subprocess.check_output(["pacman", "-Sg", group])
    pacman_raw = pacman_raw.decode("utf-8").strip()
    return [i.split(" ")[1] for i in pacman_raw.split("\n")]



def list_modified_config_files(packages=[]):
    """
    List all the manually modified configuration files.

    packages is an optionnal filtering list of packages. Defaults to [] which
    means "all the packages".

    Returns a dict with modified configuration files as keys and diffs as
    values.
    """
    pacman_raw = subprocess.check_output(["pacman", "-Qii"] + packages)
    pacman_raw = pacman_raw.decode("utf-8").strip()
    modified_list = [i.split("\t")[1]
                     for i in pacman_raw.split("\n")
                     if i.startswith("MODIFIED")]
    modified_files = {}
    for i in modified_list:
        package_file = get_file_from_package(i)
        with open(i, 'r') as fh:
            fs_file = fh.read()
        modified_files[i] = None
    return modified_files


def list_installed_packages():
    """
    List all the installed packages (native, not AUR).

    If a group of packages is completely installed, those packages will be
    replaced by the matching group name.
    """
    # Get a list of all the explicitly installed packages
    pacman_packages_raw = subprocess.check_output(["pacman", "-Qenq"])
    pacman_packages_raw = pacman_packages_raw.decode("utf-8").strip()
    packages_list = pacman_packages_raw.split("\n")
    # Get a list of all the explicitly installed packages, part of a group
    pacman_groups_raw = subprocess.check_output(["pacman", "-Qgenq"])
    pacman_groups_raw = pacman_groups_raw.decode("utf-8").strip()
    # Store the installed packages of each group
    groups_packages = {}
    for i in pacman_groups_raw.split("\n"):
        group, package = i.split(" ")
        if group in groups_packages:
            groups_packages[group] += [package]
        else:
            groups_packages[group] = [package]
    # Check if the whole group has been installed
    for group in groups_packages:
        # List of packages in the group not explicitly installed
        diff = set(list_packages_in_group(group)).difference(
            set(groups_packages[group]))
        # Check that they are installed anyway
        diff_are_all_installed = True
        for package in diff:
            if not is_installed(package):
                diff_are_all_installed = False
                break
        if diff_are_all_installed:
            # If the whole group has been installed, replace its packages in
            # the packages list by itself
            for package in groups_packages[group]:
                try:
                    packages_list.remove(package)
                except ValueError:
                    pass
            packages_list.append(group)
    return packages_list
