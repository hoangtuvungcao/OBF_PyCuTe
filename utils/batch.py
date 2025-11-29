#!/usr/bin/env python3
"""
Batch Processor - PyCute Obfuscator
Process multiple files efficiently
"""

import os
from pathlib import Path
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from core.obfuscator import ObfuscatorEngine
from utils.config import ObfuscationConfig
from utils.logger import ObfuscatorLogger


class BatchProcessor:
    """Process multiple files in batch"""
    
    def __init__(self, config: ObfuscationConfig, max_workers: int = 4):
        """
        Initialize batch processor
        
        Args:
            config: Base obfuscation configuration
            max_workers: Maximum parallel workers
        """
        self.config = config
        self.max_workers = max_workers
        self.logger = ObfuscatorLogger.get_logger()
    
    def process_directory(
        self, 
        input_dir: str, 
        output_dir: str,
        pattern: str = "*.py",
        recursive: bool = False
    ) -> Dict[str, str]:
        """
        Process all Python files in directory
        
        Args:
            input_dir: Input directory path
            output_dir: Output directory path
            pattern: File pattern to match
            recursive: Search recursively
            
        Returns:
            Dictionary mapping input files to output files
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Find all matching files
        if recursive:
            files = list(input_path.rglob(pattern))
        else:
            files = list(input_path.glob(pattern))
        
        self.logger.info(f"Found {len(files)} files to process")
        
        # Process files
        results = {}
        for file in files:
            relative_path = file.relative_to(input_path)
            output_file = output_path / relative_path
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                engine = ObfuscatorEngine(self.config)
                engine.obfuscate_file(str(file), str(output_file))
                results[str(file)] = str(output_file)
                self.logger.info(f"✓ Processed: {file.name}")
            except Exception as e:
                self.logger.error(f"✗ Failed: {file.name} - {str(e)}")
                results[str(file)] = None
        
        return results
    
    def process_files_parallel(
        self,
        input_files: List[str],
        output_dir: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Process multiple files in parallel
        
        Args:
            input_files: List of input file paths
            output_dir: Output directory (optional)
            
        Returns:
            Dictionary mapping input files to output files
        """
        results = {}
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {}
            
            for input_file in input_files:
                if output_dir:
                    output_file = Path(output_dir) / f"obf_{Path(input_file).name}"
                else:
                    output_file = f"obf_{input_file}"
                
                engine = ObfuscatorEngine(self.config)
                future = executor.submit(
                    engine.obfuscate_file,
                    input_file,
                    str(output_file)
                )
                futures[future] = (input_file, str(output_file))
            
            for future in as_completed(futures):
                input_file, output_file = futures[future]
                try:
                    future.result()
                    results[input_file] = output_file
                    self.logger.info(f"✓ Completed: {Path(input_file).name}")
                except Exception as e:
                    results[input_file] = None
                    self.logger.error(f"✗ Failed: {Path(input_file).name} - {str(e)}")
        
        return results
    
    def get_statistics(self, results: Dict[str, str]) -> dict:
        """Get processing statistics"""
        total = len(results)
        successful = sum(1 for v in results.values() if v is not None)
        failed = total - successful
        
        return {
            "total": total,
            "successful": successful,
            "failed": failed,
            "success_rate": (successful / total * 100) if total > 0 else 0
        }
