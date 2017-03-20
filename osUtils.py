#-*- coding: utf-8 -*-
import os, sys, functools
from subprocess import Popen, PIPE

def subcmd(cmd):
    subpipe = Popen(cmd, shell = True, stdout = PIPE, stderr = PIPE)
    subout, suberr = subpipe.communicate()
    retcode = subpipe.wait()
    return (subout, suberr, retcode)
