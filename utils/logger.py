#!/usr/bin/env python3
"""
Logging System - PyCuTe Obfuscator
Comprehensive logging for debugging and monitoring
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


class ObfuscatorLogger:
    """Centralized logging system"""
    
    _instance: Optional[logging.Logger] = None
    
    @classmethod
    def get_logger(cls, name: str = "PyCuTe") -> logging.Logger:
        """Get or create logger instance"""
        if cls._instance is None:
            cls._instance = cls._setup_logger(name)
        return cls._instance
    
    @classmethod
    def _setup_logger(cls, name: str) -> logging.Logger:
        """Setup logger with file and console handlers (cross-platform)"""
        logger = logging.Logger(name)
        logger.setLevel(logging.DEBUG)
        
        # Create logs directory (cross-platform)
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # File handler - detailed logs
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"pycute_{timestamp}.log"
        file_handler = logging.FileHandler(
            log_file,
            encoding='utf-8',
            delay=True
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        
        # Console handler - important messages only
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.WARNING)
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    @classmethod
    def log_obfuscation_start(cls, input_file: str, config: dict):
        """Log obfuscation start"""
        logger = cls.get_logger()
        logger.info(f"Starting obfuscation of: {input_file}")
        logger.debug(f"Configuration: {config}")
    
    @classmethod
    def log_obfuscation_complete(cls, output_file: str, stats: dict):
        """Log obfuscation completion"""
        logger = cls.get_logger()
        logger.info(f"Obfuscation complete: {output_file}")
        logger.debug(f"Statistics: {stats}")
    
    @classmethod
    def log_error(cls, error: Exception, context: str = ""):
        """Log error with context"""
        logger = cls.get_logger()
        logger.error(f"{context}: {str(error)}", exc_info=True)
    
    @classmethod
    def log_warning(cls, message: str):
        """Log warning"""
        logger = cls.get_logger()
        logger.warning(message)
