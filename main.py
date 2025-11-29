#!/usr/bin/env python3
import sys
import argparse
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.obfuscator import ObfuscatorEngine
from utils.config import ObfuscationConfig, Config
from utils.logger import ObfuscatorLogger
from utils.batch import BatchProcessor
from utils.profiles import ProfileManager
from ui.cli import CLI


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="PyCute Obfuscator - Enterprise Python Code Protection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                              Interactive mode
  %(prog)s -f script.py                Single file
  %(prog)s -f app.py -p maximum        With profile
  %(prog)s --batch project/            Batch process
  %(prog)s --list-profiles             Show profiles
        """
    )
    
    parser.add_argument('-f', '--file', help='Input file to obfuscate')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-p', '--profile', 
                       choices=['minimal', 'balanced', 'maximum', 'production'],
                       help='Obfuscation profile')
    parser.add_argument('--batch', metavar='DIR', help='Batch process directory')
    parser.add_argument('--recursive', action='store_true', 
                       help='Recursive directory search')
    parser.add_argument('--list-profiles', action='store_true',
                       help='List available profiles')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')
    
    return parser.parse_args()


def main():
    """Main entry point"""
    args = parse_arguments()
    
    # Setup logger
    logger = ObfuscatorLogger.get_logger()
    
    # List profiles mode
    if args.list_profiles:
        print("\n" + "="*60)
        print("  PyCute Obfuscator - Available Profiles")
        print("="*60)
        for name, description in ProfileManager.list_profiles().items():
            print(f"\n📋 {name.upper()}")
            print(f"   {description}")
            # Show details
            summary = ProfileManager.get_profile_summary(name)
            print(summary)
        return 0
    
    # Batch processing mode
    if args.batch:
        cli = CLI()
        cli.print_banner()
        
        print()
        cli.print(f" Batch Processing Mode: {args.batch}")
        print()
        
        # Get or create config
        if args.profile:
            config = ProfileManager.get_profile(args.profile)
            cli.print(f" Using profile: {args.profile}")
        else:
            config = ObfuscationConfig()
        
        # Process directory
        processor = BatchProcessor(config)
        results = processor.process_directory(
            args.batch,
            args.output or "obfuscated_output",
            recursive=args.recursive
        )
        
        # Show statistics
        stats = processor.get_statistics(results)
        print()
        cli.success("Batch processing complete!")
        cli.print(f" Total files: {stats['total']}")
        cli.print(f" Successful: {stats['successful']}")
        cli.print(f" Failed: {stats['failed']}")
        cli.print(f" Success rate: {stats['success_rate']:.1f}%")
        print()
        
        return 0
    
    # Single file mode
    if args.file:
        cli = CLI()
        cli.print_banner()
        
        # Get config
        if args.profile:
            config = ProfileManager.get_profile(args.profile)
            config.input_file = args.file
            config.output_file = args.output
            cli.print(f" Using profile: {args.profile}")
        else:
            config = ObfuscationConfig(
                input_file=args.file,
                output_file=args.output
            )
        
        # Show summary
        cli.show_summary(config)
        
        # Obfuscate
        cli.print(" Initializing obfuscator...")
        engine = ObfuscatorEngine(config)
        
        cli.print(" Starting obfuscation process...")
        print()
        
        try:
            output_file = engine.obfuscate_file(config.input_file, config.output_file)
            
            print()
            cli.success("Obfuscation completed!")
            cli.print(f" Output saved to: {output_file}")
            
            # Show file sizes
            import os
            original_size = os.path.getsize(config.input_file)
            obfuscated_size = os.path.getsize(output_file)
            ratio = obfuscated_size / original_size
            
            print()
            cli.print(f" Original size: {original_size:,} bytes")
            cli.print(f" Obfuscated size: {obfuscated_size:,} bytes")
            cli.print(f" Size ratio: {ratio:.2f}x")
            
            return 0
            
        except Exception as e:
            print()
            cli.error(f"Obfuscation failed: {str(e)}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            return 1
    
    # Interactive mode (no arguments)
    cli = CLI()
    cli.print_banner()
    
    # Get configuration from user
    config = cli.get_user_config()
    Config.set(config)
    
    # Show summary
    cli.show_summary(config)
    
    # Initialize obfuscator
    print()
    cli.print(" Initializing obfuscator...")
    engine = ObfuscatorEngine(config)
    
    # Obfuscate
    cli.print(" Starting obfuscation process...")
    print()
    
    try:
        output_file = engine.obfuscate_file(config.input_file, config.output_file)
        
        print()
        cli.success("Obfuscation completed!")
        cli.print(f" Output saved to: {output_file}")
        
        # Show file sizes
        import os
        original_size = os.path.getsize(config.input_file)
        obfuscated_size = os.path.getsize(output_file)
        ratio = obfuscated_size / original_size
        
        print()
        cli.print(f" Original size: {original_size:,} bytes")
        cli.print(f" Obfuscated size: {obfuscated_size:,} bytes")
        cli.print(f" Size ratio: {ratio:.2f}x")
        
        return 0
        
    except Exception as e:
        print()
        cli.error(f"Obfuscation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
