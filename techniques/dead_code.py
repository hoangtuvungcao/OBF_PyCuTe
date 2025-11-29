#!/usr/bin/env python3
"""
Dead Code Injection - PyCuTe Obfuscator
Injects realistic-looking dead code
"""

import ast
import random
from typing import List
from utils.random_gen import RandomGenerator, rd


class DeadCodeInjector:
    """Inject dead code to confuse analysis"""
    
    @staticmethod
    def generate_dead_assignment() -> ast.Assign:
        """Generate dead variable assignment"""
        var_name = rd()
        value = random.choice([
            ast.Constant(value=random.randint(0, 1000)),
            ast.Constant(value=random.choice(["dead", "code", "junk"])),
            ast.List(elts=[ast.Constant(value=i) for i in range(random.randint(1, 5))], ctx=ast.Load())
        ])
        
        return ast.Assign(
            targets=[ast.Name(id=var_name, ctx=ast.Store())],
            value=value
        )
    
    @staticmethod
    def generate_dead_function() -> ast.FunctionDef:
        """Generate dead function definition"""
        func_name = rd()
        arg_name = rd()
        
        return ast.FunctionDef(
            name=func_name,
            args=ast.arguments(
                posonlyargs=[],
                args=[ast.arg(arg=arg_name, annotation=None)],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[]
            ),
            body=[
                ast.Return(value=ast.Name(id=arg_name, ctx=ast.Load()))
            ],
            decorator_list=[]
        )
    
    @staticmethod
    def generate_dead_conditional() -> ast.If:
        """Generate always-false conditional (dead code path)"""
        return ast.If(
            test=ast.Compare(
                left=ast.Constant(value="dummy_var1"),
                ops=[ast.Eq()],
                comparators=[ast.Constant(value="dummy_var2")]
            ),
            body=[
                DeadCodeInjector.generate_dead_assignment(),
                DeadCodeInjector.generate_dead_assignment()
            ],
            orelse=[]
        )
    
    @staticmethod
    def inject_into_body(body: List[ast.stmt], injection_rate: float = 0.2) -> List[ast.stmt]:
        """
        Inject dead code into statement list
        
        Args:
            body: Original statements
            injection_rate: Probability of injection per statement
            
        Returns:
            Modified statement list with dead code
        """
        new_body = []
        
        for stmt in body:
            new_body.append(stmt)
            
            # Randomly inject dead code
            if random.random() < injection_rate:
                dead_code = random.choice([
                    DeadCodeInjector.generate_dead_assignment(),
                    DeadCodeInjector.generate_dead_conditional()
                ])
                new_body.append(dead_code)
        
        return new_body
    
    @staticmethod
    def inject_dead_functions(tree: ast.Module, count: int = 3) -> ast.Module:
        """
        Inject dead functions at module level
        
        Args:
            tree: AST tree
            count: Number of dead functions to inject
            
        Returns:
            Modified AST tree
        """
        for _ in range(count):
            tree.body.insert(
                random.randint(0, len(tree.body)),
                DeadCodeInjector.generate_dead_function()
            )
        
        return tree
