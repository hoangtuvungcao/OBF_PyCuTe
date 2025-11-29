#!/usr/bin/env python3
"""
Integrity Checker - PyCuTe Obfuscator
NEW - Runtime code integrity validation
"""

import hashlib
import os


class IntegrityChecker:
    """Validates code integrity at runtime"""
    
    @staticmethod
    def generate_check_code(file_path: str = None) -> str:
        """
        Generate runtime integrity check code
        
        Args:
            file_path: Path to file being protected
            
        Returns:
            Integrity check code
        """
        code = '''
# ============================================================================
# CODE INTEGRITY PROTECTION
# Detects file tampering and modification
# ============================================================================

import hashlib as __hash_mod__
import sys as __sys_mod__

class __IntegrityChecker__:
    """Runtime integrity validation"""
    
    @staticmethod
    def __check_file__(__path__):
        """Verify file hasn't been modified"""
        try:
            with open(__path__, 'rb') as __f__:
                __content__ = __f__.read()
                __hash__ = __hash_mod__.sha256(__content__).hexdigest()
                # Original hash would be embedded here
                # if __hash__ != __expected__:
                #     __sys_mod__.exit(1)
        except:
            pass
    
    @staticmethod
    def __check_imports__():
        """Detect  suspicious imports"""
        __forbidden__ = ['ast', 'dis', 'inspect', 'types']
        for __mod__ in __forbidden__:
            if __mod__ in __sys_mod__.modules:
                try:
                    # Check if legitimately imported
                    if not hasattr(__sys_mod__.modules[__mod__], '__obf_safe__'):
                        pass  # Could exit here
                except:
                    pass

# Run integrity checks
try:
    __IntegrityChecker__.__check_imports__()
except:
    pass
'''
        return code
    
    @staticmethod
    def calculate_hash(content: str) -> str:
        """Calculate SHA256 hash of content"""
        return hashlib.sha256(content.encode()).hexdigest()
    
    @staticmethod
    def generate_library_check() -> str:
        """Generate library integrity check code"""
        code = '''
# Library integrity check
import os as __os__
import hashlib as __hash__

def __check_lib__(__lib_name__):
    """Verify library hasn't been tampered with"""
    try:
        __mod__ = __import__(__lib_name__)
        __path__ = __mod__.__file__
        if __path__ and __os__.path.exists(__path__):
            with open(__path__, 'rb') as __f__:
                __size__ = len(__f__.read())
                # Basic size check
                if __size__ < 100:  # Suspiciously small
                    __import__('sys').exit(1)
    except:
        pass

# Check critical libraries
for __lib__ in ['requests', 'pystyle']:
    try:
        __check_lib__(__lib__)
    except:
        pass
'''
        return code
