#!/usr/bin/env python3
"""
Configuration Manager - PyCuTe Obfuscator
Handles obfuscation settings and options
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ObfuscationConfig:
    """Configuration for obfuscation process"""
    
    # User settings
    user_name: str = "Nguyễn Văn Trọng"
    input_file: str = ""
    output_file: Optional[str] = None
    
    # Obfuscation levels
    enable_string_obf: bool = True
    enable_integer_obf: bool = True
    enable_control_flow: bool = True
    enable_name_mangling: bool = True
    enable_dead_code: bool = False
    
    # Protection features
    enable_anti_debug: bool = True
    enable_anti_decompile: bool = True
    enable_anti_crack: bool = True
    enable_integrity_check: bool = False
    
    # Advanced options
    obfuscation_level: int = 3  # 1=Low, 2=Medium, 3=High
    more_obfuscation: bool = False
    preserve_names: List[str] = None
    
    # Performance
    use_multiprocessing: bool = False
    verbose: bool = False
    
    def __post_init__(self):
        if self.preserve_names is None:
            self.preserve_names = ["__main__", "__init__"]
        
        if self.output_file is None and self.input_file:
            #self.output_file = f"obfuscated_{self.input_file}"
            self.output_file = f"obf_{self.input_file}"
    
    def get_level_name(self) -> str:
        """Get human-readable obfuscation level"""
        levels = {1: "Low", 2: "Medium", 3: "High"}
        return levels.get(self.obfuscation_level, " High")
    
    def to_dict(self) -> dict:
        """Convert config to dictionary"""
        return {
            "user_name": self.user_name,
            "input_file": self.input_file,
            "output_file": self.output_file,
            "level": self.get_level_name(),
            "anti_debug": self.enable_anti_debug,
            "anti_decompile": self.enable_anti_decompile,
            "anti_crack": self.enable_anti_crack,
        }


class Config:
    """Global configuration manager"""
    
    _instance: Optional[ObfuscationConfig] = None
    
    @classmethod
    def get(cls) -> ObfuscationConfig:
        """Get or create configuration instance"""
        if cls._instance is None:
            cls._instance = ObfuscationConfig()
        return cls._instance
    
    @classmethod
    def set(cls, config: ObfuscationConfig):
        """Set configuration instance"""
        cls._instance = config
    
    @classmethod
    def reset(cls):
        """Reset configuration to defaults"""
        cls._instance = ObfuscationConfig()
