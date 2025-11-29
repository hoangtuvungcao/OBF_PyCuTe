#!/usr/bin/env python3
"""
Anti-Debug Protection - PyCuTe Obfuscator
ENHANCED anti-debugging with multiple detection techniques
"""

import sys
import os
import time
from typing import Callable


class AntiDebug:
    """Enhanced anti-debugging protection with multiple detection methods"""
    
    @staticmethod
    def generate_code() -> str:
        """
        Generate advanced anti-debugging code to inject into obfuscated output
        
        Returns:
            Python code implementing multiple anti-debug techniques
        """
        code = '''
import sys as __sys_module__
import time as __time_module__
import os as __os_module__

class __ProtectionLayer__:
    
    @staticmethod
    def __timing_check__():
        __start__ = __time_module__.perf_counter()
        __dummy__ = sum(range(1000))
        __end__ = __time_module__.perf_counter()
        if __end__ - __start__ > 0.01:
            __sys_module__.exit(1)
    
    @staticmethod
    def __trace_check__():
        if __sys_module__.gettrace() is not None:
            __sys_module__.exit(1)
    
    @staticmethod
    def __debugger_check__():
        try:
            import psutil as __psutil__
            __debuggers__ = ['gdb', 'lldb', 'pdb', 'pydevd', 'debugpy']
            for __proc__ in __psutil__.process_iter(['name']):
                if any(__d__ in __proc__.info['name'].lower() for __d__ in __debuggers__):
                    __sys_module__.exit(1)
        except:
            pass
    
    @staticmethod
    def __environment_check__():
        __debug_vars__ = ['PYTHONBREAKPOINT', 'PYDEBUG', 'PYTHONDEBUG']
        for __var__ in __debug_vars__:
            if __os_module__.environ.get(__var__):
                __sys_module__.exit(1)
    
    @staticmethod
    def __module_check__():
        __debug_modules__ = ['pdb', 'pydevd', 'debugpy', 'ipdb']
        for __mod__ in __debug_modules__:
            if __mod__ in __sys_module__.modules:
                __sys_module__.exit(1)
    
    @staticmethod
    def __protect__():
        try:
            __ProtectionLayer__.__trace_check__()
            __ProtectionLayer__.__timing_check__()
            __ProtectionLayer__.__environment_check__()
            __ProtectionLayer__.__module_check__()
            __ProtectionLayer__.__debugger_check__()
        except:
            pass

try:
    __ProtectionLayer__.__protect__()
except:
    pass

def __runtime_check__(__func__):
    def __wrapper__(*args, **kwargs):
        try:
            __ProtectionLayer__.__trace_check__()
        except:
            pass
        return __func__(*args, **kwargs)
    return __wrapper__
'''
        return code
    
    @staticmethod
    def create_trace_detection() -> str:
        """Generate trace detection code"""
        return """
# Trace detection
if __import__('sys').gettrace() is not None:
    __import__('sys').exit(1)
"""
    
    @staticmethod
    def create_timing_trap() -> str:
        """Generate timing-based debugger detection"""
        return """
# Timing trap
__t1__ = __import__('time').perf_counter()
_ = sum(range(500))
__t2__ = __import__('time').perf_counter()
if __t2__ - __t1__ > 0.005:
    __import__('sys').exit(1)
"""
    
    @staticmethod
    def wrap_function(func_code: str, func_name: str) -> str:
        """
        Wrap function with anti-debug checks
        
        Args:
            func_code: Original function code
            func_name: Function name
            
        Returns:
            Function code with anti-debug protection
        """
        wrapper = f"""
def {func_name}(*args, **kwargs):
    # Anti-debug check
    if __import__('sys').gettrace() is not None:
        __import__('sys').exit(1)
    
    # Original function
    {func_code}
"""
        return wrapper
