#!/usr/bin/env python3
"""
Integer Encoder - PyCuTe Obfuscator
Obfuscates integer constants using mathematical operations
"""

from typing import Union
from utils.random_gen import RandomGenerator, rd


class IntegerEncoder:
    """Handles integer constant obfuscation"""
    
    # Large offset for obfuscation
    OFFSET = 0xFFFFFFFFFFFFFFFFFFFFFF
    
    def __init__(self, vaicalon_func: str, idk_func: str):
        """
        Initialize integer encoder
        
        Args:
            vaicalon_func: Name of value calculation function variable
            idk_func: Name of byte decoding function variable
        """
        self.vaicalon_func = vaicalon_func
        self.idk_func = idk_func
    
    @staticmethod
    def _to_bytes(value: int) -> bytes:
        """
        Convert integer to byte representation
        
        Args:
            value: Integer to convert
            
        Returns:
            Byte representation with prefix
        """
        byte_array = bytearray()
        byte_array.extend(value.to_bytes((value.bit_length() + 7) // 8, 'big'))
        return b"0xFFFFFFFF/" + byte_array
    
    def obfuscate(self, value: Union[int, bool]) -> str:
        """
        Obfuscate integer or boolean value
        
        Args:
            value: Number or boolean to obfuscate
            
        Returns:
            Obfuscated value as Python code
        """
        if isinstance(value, bool):
            return self._obfuscate_bool(value)
        else:
            return self._obfuscate_int(value)
    
    def _obfuscate_bool(self, value: bool) -> str:
        """Obfuscate boolean value"""
        n = rd()
        if value:
            return (
                f'(lambda: (lambda {n}: {n} + '
                f'(lambda : {self.vaicalon_func}({(1 + self.OFFSET)}))())'
                f'(0) == 1)()'
            )
        else:
            return (
                f'(lambda: (lambda {n}: {n} - '
                f'(lambda : {self.vaicalon_func}(({(1 + self.OFFSET)} ) ) )())'
                f'(0) == 1)()'
            )
    
    def _obfuscate_int(self, value: int) -> str:
        """Obfuscate integer value"""
        byte_repr = self._to_bytes(int(value))
        return f'(lambda: {self.idk_func}({byte_repr}))()'
    
    @staticmethod
    def create_decoder_code(
        vaicalon_func: str,
        idk_func: str,
        int_func: str,
        bytearray_func: str,
        len_func: str,
        wt_var: str,
        exx_var: str,
        temp_var: str,
        temp1_var: str
    ) -> str:
        """
        Generate decoder functions for obfuscated integers
        
        Returns:
            Python code for decoder functions
        """
        decoder = f"""def {vaicalon_func}({wt_var}):
    return {int_func}({wt_var}-0xFFFFFFFFFFFFFFFFFFFFFF)
def {idk_func}({wt_var}):
    {exx_var} = {bytearray_func}({wt_var}[{len_func}(b'0xFFFFFFFF/'):])
    {temp_var} = 0
    for {temp1_var} in {exx_var}:
        {temp_var} = {temp_var} * 256 + {temp1_var}
    return {temp_var}
"""
        return decoder
