#!/usr/bin/env python3
"""
Modern CLI Interface - PyCuTe Obfuscator
Premium Python Code Protection with Style
"""

import sys
from typing import Optional
from pystyle import Col, Colorate,Colors, Add

try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from utils.config import ObfuscationConfig


class CLI:
    """Modern command-line interface"""
    
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.dark = Col.dark_gray
        self.light = Col.light_gray
        self.purple = Colors.StaticMIX((Col.purple, Col.red))
    
    def print_banner(self):
        """Display beautiful ASCII banner with PyCuTe branding"""
        # Set UTF-8 encoding for Windows console
        if sys.platform == "win32":
            try:
                sys.stdout.reconfigure(encoding='utf-8')
            except:
                pass
        
        text = """

    ███████╗ ██╗   ██╗ ██████╗██╗   ██╗████████╗███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║╚══██╔══╝██╔════╝
    ██████╔╝ ╚████╔╝ ██║     ██║   ██║   ██║   █████╗  
    ██╔═══╝   ╚██╔╝  ██║     ██║   ██║   ██║   ██╔══╝  
    ██║        ██║   ╚██████╗╚██████╔╝   ██║   ███████╗
    ╚═╝        ╚═╝    ╚═════╝ ╚═════╝    ╚═╝   ╚══════╝

        🔐 PyCuTe Obfuscator v3.0 - Premium Edition 🔐
          Advanced Python Code Protection & Obfuscation
                  ~ Make Your Code Unbreakable ~


"""
        banner = ""
        banner = Add.Add(text, banner, center=True)
        try:
            print(Colorate.Diagonal(Colors.DynamicMIX((Col.red, self.light)), banner))
        except UnicodeEncodeError:
            # Fallback for terminals that don't support Unicode
            print(text)
    
    def stage(self, text: str, symbol: str = 'PYCUTE ✨') -> str:
        """Format text with symbol"""
        return f""" {Col.Symbol(symbol, self.light, self.dark)} {Colorate.Diagonal(Colors.DynamicMIX((Col.red, self.light)), text)}{self.light}"""
    
    def input(self, prompt: str) -> str:
        """Get user input with styled prompt"""
        return input(self.stage(prompt))
    
    def print(self, text: str):
        """Print styled text"""
        print(self.stage(text))
    
    def print_progress(self, text: str):
        """Print progress message (without newline)"""
        print(self.stage(text), end='\r')
    
    def success(self, text: str):
        """Print success message"""
        self.print(f"✓ {text}")
    
    def error(self, text: str):
        """Print error message"""
        self.print(f"✗ {text}")
    
    def warning(self, text: str):
        """Print warning message"""
        self.print(f"⚠ {text}")
    
    def get_user_config(self) -> ObfuscationConfig:
        """Interactive configuration collection"""
        self.print_banner()
        
        config = ObfuscationConfig()
        
        # Get user name
        config.user_name = self.input(" ENTER YOUR NAME: ")
        
        # Get input file
        while True:
            config.input_file = self.input(" ENTER FILE TO OBFUSCATE: ")
            try:
                with open(config.input_file, 'r', encoding='utf-8') as f:
                    f.read()
                break
            except FileNotFoundError:
                self.error(" File not found! Please try again.")
        
        # Get options
        more_obf = self.input(" MORE OBFUSCATION? (y/n): ").upper()
        config.more_obfuscation = (more_obf == 'Y')
        
        anti_debug = self.input(" ENABLE COPYRIGHT PROTECTION / ANTI-DEBUG? (y/n): ").upper()
        config.enable_anti_debug = (anti_debug == 'Y')
        
        anti_crack = self.input(" ENABLE ANTI-CRACK PROTECTION? (y/n): ").upper()
        config.enable_anti_crack = (anti_crack == 'Y')
        
        return config
    
    def show_summary(self, config: ObfuscationConfig):
        """Display configuration summary"""
        print()
        self.print("═" * 50)
        self.print(" OBFUSCATION CONFIGURATION")
        self.print("═" * 50)
        self.print(f" Input File: {config.input_file}")
        self.print(f" Output File: {config.output_file}")
        self.print(f" Level: {config.get_level_name()}")
        self.print(f" Anti-Debug: {'Enabled' if config.enable_anti_debug else 'Disabled'}")
        self.print(f" Anti-Crack: {'Enabled' if config.enable_anti_crack else 'Disabled'}")
        self.print("═" * 50)
        print()
