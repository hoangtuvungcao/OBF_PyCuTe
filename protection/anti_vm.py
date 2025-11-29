#!/usr/bin/env python3
"""
Anti-VM Detection - PyCute Obfuscator
Detect virtual machine and sandbox environments
"""

import os
import platform
import subprocess


class AntiVM:
    """Detect virtual machine environments"""
    
    @staticmethod
    def generate_detection_code() -> str:
        """
        Generate VM detection code to inject
        
        Returns:
            Python code for VM detection
        """
        code = '''
import os as __os__
import platform as __platform__
import subprocess as __subprocess__

class __VMDetector__:
    
    @staticmethod
    def __check_mac_address__():
        try:
            import uuid as __uuid__
            __mac__ = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
            
            __vm_macs__ = ['00:05:69', '00:0C:29', '00:1C:14', '00:50:56', '08:00:27']
            for __prefix__ in __vm_macs__:
                if __mac__.startswith(__prefix__):
                    __import__('sys').exit(1)
        except:
            pass
    
    @staticmethod
    def __check_hostname__():
        try:
            __hostname__ = __platform__.node().lower()
            __vm_names__ = ['vmware', 'vbox', 'virtualbox', 'qemu', 'kvm', 'xen']
            for __vm__ in __vm_names__:
                if __vm__ in __hostname__:
                    __import__('sys').exit(1)
        except:
            pass
    
    @staticmethod
    def __check_processes__():
        try:
            import psutil as __psutil__
            __vm_procs__ = ['vmtoolsd', 'vboxservice', 'vboxtray', 'qemu-ga']
            for __proc__ in __psutil__.process_iter(['name']):
                if __proc__.info['name'].lower() in __vm_procs__:
                    __import__('sys').exit(1)
        except:
            pass
    
    @staticmethod
    def __check_system_info__():
        try:
            __system__ = __platform__.system()
            if __system__ == 'Linux':
                try:
                    with open('/proc/cpuinfo', 'r') as __f__:
                        __cpu_info__ = __f__.read().lower()
                        if 'hypervisor' in __cpu_info__ or 'qemu' in __cpu_info__:
                            __import__('sys').exit(1)
                except:
                    pass
            elif __system__ == 'Windows':
                pass
        except:
            pass
    
    @staticmethod
    def __check_cpu_count__():
        try:
            import multiprocessing as __mp__
            if __mp__.cpu_count() < 2:
                pass
        except:
            pass
    
    @staticmethod
    def __detect__():
        try:
            __VMDetector__.__check_mac_address__()
            __VMDetector__.__check_hostname__()
            __VMDetector__.__check_processes__()
            __VMDetector__.__check_system_info__()
            __VMDetector__.__check_cpu_count__()
        except:
            pass

try:
    __VMDetector__.__detect__()
except:
    pass
'''
        return code
    
    @staticmethod
    def is_vm() -> bool:
        """
        Check if running in VM (for testing)
        
        Returns:
            True if VM detected
        """
        # Check MAC address
        try:
            import uuid
            mac = uuid.getnode()
            mac_str = ':'.join(['{:02x}'.format((mac >> ele) & 0xff) 
                               for ele in range(0,8*6,8)][::-1])
            vm_macs = ['00:05:69', '00:0C:29', '00:1C:14', '00:50:56', '08:00:27']
            for prefix in vm_macs:
                if mac_str.startswith(prefix):
                    return True
        except:
            pass
        
        # Check hostname
        try:
            hostname = platform.node().lower()
            if any(vm in hostname for vm in ['vmware', 'vbox', 'virtualbox', 'qemu']):
                return True
        except:
            pass
        
        return False
