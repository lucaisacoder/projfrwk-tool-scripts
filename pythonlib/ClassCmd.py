#!/usr/bin/env python
#-*- coding = utf-8 -*-
import os, subprocess, shutil, time
from multiprocessing import cpu_count
from pythonlib.ClassPrint import *

PRT = ClassPrint()
COMPILE_TYPES = ["Unix Makefiles",""]

class ClassCmd:

    cmd_sdk_path = ""
    cmd_project_path = ""
    cmd_compile_type = ""
    cmd_verbose = False
    cmd_build_path = ""
    def __init__(self, sdk_path, project_path, compile_type, verbose):
        self.cmd_sdk_path = sdk_path
        self.cmd_project_path = project_path
        self.cmd_compile_type = compile_type
        self.cmd_verbose = verbose

        self.cmd_build_path = self.cmd_project_path + "/build"

        PRT.debug("sdk_path", self.cmd_sdk_path)
        PRT.debug("project_path", self.cmd_project_path)
        PRT.debug("compile_type", self.cmd_compile_type)
        PRT.debug("verbose", self.cmd_verbose)
        
        if self.cmd_compile_type not in COMPILE_TYPES:
            PRT.error("no compile type found - %s." % (self.cmd_compile_type))
            exit(1)


    def build(self):
        PRT.Start("build!")
        time_start = time.time()

        if not os.path.exists(self.cmd_build_path):
            os.mkdir(self.cmd_build_path)
            PRT.Complete("Build %s" % self.cmd_build_path)
        else:
            PRT.info("Existed", self.cmd_build_path)
        os.chdir(self.cmd_build_path)
        PRT.Process("Enter into: %s" % self.cmd_build_path)

        if not os.path.exists("Makefile"):
            res = subprocess.call(["cmake", "-G", self.cmd_compile_type, ".."])
            if res != 0:
                exit(1)
        if self.cmd_verbose:
                res = subprocess.call(["make", "VERBOSE=1"])
        else:
            res = subprocess.call(["make", "-j{}".format(cpu_count())])
        if res != 0:
            exit(1)

        time_end = time.time()
        PRT.TimeLast(time_start, time_end)
        PRT.Complete("build!")

    def unknown(self):
        PRT.error("unknown cmd.")