Blueprinting
============

This is a basic blueprinting script for Arch Linux. It aims at listing all installed packages, all installed AUR packages and list modifications done in config files (both for config files provided by Arch packages, and for newly created config files).

Hence, it aims at helping you write Ansible scripts quickly from an already running machine.


This script is mostly inspired by [Devstructure's blueprint](https://github.com/devstructure/blueprint).


## Usage

`pacman.py` is to be considered as a wrapper around useful pacman commands to extract informations on installed packages, installed AUR packages, configuration files etc.

`blueprinting.py` is the main entry point. For now, it just calls main entry points of `pacman.py` to get useful information on your system, so you should refer to the code in `blueprinting.py` and edit it to do something useful with the returns from these functions. But this script is a Work In Progress and a user interface is planned.


## License

All the source code I wrote is under a `no-alcohol beer-ware license`.
```
* --------------------------------------------------------------------------------
* "THE NO-ALCOHOL BEER-WARE LICENSE" (Revision 42):
* Phyks (webmaster@phyks.me) wrote this file. As long as you retain this notice you
* can do whatever you want with this stuff (and you can also do whatever you want
* with this stuff without retaining it, but that's not cool...). If we meet some
* day, and you think this stuff is worth it, you can buy me a <del>beer</del> soda
* in return.
*																		Phyks
* ---------------------------------------------------------------------------------
```
