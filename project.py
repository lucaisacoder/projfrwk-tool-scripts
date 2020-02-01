#!/usr/bin/env python
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
    PRT.info("SDK_PATH", sdk_path)
    PRT.info("PROJECT", project_name)
    PRT.info("PROJECT_PATH", project_path)
    project_cmake_file = project_path + "/CMakeLists.txt"
    PRT.debug("PROJECT_CMAKE_FILE", project_cmake_file)

    # args parser
    project_parser = argparse.ArgumentParser(description='project args parser', prog="project.py")
    #project_parser.add_argument('--toolchain', help='toolchain absolute path', metavar='PATH', default="")
    #project_parser.add_argument('--toolchain-prefix', help='toolchain prefix', metavar='PREFIX', default="")
    #project_parser.add_argument('--config', help='config file path', metavar='PATH', default="{}/config.mk".format(project_path))
    project_parser.add_argument('--verbose', help='debug build command, `make VERBOSE=1`', action="store_true", default=False)
    project_parser.add_argument("cmd", help='command list', choices=["config", "build", "rebuild", "menuconfig", "clean", "distclean", "clean_conf", "unit_test", "install", "uninstall"])
    project_args = project_parser.parse_args()

    cmder = ClassCmd(sdk_path, project_path, "Unix Makefiles", project_args.verbose)
    # build
    if project_args.cmd == "build":
        cmder.build()
    else:
        cmder.unknown()
        exit(1)