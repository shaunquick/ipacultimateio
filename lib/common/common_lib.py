
import sys


isdebugset = False


def my_func_name(): 
    return (sys._getframe(1).f_code.co_name+"(): ")

def SetDebugOn():
    global isdebugset
    isdebugset = True

def isDebugOn():
    return(isdebugset)

