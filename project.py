#!/usr/bin/env python
#-*- coding = utf-8 -*-

import argparse
import os, sys, re
from multiprocessing import cpu_count
from ClassPrint import *
from ClassConfig import *


if __name__ == "__main__":
    if not os.path.exists("CMakeLists.txt") or not os.path.exists("code"):
        print("please run me at project folder!")
        exit(1)

    try:
        sdk_path = sdk_path
    except Exception:
        sdk_path = os.path.abspath("../../")
    project_path = sys.path[0]
    project_name = ""
    project_cmake_path = project_path+"/CMakeLists.txt"
    project_cmake_content = ""
    with open(project_cmake_path) as f:
        project_cmake_content = f.read()
    match = re.findall(r"{}(.*){}".format(r"project\(", r"\)"), project_cmake_content, re.MULTILINE|re.DOTALL)
    if len(match) != 0:
        project_name = match[0]
        print(project_name)
    if project_name == "":
        print("[ERROR] Can not find project name in {}".format(project_cmake_path))
        exit(1)


    project_parser = argparse.ArgumentParser(description='cmder', prog="project.py")

    project_parser.add_argument('--toolchain', help='toolchain absolute path', metavar='PATH', default="")
    project_parser.add_argument('--toolchain-prefix', help='toolchain prefix', metavar='PREFIX', default="")
    project_parser.add_argument('--config', help='config file path', metavar='PATH', default="{}/config.mk".format(project_path))
    project_parser.add_argument('--verbose', help='debug build command, `make VERBOSE=1`', action="store_true", default=False)
    project_parser.add_argument("cmd", help='command list', choices=["config", "build", "rebuild", "menuconfig", "clean", "distclean", "clean_conf"])

    project_args = project_parser.parse_args()

    config_filename = ".config.mk"
    build_path = sys.path[0]
    print("0000000 %s"%build_path)
    project_type = "Unix Makefiles"
    config = ClassConfig(build_path, config_filename, project_args.toolchain, project_args.toolchain_prefix)
    config.update_config()

    cmd = ClassCmd(sdk_path, project_type, build_path, config_filename, project_args.verbose)
    # config
    if project_args.cmd == "config":
        cmd.config()
    # build
    elif project_args.cmd == "build":
        cmd.build()
    # rebuild
    elif project_args.cmd == "rebuild":
        cmd.rebuild()
    # clean
    elif project_args.cmd == "clean":
        cmd.clean()
    # distclean    
    elif project_args.cmd == "distclean":
        cmd.distclean()
    # menuconfig
    elif project_args.cmd == "menuconfig":
        cmd.menuconfig()
    # clean_conf
    elif project_args.cmd == "clean_conf":
        cmd.clean_conf()
    else:
        cmd.unknown()
        exit(1)

