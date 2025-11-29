#!/usr/bin/env python3
"""
String Encoder - PyCuTe Obfuscator
Advanced string obfuscation using Unicode transformation and multi-layer encoding
"""

import zlib
from typing import List
from utils.random_gen import RandomGenerator


class StringEncoder:
    """Handles string obfuscation with Unicode encoding"""
    
    # Encoding offset (decompressed value)
    ENCODING_OFFSET = int(zlib.decompress(b'x\x9c36&\x17\x18\x99\x00!:0\x87P\xc6\xc6\x00\x0bx\x11v'))
    
    def __init__(self, join_func: str, hexrun_func: str, list_func: str, map_func: str):
        """
        Initialize string encoder
        
        Args:
            join_func: Name of join function variable
            hexrun_func: Name of hex conversion function variable
            list_func: Name of list function variable
            map_func: Name of map function variable
        """
        self.join_func = join_func
        self.hexrun_func = hexrun_func
        self.list_func = list_func
        self.map_func = map_func
    
    def encode_char(self, char: str) -> int:
        """
        Encode single character with offset
        
        Args:
            char: Character to encode
            
        Returns:
            Encoded integer value
        """
        return ord(char) + self.ENCODING_OFFSET
    
    def obfuscate(self, string: str) -> str:
        """
        Obfuscate a string by encoding each character
        
        Args:
            string: String to obfuscate
            
        Returns:
            Python code that decodes to the original string
        """
        # Encode each character
        encoded_chars = [str(self.encode_char(char)) for char in string]
        
        # Generate obfuscation code
        obf_code = f"{self.join_func}({self.list_func}({self.map_func}({self.hexrun_func}, [{', '.join(encoded_chars)}])))"
        
        return obf_code
