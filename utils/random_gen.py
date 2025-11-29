#!/usr/bin/env python3
"""
Random Name Generator - PyCuTe Obfuscator
Generates random variable names and strings for obfuscation
"""

import random
import string
from typing import List


class RandomGenerator:
    """Generate random strings for variable obfuscation"""
    
    @staticmethod
    def lowercase(length: int = 5) -> str:
        """Generate random lowercase string"""
        return ''.join(random.sample(string.ascii_lowercase, k=min(length, 26)))
    
    @staticmethod
    def chinese_chars(length: int = 3) -> str:
        """Generate random Chinese characters for variable names"""
        # Use only valid CJK Unified Ideographs range (U+4E00 to U+9FA5)
        # Avoid U+9FA6 to U+9FFF which are unassigned/invalid for identifiers
        return ''.join(random.choices(
            [chr(i) for i in range(0x4e00, 0x9FA6)], 
            k=length
        ))
    
    @staticmethod
    def unicode_chars(length: int = 1503) -> str:
        """Generate very long random Unicode string for padding"""
        return ''.join(random.choices(
            [chr(i) for i in range(1000, 3000)], 
            k=length
        ))
    
    @staticmethod
    def digits(length: int = 2) -> str:
        """Generate random digit string"""
        return ''.join(random.sample(string.digits[1:], k=min(length, 9)))
    
    @staticmethod
    def variable_name() -> str:
        """Generate obfuscated variable name using Chinese characters"""
        return RandomGenerator.chinese_chars(3)
    
    @staticmethod
    def long_variable_name() -> str:
        """Generate longer obfuscated variable name"""
        return RandomGenerator.chinese_chars(4)
    
    @staticmethod
    def random_comparison() -> str:
        """Generate random comparison operator"""
        return random.choice(['<', '>', '=='])


# Global instances for backward compatibility
def rd() -> str:
    """Generate 3-character Chinese variable name"""
    return RandomGenerator.variable_name()


def rd2() -> str:
    """Generate 4-character Chinese variable name"""
    return RandomGenerator.long_variable_name()


def _rd() -> str:
    """Generate 5-letter lowercase string"""
    return RandomGenerator.lowercase(5)


def _rd1() -> str:
    """Generate 1-letter lowercase string"""
    return RandomGenerator.lowercase(1)


def superrandom() -> str:
    """Generate very long Unicode string"""
    return RandomGenerator.unicode_chars(1503)


def rditerger() -> str:
    """Generate 2-digit number string"""
    return RandomGenerator.digits(2)


def randomchar() -> str:
    """Generate random comparison operator"""
    return RandomGenerator.random_comparison()
