#!/usr/bin/env python3
"""
Progress Tracker - PyCuTe Obfuscator
Track and display obfuscation progress
"""

import sys
from typing import Optional

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False


class ProgressTracker:
    """Track obfuscation progress with visual feedback"""
    
    def __init__(self, total_steps: int = 100, desc: str = "Obfuscating"):
        self.total_steps = total_steps
        self.current_step = 0
        self.desc = desc
        self.pbar = None
        
        if TQDM_AVAILABLE:
            self.pbar = tqdm(total=total_steps, desc=desc, ncols=80)
    
    def update(self, steps: int = 1, message: str = ""):
        """Update progress"""
        self.current_step += steps
        
        if self.pbar:
            self.pbar.update(steps)
            if message:
                self.pbar.set_postfix_str(message)
        else:
            # Fallback: simple percentage
            percentage = (self.current_step / self.total_steps) * 100
            print(f"\r{self.desc}: {percentage:.1f}%  {message}", end='', flush=True)
    
    def set_message(self, message: str):
        """Set current operation message"""
        if self.pbar:
            self.pbar.set_postfix_str(message)
        else:
            percentage = (self.current_step / self.total_steps) * 100
            print(f"\r{self.desc}: {percentage:.1f}%  {message}", end='', flush=True)
    
    def close(self):
        """Close progress bar"""
        if self.pbar:
            self.pbar.close()
        else:
            print()  # New line
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class SimpleProgress:
    """Simple progress tracker without external dependencies"""
    
    def __init__(self, stages: list):
        self.stages = stages
        self.current_stage = 0
        self.total_stages = len(stages)
    
    def next_stage(self):
        """Move to next stage"""
        if self.current_stage < self.total_stages:
            stage_name = self.stages[self.current_stage]
            percentage = ((self.current_stage + 1) / self.total_stages) * 100
            print(f" [{percentage:5.1f}%] {stage_name}...", flush=True)
            self.current_stage += 1
    
    def complete(self):
        """Mark as complete"""
        try:
            print(" [100.0%] ✓ Obfuscation complete!")
        except UnicodeEncodeError:
            print(" [100.0%] [OK] Obfuscation complete!")
