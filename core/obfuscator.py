#!/usr/bin/env python3
"""
Main Obfuscator Engine - PyCuTe Obfuscator
Central orchestration of all obfuscation techniques
"""

import ast
from pathlib import Path
from typing import Optional

from core.ast_transformer import ASTTransformer
from techniques.control_flow import ControlFlowObfuscator
from techniques.name_mangling import NameMangler
from techniques.dead_code import DeadCodeInjector
from protection.anti_debug import AntiDebug
from protection.anti_decompile import AntiDecompile
from protection.integrity import IntegrityChecker
from protection.anti_vm import AntiVM
from protection.anti_tamper import AntiTamper
from utils.config import ObfuscationConfig
from utils.random_gen import rd
from ui.progress import ProgressTracker, SimpleProgress


class ObfuscatorEngine:
    """Main obfuscation engine coordinating all techniques"""
    
    def __init__(self, config: ObfuscationConfig):
        """
        Initialize obfuscator engine
        
        Args:
            config: Obfuscation configuration
        """
        self.config = config
        self.memory_error_class = rd()
    
    def obfuscate_file(self, input_path: str, output_path: Optional[str] = None) -> str:
        """
        Obfuscate a Python file
        
        Args:
            input_path: Path to input file
            output_path: Path to output file (optional)
            
        Returns:
            Path to obfuscated file
        """
        # Read source code
        with open(input_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # Obfuscate
        obfuscated_code = self.obfuscate(source_code)
        
        # Determine output path
        if output_path is None:
            output_path = f"obf_{Path(input_path).name}"
        
        # Write output
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(obfuscated_code)
        
        return output_path
    
    def obfuscate(self, source_code: str) -> str:
        """
        Obfuscate Python source code
        
        Args:
            source_code: Original Python code
            
        Returns:
            Obfuscated Python code
        """
        # Progress tracking
        stages = [
            "Parsing code",
            "String obfuscation",
            "Integer obfuscation",
            "Control flow",
            "Name mangling",
            "Adding protections",
            "Finalizing"
        ]
        progress = SimpleProgress(stages)
        
        # Stage 1: Parse
        progress.next_stage()
        tree = ast.parse(source_code)
        
        # Stage 2-3: AST transformation (strings + integers)
        progress.next_stage()
        transformer = ASTTransformer(
            memory_error_class=self.memory_error_class,
            enable_strings=self.config.enable_string_obf,
            enable_integers=self.config.enable_integer_obf
        )
        obfuscated_code = transformer.transform(source_code)
        progress.next_stage()
        
        # Re-parse for further transformations
        tree = ast.parse(obfuscated_code)
        
        # Stage 4: Control flow obfuscation
        if self.config.enable_control_flow:
            progress.next_stage()
            tree = self._apply_control_flow(tree)
        else:
            progress.next_stage()
        
        # Stage 5: Name mangling
        if self.config.enable_name_mangling:
            progress.next_stage()
            preserve = set(self.config.preserve_names)
            preserve.add(self.memory_error_class)
            mangler = NameMangler(preserve)
            tree = mangler.rename_in_tree(tree)
            ast.fix_missing_locations(tree)
        else:
            progress.next_stage()
        
        # Stage 6: Add protections
        progress.next_stage()
        protection_code = self._generate_protection_code()
        
        # Stage 7: Finalize
        progress.next_stage()
        final_code = self._finalize(tree, protection_code)
        
        progress.complete()
        
        return final_code
    
    def _apply_control_flow(self, tree: ast.Module) -> ast.Module:
        """Apply control flow obfuscation"""
        obfuscator = ControlFlowObfuscator(self.memory_error_class)
        
        # Wrap functions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                obfuscator.wrap_function(node)
        
        # Wrap module-level statements
        new_body = []
        for stmt in tree.body:
            if isinstance(stmt, (ast.Assign, ast.Expr)):
                wrapped = obfuscator.create_exception_wrapper([stmt])
                new_body.extend(wrapped)
            else:
                new_body.append(stmt)
        
        tree.body = new_body
        
        # Fix missing location information for all newly created nodes
        ast.fix_missing_locations(tree)
        
        return tree
    
    def _generate_protection_code(self) -> str:
        """Generate protection code header"""
        protection_code = f"""
class {self.memory_error_class}(Exception):
    pass

"""
        
        if self.config.enable_anti_debug:
            protection_code += AntiDebug.generate_code() + "\n\n"
        
        if self.config.enable_anti_decompile:
            protection_code += AntiDecompile.generate_full_protection() + "\n\n"
        
        if self.config.enable_integrity_check:
            protection_code += IntegrityChecker.generate_check_code() + "\n\n"
            protection_code += IntegrityChecker.generate_library_check() + "\n\n"
        
        # NEW: Add Anti-VM protection
        if self.config.enable_anti_debug:  # Include with anti-debug
            protection_code += AntiVM.generate_detection_code() + "\n\n"
        
        # NEW: Add Ultra Anti-Tamper (STRONGER THAN ORIGINAL)
        protection_code += AntiTamper.generate_ultra_protection() + "\n\n"
        protection_code += AntiTamper.generate_code_signing() + "\n\n"
        
        return protection_code
    
    def _finalize(self, tree: ast.Module, protection_code: str) -> str:
        """Finalize obfuscated code"""
        # Unparse AST
        obfuscated_code = ast.unparse(tree)
        
        # Combine protection + code
        final_code = protection_code + obfuscated_code
        
        # Add header comment
        header = f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# The code has been messed up with PyCuTe v3.0.
# Obfuscated by: {self.config.user_name}
# Protection Level: {self.config.get_level_name()}
# ==============================================================================

"""
        
        return header + final_code
