#!/usr/bin/env python3
"""
AST Transformer - PyCuTe Obfuscator
Main AST transformation engine coordinating all obfuscation techniques
"""

import ast
from typing import Optional
from core.string_encoder import StringEncoder
from core.integer_encoder import IntegerEncoder
from utils.random_gen import rd


class ASTTransformer(ast.NodeTransformer):
    """Main AST transformer coordinating all obfuscation"""
    
    def __init__(self, memory_error_class: str, enable_strings: bool = True, enable_integers: bool = True):
        """
        Initialize AST transformer
        
        Args:
            memory_error_class: Name of custom exception class
            enable_strings: Enable string obfuscation
            enable_integers: Enable integer obfuscation
        """
        self.enable_strings = enable_strings
        self.enable_integers = enable_integers
        self.memory_error_class = memory_error_class
        
        # Initialize obfuscated variable names
        self._join = rd()
        self._int = rd()
        self._str = rd()
        self._bool = rd()
        self._type = rd()
        self._bytes = rd()
        self._list = rd()
        self._map = rd()
        self._hexrun = rd()
        self._argshexrun = rd()
        self._eval = rd()
        self._idk = rd()
        self.vaicalon = rd()
        
        # Initialize encoders
        self.string_encoder = StringEncoder(
            self._join, self._hexrun, self._list, self._map
        )
        self.integer_encoder = IntegerEncoder(
            self.vaicalon, self._idk
        )
    
    def transform(self, source_code: str) -> str:
        """
        Transform Python source code
        
        Args:
            source_code: Original Python code
            
        Returns:
            Obfuscated Python code
        """
        # Parse to AST
        tree = ast.parse(source_code)
        
        # Transform AST
        transformed_tree = self.visit(tree)
        
        # Generate decoder functions
        decoder_code = self._generate_decoder_functions()
        
        # Unparse back to code
        transformed_code = ast.unparse(transformed_tree)
        
        # Combine decoder + transformed code
        final_code = decoder_code + "\n\n" + transformed_code
        
        return final_code
    
    def visit_Constant(self, node: ast.Constant):
        """Visit constant nodes (strings, integers, booleans)"""
        if isinstance(node.value, str) and self.enable_strings:
            # Obfuscate strings
            obf_code = self.string_encoder.obfuscate(node.value)
            new_node = ast.parse(obf_code).body[0].value
            return ast.copy_location(new_node, node)
        
        elif isinstance(node.value, (int, bool)) and self.enable_integers:
            # Obfuscate integers/booleans
            obf_code = self.integer_encoder.obfuscate(node.value)
            new_node = ast.parse(obf_code).body[0].value
            return ast.copy_location(new_node, node)
        
        return node
    
    def visit_JoinedStr(self, node: ast.JoinedStr) -> ast.Call:
        """Convert f-strings to format() calls"""
        new_node = ast.Call(
            func=ast.Attribute(
                value=ast.Constant(value="{}" * len(node.values)),
                attr="format",
                ctx=ast.Load()
            ),
            args=[
                value.value if isinstance(value, ast.FormattedValue) else value
                for value in node.values
            ],
            keywords=[]
        )
        return ast.copy_location(new_node, node)
    
    def _generate_decoder_functions(self) -> str:
        """Generate all decoder functions needed for obfuscated code"""
        # Helper variable names
        utf8_var = rd()
        globals_dict = rd()
        temp_var = rd()
        temp1_var = rd()
        wt_var = rd()
        exp_var = rd()
        exx_var = rd()
        meh_var = rd()
        
        code = f'''# Generated decoder functions
import sys

{utf8_var} = "utf8"
{globals_dict} = globals()

# Initialize core functions
{self._eval} = eval
{self._bool} = bool
{self._str} = str
{self._type} = type
{self._int} = int
{self._bytes} = bytes
{self._list} = list
{self._map} = map

# String decoder
def {self._hexrun}({self._argshexrun}):
    {self._argshexrun} = {self._argshexrun} - 3333333333333333333333333333333333333333333333333333333333242422222222222222222722222233
    if {self._argshexrun} <= 0x7F:
        return {self._str}({self._bytes}([{self._argshexrun}]), {utf8_var})
    elif {self._argshexrun} <= 0x7FF:
        {temp_var} = 0xC0 | ({self._argshexrun} >> 6)
        {temp1_var} = 0x80 | ({self._argshexrun} & 0x3F)
        return {self._str}({self._bytes}([{temp_var}, {temp1_var}]), {utf8_var})
    elif {self._argshexrun} <= 0xFFFF:
        {temp_var} = 0xE0 | ({self._argshexrun} >> 12)
        {temp1_var} = 0x80 | (({self._argshexrun} >> 6) & 0x3F)
        {wt_var} = 0x80 | ({self._argshexrun} & 0x3F)
        return {self._str}({self._bytes}([{temp_var}, {temp1_var}, {wt_var}]), {utf8_var})
    else:
        {temp_var} = 0xF0 | ({self._argshexrun} >> 18)
        {temp1_var} = 0x80 | (({self._argshexrun} >> 12) & 0x3F)
        {wt_var} = 0x80 | (({self._argshexrun} >> 6) & 0x3F)
        {exp_var} = 0x80 | ({self._argshexrun} & 0x3F)
        return {self._str}({self._bytes}([{temp_var}, {temp1_var}, {wt_var}, {exp_var}]), {utf8_var})

# Join function
def {self._join}({exx_var}, *k):
    {meh_var} = ''
    for item in {exx_var}:
        {meh_var} += {self._str}(item)
    return {meh_var}

# Integer decoders
def {self.vaicalon}({wt_var}):
    return {self._int}({wt_var} - 0xFFFFFFFFFFFFFFFFFFFFFF)

def {self._idk}({wt_var}):
    {exx_var} = bytearray({wt_var}[len(b'0xFFFFFFFF/'):])
    {temp_var} = 0
    for {temp1_var} in {exx_var}:
        {temp_var} = {temp_var} * 256 + {temp1_var}
    return {temp_var}

'''
        return code
