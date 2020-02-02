#!/usr/bin/env python3
#-*- coding = utf-8 -*-

import argparse
import os, sys, re
from pythonlib.ClassPrint import *
from pythonlib.ClassCmd import *

if __name__ == '__main__':
    PRT = ClassPrint()

    # check files
    files = ["CMakeLists.txt", "Kconfig"]
    for item in files:
        if not os.path.exists(item): 
            PRT.NoSuchFile(item)
            exit(1)
    
    # project info
    PRT.info("SDK_PATH", project.sdk_path())
    PRT.info("PROJECT", project.name())
    PRT.info("PROJECT_PATH", project.path())
    PRT.info("PROJECT_CMAKE_FILE", project.cmake_file())

    # args parser
    project_parser = argparse.ArgumentParser(description='project args parser', prog="project.py")
    #project_parser.add_argument('--toolchain', help='toolchain absolute path', metavar='PATH', default="")
    #project_parser.add_argument('--toolchain-prefix', help='toolchain prefix', metavar='PREFIX', default="")
    #project_parser.add_argument('--config', help='config file path', metavar='PATH', default="{}/config.mk".format(project_path))
    project_parser.add_argument('--install', help='config install path', metavar='PATH', default="installed")
    project_parser.add_argument('--verbose', help='debug build command, `make VERBOSE=1`', action="store_true", default=False)
    project_parser.add_argument("cmd", help='command list', choices=["build", "install", "uninstall", "clean", "distclean", "config", "rebuild", "menuconfig", "clean_conf"])
    project_args = project_parser.parse_args()

    cmder = ClassCmd(project.sdk_path(), project.path(), project_args.install, "Unix Makefiles", project_args.verbose)
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
    else:
        cmder.unknown(project_args.cmd)
        exit(1)