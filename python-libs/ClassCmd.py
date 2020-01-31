#!/usr/bin/env python
#-*- coding = utf-8 -*-
import os, subprocess, shutil, time
from ClassPrint import *
from multiprocessing import cpu_count

PRT = ClassPrint()
COMPILE_TYPES = ["Unix Makefiles",""]

class ClassCmd:
    def __init__(self, project_path, compile_type, build_path, config_file, verbose):
        PRT.debug("%s\%s\%s\%s\%s"%(project_path, compile_type, build_path, config_file, verbose))
        if not os.path.exists(project_path):
            PRT.NoPathFound(project_path)
            exit(1)
        self.project_path = project_path
        if compile_type not in COMPILE_TYPES:
            PRT.error("no compile type found - %s. set default type." % (compile_type))
            compile_type = "Unix Makefiles"
        self.compile_type = compile_type
        self.build_path = build_path
        self.config_file = config_file
        self.verbose = verbose

    def menuconfig(self):
        PRT.Start("menuconfig!")
        time_start = time.time()

        if not os.path.exists(self.build_path):
            os.mkdir(self.build_path)
        os.chdir(self.build_path)
        PRT.Process("Enter into: %s" % self.build_path)

        if not os.path.exists(self.build_path + "/Makefile"):
            if not os.path.isabs(self.config_file):
                self.config_file = os.path.join(self.project_path, self.config_file)
            config_path = os.path.abspath(self.config_file)
            PRT.Process("Config filename: %s" % config_path)
            if not os.path.exists(config_path):
                PRT.NoPathFound(config_path)
                exit(1)
            res = subprocess.call(["cmake", "-G", self.compile_type, "-DDEFAULT_CONFIG_FILE={}".format(config_path), "-DCOMPILE_UNIT_TEST={}".format(""), ".."])
            if res != 0:
                exit(1)
        res = subprocess.call(["make", "menuconfig"])
        if res != 0:
            exit(1)

    def clean_conf(self):
        PRT.Start("clean configuration!")
        if os.path.exists(".config.mk"):
            os.remove(".config.mk")
        if os.path.exists(self.build_path + os.path.split() + "config"):
            shutil.rmtree(self.build_path + os.path.split() + "config")
        PRT.Complete("clean configuration!")

    def config(self):
        PRT.Complete("configuration!")

    def build(self):
        PRT.Start("build!")
        time_start = time.time()

        if not os.path.exists(self.build_path):
            os.mkdir(self.build_path)
        os.chdir(self.build_path)
        PRT.Process("Enter into: %s" % self.build_path)

        if not os.path.exists("Makefile"):
            if not os.path.isabs(self.config_file):
                self.config_file = os.path.join(self.project_path, self.config_file)
            config_path = os.path.abspath(self.config_file)
            if not os.path.exists(config_path):
                PRT.NoPathFound(config_path)
                exit(1)
            res = subprocess.call(["cmake", "-G", self.compile_type, "-DDEFAULT_CONFIG_FILE={}".format(config_path), "-DCOMPILE_UNIT_TEST={}".format("BUILD"), ".."])
            if res != 0:
                exit(1)
        if self.verbose:
                res = subprocess.call(["make", "VERBOSE=1"])
        else:
            res = subprocess.call(["make", "-j{}".format(cpu_count())])
        if res != 0:
            exit(1)

        time_end = time.time()
        PRT.TimeLast(time_start, time_end)
        PRT.Complete("build!")

    def rebuild(self):
        self.build()

    def clean(self):
        PRT.Start("clean!")
        if os.path.exists(self.build_path):
            os.chdir(self.build_path)
            p =subprocess.Popen(["make", "clean"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, err = p.communicate("")
            res = p.returncode
            if res == 0:
                PRT.info(output.decode())
        PRT.Complete("clean!")

    def distclean(self):
        PRT.Start("disclean!")
        self.clean(self.build_path)
        os.chdir(self.build_path + os.path.split() + "..")
        shutil.rmtree(self.build_path)
        PRT.Complete("disclean!")

    def unit_test(self):
        PRT.Start("unit_test!")
        time_start = time.time()

        if not os.path.exists(self.build_path):
            os.mkdir(self.build_path)
        os.chdir(self.build_path)
        PRT.Process("Enter into: %s" % self.build_path)

        if not os.path.exists("Makefile"):
            if not os.path.isabs(self.config_file):
                self.config_file = os.path.join(self.project_path, self.config_file)
            config_path = os.path.abspath(self.config_file)
            if not os.path.exists(config_path):
                PRT.NoPathFound(config_path)
                exit(1)
            res = subprocess.call(["cmake", "-G", self.compile_type, "-DDEFAULT_CONFIG_FILE={}".format(config_path), "-DCOMPILE_UNIT_TEST={}".format("UNIT_TEST"), ".."])
            if res != 0:
                exit(1)
        if self.verbose:
                res = subprocess.call(["make", "VERBOSE=1"])
        else:
            res = subprocess.call(["make", "-j{}".format(cpu_count())])
        if res != 0:
            exit(1)

        time_end = time.time()
        PRT.TimeLast(time_start, time_end)
        PRT.Complete("unit_test!")

    def install(self):
        PRT.Start("install!")
        time_start = time.time()

        if not os.path.exists(self.build_path):
            os.mkdir(self.build_path)
        os.chdir(self.build_path)
        PRT.Process("Enter into: %s" % self.build_path)

        res = subprocess.call(["make", "install"])
        if res != 0:
            exit(1)
        time_end = time.time()
        PRT.TimeLast(time_start, time_end)
        PRT.Complete("install!")

    def unknown(self):
        PRT.error("unknown cmd.")