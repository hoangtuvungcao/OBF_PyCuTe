#!/usr/bin/env python3
"""
Control Flow Obfuscation - PyCuTe Obfuscator
Makes code flow harder to follow using nested try-except
"""

import ast
from typing import List
from utils.random_gen import RandomGenerator, rd


class ControlFlowObfuscator:
    """Obfuscate control flow with nested structures"""
    
    def __init__(self, memory_error_class: str):
        self.memory_error_class = memory_error_class
    
    def create_exception_wrapper(self, body: List[ast.stmt]) -> List[ast.stmt]:
        """
        Wrap statements in nested try-except blocks
        
        Args:
            body: Statements to wrap
            
        Returns:
            Wrapped statements
        """
        var = rd()
        en = rd()
        
        wrapped = [
            ast.AugAssign(
                target=ast.Name(id=var, ctx=ast.Store()),
                op=ast.Add(),
                value=ast.Constant(value=1)
            ),
            ast.Try(
                body=[
                    ast.Raise(
                        exc=ast.Call(
                            func=ast.Name(id=self.memory_error_class, ctx=ast.Load()),
                            args=[ast.Name(id=var, ctx=ast.Load())],
                            keywords=[]
                        )
                    )
                ],
                handlers=[
                    ast.ExceptHandler(
                        type=ast.Name(id=self.memory_error_class, ctx=ast.Load()),
                        name=en,
                        body=[]
                    )
                ],
                orelse=[],
                finalbody=[]
            )
        ]
        
        # Add each original statement wrapped in conditional
        for stmt in body:
            wrapped[1].handlers[0].body.append(
                ast.If(
                    test=ast.Compare(
                        left=ast.Subscript(
                            value=ast.Attribute(
                                value=ast.Name(id=en, ctx=ast.Load()),
                                attr='args',
                                ctx=ast.Load()
                            ),
                            slice=ast.Constant(value=0),
                            ctx=ast.Load()
                        ),
                        ops=[ast.Eq()],
                        comparators=[ast.Constant(value=1)]
                    ),
                    body=[stmt],
                    orelse=[]
                )
            )
        
        # Add junk conditions
        wrapped[1].handlers[0].body.extend(self._generate_junk_conditions(en, len(body)))
        
        # Add variable initialization
        init = ast.Assign(
            targets=[ast.Name(id=var, ctx=ast.Store())],
            value=ast.Constant(value=0)
        )
        
        return [init] + wrapped
    
    def _generate_junk_conditions(self, en: str, max_value: int) -> List[ast.If]:
        """Generate junk conditional statements"""
        import random
        junk = []
        line = max_value + 1
        
        for i in range(random.randint(1, 5)):
            case_name = f"__{rd()}"
            junk.append(
                ast.If(
                    test=ast.Compare(
                        left=ast.Subscript(
                            value=ast.Attribute(
                                value=ast.Name(id=en, ctx=ast.Load()),
                                attr='args',
                                ctx=ast.Load()
                            ),
                            slice=ast.Constant(value=0),
                            ctx=ast.Load()
                        ),
                        ops=[ast.Eq()],
                        comparators=[ast.Constant(value=line)]
                    ),
                    body=[
                        ast.Assign(
                            targets=[ast.Name(id=case_name, ctx=ast.Store())],
                            value=ast.Constant(value=random.randint(0xFFFFF, 0xFFFFFFFFFFFF))
                        )
                    ],
                    orelse=[]
                )
            )
            line += 1
        
        return junk
    
    def wrap_function(self, node: ast.FunctionDef) -> ast.FunctionDef:
        """Wrap function body with control flow obfuscation"""
        original_body = node.body
        var = rd()
        en = rd()
        
        wrapped_body = [
            ast.AugAssign(
                target=ast.Name(id=var, ctx=ast.Store()),
                op=ast.Add(),
                value=ast.Constant(value=1)
            ),
            ast.Try(
                body=[
                    ast.Raise(
                        exc=ast.Call(
                            func=ast.Name(id=self.memory_error_class, ctx=ast.Load()),
                            args=[ast.Name(id=var, ctx=ast.Load())],
                            keywords=[]
                        )
                    )
                ],
                handlers=[
                    ast.ExceptHandler(
                        type=ast.Name(id=self.memory_error_class, ctx=ast.Load()),
                        name=en,
                        body=[]
                    )
                ],
                orelse=[],
                finalbody=[]
            )
        ]
        
        for stmt in original_body:
            wrapped_body[1].handlers[0].body.append(
                ast.If(
                    test=ast.Compare(
                        left=ast.Subscript(
                            value=ast.Attribute(
                                value=ast.Name(id=en, ctx=ast.Load()),
                                attr='args',
                                ctx=ast.Load()
                            ),
                            slice=ast.Constant(value=0),
                            ctx=ast.Load()
                        ),
                        ops=[ast.Eq()],
                        comparators=[ast.Constant(value=1)]
                    ),
                    body=[stmt],
                    orelse=[]
                )
            )
        
        wrapped_body[1].handlers[0].body.extend(
            self._generate_junk_conditions(en, len(original_body))
        )
        
        node.body = [
            ast.Assign(
                targets=[ast.Name(id=var, ctx=ast.Store())],
                value=ast.Constant(value=0)
            )
        ] + wrapped_body
        
        return node
