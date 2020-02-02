#!/usr/bin/env python3
#-*- coding = utf-8 -*-

from pathlib import * # only Python3 supports
import os, subprocess, shutil, time
from multiprocessing import cpu_count
from pyscripts.ClassPrint import *
from pyscripts.ClassCompile import *

PRT = ClassPrint()
COMPILE_TYPES = ["Unix Makefiles",""]

class ClassCmd:

    _cmd_sdk_path = ""
    _cmd_project_path = ""
    _cmd_compile_type = ""
    _cmd_verbose = False
    _cmd_build_path = ""
    _cmd_install_path = ""
    
    def __init__(self, sdk_path, project_path, install_path, compile_type, verbose):
        self._cmd_sdk_path = sdk_path
        self._cmd_project_path = project_path
        self._cmd_compile_type = compile_type
        self._cmd_verbose = verbose

        self._cmd_build_path = self._cmd_project_path / "build"
        self._cmd_install_path = self._cmd_project_path / install_path

        PRT.debug("sdk_path", self._cmd_sdk_path)
        PRT.debug("project_path", self._cmd_project_path)
        PRT.debug("compile_type", self._cmd_compile_type)
        PRT.debug("verbose", self._cmd_verbose)
        
        if self._cmd_compile_type not in COMPILE_TYPES:
            PRT.error("no compile type found", self._cmd_compile_type)
            exit(1)


    def build(self):
        PRT.Start("build!")
        time_start = time.time()

        if not self._cmd_build_path.exists():
            os.mkdir(self._cmd_build_path)
            PRT.Complete("Build %s" % self._cmd_build_path)
        else:
            PRT.info("Existed", self._cmd_build_path)
        os.chdir(self._cmd_build_path)
        PRT.Process("Enter into: %s" % self._cmd_build_path)

        if not os.path.exists("Makefile"):
            res = subprocess.call(["cmake", "-G", self._cmd_compile_type, "-DCMAKE_INSTALL_PREFIX={}".format(self._cmd_install_path), ".."])
            if res != 0:
                exit(1)
        if self._cmd_verbose:
                res = subprocess.call(["make", "VERBOSE=1"])
        else:
            res = subprocess.call(["make", "-j{}".format(cpu_count())])
        if res != 0:
            exit(1)

        time_end = time.time()
        PRT.TimeLast(time_start, time_end)
        PRT.Complete("build!")


    def install(self):
        PRT.Start("install!")
        if not self._cmd_build_path.exists():
            PRT.NoPathFound(self._cmd_build_path)
            PRT.info("TIPS", "Pls run 'project.py build' first!")
            exit(1)
        _makefile_path = self._cmd_build_path / "Makefile"
        if not _makefile_path.exists():
            PRT.NoSuchFile(_makefile_path)
            exit(1)
        os.chdir(self._cmd_build_path)
        PRT.Process("Enter into: %s" % self._cmd_build_path)
        res = subprocess.call(["make", "install"])
        if res != 0:
            exit(1)
        PRT.Complete("install!")


    def uninstall(self):
        PRT.Start("uninstall!")
        _cmake_install_cmake = self._cmd_build_path / "Uninstall.cmake"
        if not _cmake_install_cmake.exists():
            PRT.NoPathFound(_cmake_install_cmake)
            PRT.info("TIPS", "Pls run 'project.py install' first!")
            exit(1)
        if not self._cmd_build_path.exists():
            PRT.NoPathFound(self._cmd_build_path)
            exit(1)
        _makefile_path = self._cmd_build_path / "Makefile"
        if not _makefile_path.exists():
            PRT.NoSuchFile(_makefile_path)
            exit(1)
        os.chdir(self._cmd_build_path)
        PRT.Process("Enter into: %s" % self._cmd_build_path)
        res = subprocess.call(["make", "uninstall"])
        if res != 0:
            exit(1)
        PRT.Complete("uninstall!")


    def clean(self):
        PRT.Start("clean!")
        if self._cmd_build_path.exists():
            os.chdir(self._cmd_build_path)
            p =subprocess.Popen(["make", "clean"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, err = p.communicate("")
            res = p.returncode
            if res == 0:
                PRT.Process(output.decode())
        PRT.Complete("clean!")


    def distclean(self):
        PRT.Start("disclean!")
        os.chdir(self._cmd_project_path)
        if self._cmd_build_path.exists():
            shutil.rmtree(self._cmd_build_path)
        if self._cmd_install_path.exists():
            shutil.rmtree(self._cmd_install_path)
        PRT.Complete("disclean!")


    def unknown(self, cmd):
        PRT.error("unknown", cmd)