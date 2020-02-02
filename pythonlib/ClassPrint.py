#!/usr/bin/env python
#-*- coding = utf-8 -*-
import sys, os

class ClassPrint:
    def __init__(self):
        pass

    def debug(self, title, str):
        print("[Debug] %s, %s - %s: %s" % (os.path.basename(sys._getframe().f_back.f_code.co_filename), sys._getframe().f_back.f_code.co_name, title, str))

    def info(self, title, str):
        print(">>> %s: %s" % (title, str))

    def error(self, title, str):
        print("[Error]: %s: %s" % (title, str))
        print("[Error]: %s: %s:%s" %(sys._getframe().f_back.f_code.co_filename, sys._getframe().f_back.f_code.co_name, sys._getframe().f_back.f_lineno))

    def Complete(self, str):
        print(">>> Complete: %s" % str)

    def Success(self, str):
        print(">>> Success: %s" % str)

    def Start(self, str):
        print(">>> Start: %s" % str)

    def Process(self, str):
        print("-- Process: %s" % str)

    def NoPathFound(self, path):
        print("[Error]: no path found, %s" % (path))
        print("[Error]: %s:%s:%s" %(sys._getframe().f_back.f_code.co_filename, sys._getframe().f_back.f_code.co_name, sys._getframe().f_back.f_lineno))

    def NoSuchFile(self, file):
        print("[Error]: no such a file, %s" % (file))
        print("[Error]: %s:%s:%s" %(sys._getframe().f_back.f_code.co_filename, sys._getframe().f_back.f_code.co_name, sys._getframe().f_back.f_lineno))

    def Result(self, title, str):
        print("==================================")
        print("  %s: %s" %(title, str))
        print("==================================")

    def TimeLast(self, time_start, time_end):
        self.Result("time last", "%.2fs" %(time_end - time_start))