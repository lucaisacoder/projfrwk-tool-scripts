#!/usr/bin/env python
#-*- coding = utf-8 -*-

class ClassPrint:
    def __init__(self):
        pass

    @staticmethod
    def info(str):
        print("Info: %s" % str)

    @staticmethod
    def error(str):
        print("Error: %s" % str)

    @staticmethod
    def Complete(str):
        print("Complete: %s" % str)

    @staticmethod
    def Success(str):
        print("Success: %s" % str)

    @staticmethod
    def Start(str):
        print("Start: %s" % str)

    @staticmethod
    def Process(str):
        print("Process: %s" % str)

    @staticmethod
    def NoPathFound(path):
        print("Error: no path found, %s" % path)

    @staticmethod
    def NoSuchFile(file):
        print("Error: no such a file, %s" % file)

    @staticmethod
    def TimeLast(time_start, time_end):
        print("==================================")
        print("  time last:%.2fs" %(time_end - time_start))
        print("==================================")