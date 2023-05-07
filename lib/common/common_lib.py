
import sys

def my_func_name(): 
    return (sys._getframe(1).f_code.co_name+"(): ")

