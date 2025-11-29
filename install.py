#!/usr/bin/env python3
"""
PyCuTe Obfuscator - Easy Installation Script
Auto-installs all required dependencies for Python 3.9+
"""

import sys
import subprocess
import os
from pathlib import Path

# Force UTF-8 encoding for stdout/stderr to prevent UnicodeEncodeError on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_banner():
    """Display installation banner"""
    banner = f"""{Colors.HEADER}{Colors.BOLD}
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║       PyCuTe Obfuscator - Installation                ║
║       Enterprise-Grade Code Protection                ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
{Colors.ENDC}"""
    print(banner)


def check_python_version():
    """Verify Python version is 3.9 or higher"""
    print(f"{Colors.OKBLUE}[1/4] Checking Python version...{Colors.ENDC}")
    
    if sys.version_info < (3, 9):
        print(f"{Colors.FAIL}✗ Error: Python 3.9 or higher is required!{Colors.ENDC}")
        print(f"{Colors.WARNING}  Current version: {sys.version}{Colors.ENDC}")
        print(f"{Colors.WARNING}  Please upgrade Python and try again.{Colors.ENDC}")
        sys.exit(1)
    
    print(f"{Colors.OKGREEN}✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detected{Colors.ENDC}")
    return True


def check_pip():
    """Verify pip is available"""
    print(f"\n{Colors.OKBLUE}[2/4] Checking pip availability...{Colors.ENDC}")
    
    try:
        import pip
        print(f"{Colors.OKGREEN}✓ pip is available{Colors.ENDC}")
        return True
    except ImportError:
        print(f"{Colors.FAIL}✗ pip is not installed!{Colors.ENDC}")
        print(f"{Colors.WARNING}  Please install pip first: https://pip.pypa.io/en/stable/installation/{Colors.ENDC}")
        sys.exit(1)


def install_dependencies():
    """Install required packages from requirements.txt"""
    print(f"\n{Colors.OKBLUE}[3/4] Installing dependencies...{Colors.ENDC}")
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print(f"{Colors.FAIL}✗ requirements.txt not found!{Colors.ENDC}")
        sys.exit(1)
    
    try:
        # Upgrade pip first
        print(f"{Colors.OKCYAN}  → Upgrading pip...{Colors.ENDC}")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        # Install requirements
        print(f"{Colors.OKCYAN}  → Installing packages from requirements.txt...{Colors.ENDC}")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
            stdout=subprocess.DEVNULL
        )
        
        print(f"{Colors.OKGREEN}✓ All dependencies installed successfully{Colors.ENDC}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"{Colors.FAIL}✗ Installation failed!{Colors.ENDC}")
        print(f"{Colors.WARNING}  Error: {e}{Colors.ENDC}")
        print(f"{Colors.WARNING}  Try manual installation: pip install -r requirements.txt{Colors.ENDC}")
        sys.exit(1)


def verify_installation():
    """Verify all required packages are properly installed"""
    print(f"\n{Colors.OKBLUE}[4/4] Verifying installation...{Colors.ENDC}")
    
    required_packages = {
        'pystyle': 'Pystyle',
        'requests': 'Requests',
        'rich': 'Rich (optional)',
        'tqdm': 'Tqdm (optional)',
        'colorama': 'Colorama (optional)'
    }
    
    failed_packages = []
    optional_missing = []
    
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"{Colors.OKGREEN}  ✓ {name}{Colors.ENDC}")
        except ImportError:
            if 'optional' in name.lower():
                optional_missing.append(name)
                print(f"{Colors.WARNING}  ⚠ {name} (not critical){Colors.ENDC}")
            else:
                failed_packages.append(name)
                print(f"{Colors.FAIL}  ✗ {name}{Colors.ENDC}")
    
    if failed_packages:
        print(f"\n{Colors.FAIL}✗ Missing critical packages: {', '.join(failed_packages)}{Colors.ENDC}")
        sys.exit(1)
    
    if optional_missing:
        print(f"\n{Colors.WARNING}⚠ Optional packages missing (non-critical): {', '.join(optional_missing)}{Colors.ENDC}")
        print(f"{Colors.WARNING}  Some features may be limited, but the obfuscator will work.{Colors.ENDC}")
    
    print(f"\n{Colors.OKGREEN}{Colors.BOLD}✓ Installation completed successfully!{Colors.ENDC}")
    return True


def print_usage():
    """Display usage instructions"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}Next Steps:{Colors.ENDC}")
    print(f"{Colors.OKCYAN}  1. Run the obfuscator:{Colors.ENDC}")
    print(f"     python main.py")
    print(f"\n{Colors.OKCYAN}  2. Follow the on-screen prompts to:  {Colors.ENDC}")
    print(f"     • Enter your name")
    print(f"     • Select the file to obfuscate")
    print(f"     • Choose obfuscation options")
    print(f"\n{Colors.OKCYAN}  3. Advanced usage:{Colors.ENDC}")
    print(f"     • Edit main.py to customize settings")
    print(f"     • Check requirements.txt for optional packages")
    print(f"\n{Colors.OKGREEN}Enjoy your PyCuTe Obfuscator! 🚀{Colors.ENDC}\n")


def main():
    """Main installation flow"""
    try:
        print_banner()
        check_python_version()
        check_pip()
        install_dependencies()
        verify_installation()
        print_usage()
        
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Installation cancelled by user.{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.FAIL}Unexpected error: {e}{Colors.ENDC}")
        sys.exit(1)


if __name__ == "__main__":
    main()
