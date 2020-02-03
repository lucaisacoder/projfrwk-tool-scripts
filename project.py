#!/usr/bin/env python3
#-*- coding = utf-8 -*-

import argparse
import os, sys, re
from pyscripts.ClassPrint import *
from pyscripts.ClassCmd import *
from pathlib import * # only Python3 supports

PRT = ClassPrint()

def project_process(project_sdk_path, project_name, project_path, project_cmake_file):
    # project info
    PRT.info("SDK_PATH", project_sdk_path)
    PRT.info("PROJECT", project_name)
    PRT.info("PROJECT_PATH", project_path)
    PRT.info("PROJECT_CMAKE_FILE", project_cmake_file)

    # args parser
    project_parser = argparse.ArgumentParser(description='project args parser', prog="project.py")
    #project_parser.add_argument('--toolchain', help='toolchain absolute path', metavar='PATH', default="")
    #project_parser.add_argument('--toolchain-prefix', help='toolchain prefix', metavar='PREFIX', default="")
    #project_parser.add_argument('--config', help='config file path', metavar='PATH', default="{}/config.mk".format(project_path))
    project_parser.add_argument('--install', help='config install path', metavar='PATH', default="installed")
    project_parser.add_argument('--verbose', help='debug build command, `make VERBOSE=1`', action="store_true", default=False)
    project_parser.add_argument("cmd", help='command list', choices=[   "build", "install", "uninstall", "clean", "distclean", "build_all", "menuconfig",
                                                                        "config", "rebuild", "clean_conf"])
    project_args = project_parser.parse_args()

    cmder = ClassCmd(project_sdk_path, project_path, project_args.install, "Unix Makefiles", project_args.verbose)
    # build
    if project_args.cmd == "build":
        cmder.build()
    elif project_args.cmd == "install":
        cmder.install()
    elif project_args.cmd == "uninstall":
        cmder.uninstall()
    elif project_args.cmd == "clean":
        cmder.clean()
    elif project_args.cmd == "distclean":
        cmder.distclean()    
    elif project_args.cmd == "build_all":
        cmder.build()
        cmder.install()
    elif project_args.cmd == "menuconfig":
        cmder.menuconfig()
    elif project_args.cmd == "menuconfig_all":
        cmder.menuconfig()
    else:
        cmder.unknown(project_args.cmd)
        exit(1)

def check_scripts_path():
    _cur_path = Path(".").resolve()
    return _cur_path.match("scripts")

def get_sdk_path():
    return Path.cwd().parent.parent

ALL_PROJECT_PATH = ["components", "core"]

if __name__ == '__main__':
    if check_scripts_path() is True:
        _project_sdk_path = get_sdk_path()
        for dir in ALL_PROJECT_PATH:
            _path = _project_sdk_path / dir
            for item in _path.iterdir():
                if item.is_dir() is True:
                    _project_name = item.name
                    _project_path = item
                    _project_cmake_file = item / "CMakeLists.txt"
                    project_process(_project_sdk_path, _project_name, _project_path, _project_cmake_file)
    else:
        # check files
        files = ["CMakeLists.txt", "Kconfig"]
        for item in files:
            if not os.path.exists(item): 
                PRT.NoSuchFile(item)
                exit(1)
        project_process(project.sdk_path(), project.name(), project.path(), project.cmake_file())

    