#!/usr/bin/env python3
"""
Configuration Profiles - PyCute Obfuscator
Pre-configured obfuscation profiles for different use cases
"""

from dataclasses import dataclass, asdict
from typing import Dict
from utils.config import ObfuscationConfig


class ProfileManager:
    """Manage obfuscation profiles"""
    
    PROFILES: Dict[str, dict] = {
        "minimal": {
            "name": "Minimal Protection",
            "description": "Light obfuscation for quick testing",
            "enable_string_obf": True,
            "enable_integer_obf": False,
            "enable_control_flow": False,
            "enable_name_mangling": False,
            "enable_dead_code": False,
            "enable_anti_debug": False,
            "enable_anti_decompile": False,
            "enable_anti_crack": False,
            "enable_integrity_check": False,
            "obfuscation_level": 1,
        },
        
        "balanced": {
            "name": "Balanced Protection",
            "description": "Good balance between security and performance",
            "enable_string_obf": True,
            "enable_integer_obf": True,
            "enable_control_flow": True,
            "enable_name_mangling": True,
            "enable_dead_code": False,
            "enable_anti_debug": True,
            "enable_anti_decompile": True,
            "enable_anti_crack": True,
            "enable_integrity_check": False,
            "obfuscation_level": 2,
        },
        
        "maximum": {
            "name": "Maximum Protection",
            "description": "Strongest protection, larger output size",
            "enable_string_obf": True,
            "enable_integer_obf": True,
            "enable_control_flow": True,
            "enable_name_mangling": True,
            "enable_dead_code": True,
            "enable_anti_debug": True,
            "enable_anti_decompile": True,
            "enable_anti_crack": True,
            "enable_integrity_check": True,
            "obfuscation_level": 3,
            "more_obfuscation": True,
        },
        
        "production": {
            "name": "Production Ready",
            "description": "Optimized for production deployment",
            "enable_string_obf": True,
            "enable_integer_obf": True,
            "enable_control_flow": True,
            "enable_name_mangling": True,
            "enable_dead_code": False,
            "enable_anti_debug": True,
            "enable_anti_decompile": True,
            "enable_anti_crack": True,
            "enable_integrity_check": True,
            "obfuscation_level": 2,
        },
    }
    
    @classmethod
    def get_profile(cls, profile_name: str) -> ObfuscationConfig:
        """
        Get configuration for named profile
        
        Args:
            profile_name: Profile name (minimal, balanced, maximum, production)
            
        Returns:
            ObfuscationConfig with profile settings
        """
        if profile_name not in cls.PROFILES:
            raise ValueError(f"Unknown profile: {profile_name}")
        
        profile_data = cls.PROFILES[profile_name].copy()
        # Remove metadata
        profile_data.pop('name', None)
        profile_data.pop('description', None)
        
        config = ObfuscationConfig(**profile_data)
        return config
    
    @classmethod
    def list_profiles(cls) -> Dict[str, str]:
        """
        List all available profiles
        
        Returns:
            Dictionary mapping profile names to descriptions
        """
        return {
            name: data.get("description", "")
            for name, data in cls.PROFILES.items()
        }
    
    @classmethod
    def save_custom_profile(cls, name: str, config: ObfuscationConfig):
        """Save custom profile"""
        cls.PROFILES[name] = {
            "name": f"Custom: {name}",
            "description": "User-defined profile",
            **asdict(config)
        }
    
    @classmethod
    def get_profile_summary(cls, profile_name: str) -> str:
        """Get human-readable profile summary"""
        if profile_name not in cls.PROFILES:
            return f"Unknown profile: {profile_name}"
        
        profile = cls.PROFILES[profile_name]
        summary = f"""
Profile: {profile.get('name', profile_name)}
Description: {profile.get('description', 'N/A')}
Level: {profile.get('obfuscation_level', 2)}

Features Enabled:
  - String Obfuscation: {profile.get('enable_string_obf', False)}
  - Integer Obfuscation: {profile.get('enable_integer_obf', False)}
  - Control Flow: {profile.get('enable_control_flow', False)}
  - Name Mangling: {profile.get('enable_name_mangling', False)}
  - Dead Code: {profile.get('enable_dead_code', False)}
  - Anti-Debug: {profile.get('enable_anti_debug', False)}
  - Anti-Decompile: {profile.get('enable_anti_decompile', False)}
  - Integrity Check: {profile.get('enable_integrity_check', False)}
"""
        return summary
