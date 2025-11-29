#!/usr/bin/env python3
"""
Name Mangling - PyCuTe Obfuscator
Obfuscates function and variable names
"""

import ast
from typing import Dict, Set
from utils.random_gen import RandomGenerator


class NameMangler:
    """Rename variables and functions to obfuscated names"""
    
    # Common keywords used in libraries (Tkinter, subprocess, requests, etc.)
    # These should NOT be obfuscated to prevent breaking library calls.
    COMMON_KEYWORDS = {
        'args', 'kwargs', 'self', 'cls',
        # Tkinter / GUI
        'text', 'font', 'bg', 'fg', 'bd', 'width', 'height', 'command', 'padx', 'pady',
        'relief', 'selectbackground', 'selectforeground', 'activebackground', 'activeforeground',
        'highlightbackground', 'highlightcolor', 'highlightthickness', 'justify', 'anchor',
        'fill', 'expand', 'side', 'orient', 'mode', 'value', 'variable', 'textvariable',
        'show', 'state', 'cursor', 'image', 'bitmap', 'compound', 'menu', 'tearoff',
        'accelerator', 'underline', 'overrelief', 'wraplength', 'takefocus', 'exportselection',
        'setgrid', 'title', 'geometry', 'minsize', 'maxsize', 'resizable', 'iconbitmap',
        'protocol', 'class_', 'style', 'row', 'column', 'sticky', 'colspan', 'rowspan', 'ipady', 'ipadx',
        'label', 'root', 'master', 'widget', 'callback', 'event', 'x', 'y', 'w', 'h',
        # Subprocess / System
        'stdin', 'stdout', 'stderr', 'shell', 'cwd', 'env', 'universal_newlines',
        'startupinfo', 'creationflags', 'capture_output', 'timeout', 'encoding', 'errors',
        'bufsize', 'executable', 'pass_fds', 'start_new_session', 'run', 'Popen', 'call',
        'check_output', 'pipe', 'devnull',
        # OS / Path
        'path', 'exists', 'join', 'split', 'dirname', 'basename', 'abspath', 'realpath',
        'relpath', 'splitext', 'getsize', 'isfile', 'isdir', 'walk', 'listdir', 'mkdir',
        'makedirs', 'remove', 'unlink', 'rmdir', 'rename', 'replace', 'system', 'environ',
        'sep', 'linesep', 'pathsep', 'curdir', 'pardir', 'getcwd', 'chdir',
        # Sys
        'argv', 'exit', 'modules', 'platform', 'version', 'maxsize', 'path', 'meta_path',
        # Requests / Network
        'url', 'params', 'data', 'json', 'headers', 'cookies', 'files', 'auth', 'timeout',
        'allow_redirects', 'proxies', 'verify', 'stream', 'cert', 'get', 'post', 'put', 'delete',
        'request', 'session', 'response', 'status_code', 'content', 'text',
        # Threading / Time
        'target', 'daemon', 'start', 'join', 'run', 'sleep', 'time', 'now', 'strftime',
        'strptime', 'localtime', 'gmtime',
        # Argparse
        'prog', 'usage', 'description', 'epilog', 'parents', 'formatter_class', 'prefix_chars',
        'fromfile_prefix_chars', 'argument_default', 'conflict_handler', 'add_help', 'allow_abbrev',
        'exit_on_error', 'action', 'nargs', 'const', 'default', 'type', 'choices', 'required',
        'help', 'metavar', 'dest',
        # Logging
        'debug', 'info', 'warning', 'error', 'critical', 'exception', 'log', 'getLogger',
        'basicConfig', 'FileHandler', 'StreamHandler', 'Formatter', 'level', 'handlers',
        # JSON
        'load', 'loads', 'dump', 'dumps', 'JSONDecoder', 'JSONEncoder',
        # Re (Regex)
        'search', 'match', 'findall', 'finditer', 'sub', 'subn', 'split', 'compile', 'escape',
        'group', 'groups', 'groupdict', 'start', 'end', 'span',
        # Math / Random
        'sin', 'cos', 'tan', 'sqrt', 'ceil', 'floor', 'fabs', 'factorial', 'gcd', 'log', 'log10',
        'pow', 'pi', 'e', 'inf', 'nan', 'seed', 'randint', 'choice', 'shuffle', 'sample',
        'random', 'uniform', 'randrange',
        # Datetime
        'datetime', 'date', 'time', 'timedelta', 'timezone', 'tzinfo', 'now', 'utcnow',
        'fromtimestamp', 'strptime', 'strftime', 'year', 'month', 'day', 'hour', 'minute',
        'second', 'microsecond', 'isoformat',
        # Collections / Itertools / Functools
        'deque', 'namedtuple', 'defaultdict', 'OrderedDict', 'Counter', 'chain', 'cycle',
        'repeat', 'count', 'islice', 'reduce', 'partial', 'wraps', 'lru_cache',
        # Pathlib
        'Path', 'cwd', 'home', 'stat', 'chmod', 'glob', 'rglob', 'is_dir', 'is_file',
        'is_symlink', 'is_socket', 'is_fifo', 'is_block_device', 'is_char_device',
        'mkdir', 'rmdir', 'open', 'read_bytes', 'read_text', 'write_bytes', 'write_text',
        'rename', 'replace', 'resolve', 'touch', 'unlink', 'parent', 'parents', 'name',
        'suffix', 'suffixes', 'stem', 'anchor', 'drive', 'root', 'parts',
        # Shutil
        'copy', 'copy2', 'copyfile', 'copytree', 'move', 'rmtree', 'disk_usage', 'chown',
        # Socket / Network
        'socket', 'AF_INET', 'SOCK_STREAM', 'SOCK_DGRAM', 'bind', 'listen', 'accept',
        'connect', 'send', 'recv', 'sendall', 'recvfrom', 'sendto', 'close', 'shutdown',
        'gethostname', 'gethostbyname', 'setsockopt', 'SOL_SOCKET', 'SO_REUSEADDR',
        # Urllib
        'request', 'parse', 'error', 'urlopen', 'urlretrieve', 'quote', 'unquote',
        'urlencode', 'urlparse', 'urlunparse', 'urljoin',
        # General / Builtins
        'name', 'type', 'id', 'object', 'format', 'end', 'sep', 'file', 'flush', 'open',
        'read', 'write', 'close', 'append', 'extend', 'pop', 'remove', 'clear', 'copy',
        'keys', 'values', 'items', 'get', 'update', 'len', 'str', 'int', 'float', 'bool',
        'list', 'dict', 'set', 'tuple', 'range', 'enumerate', 'zip', 'map', 'filter',
        'sorted', 'reversed', 'min', 'max', 'sum', 'any', 'all', 'print', 'input',
        'main', 'app', 'run', 'setup', 'init', 'config', 'insert', 'index', 'count'
    }

    def __init__(self, preserve_names: Set[str] = None):
        """
        Initialize name mangler
        
        Args:
            preserve_names: Names to not obfuscate (e.g., __main__, __init__)
        """
        self.preserve_names = preserve_names or set()
        # Always preserve dunder methods and common keywords
        self.preserve_names.update({"__main__", "__init__", "__name__", "__file__", "__doc__", "__module__", "__str__", "__repr__"})
        self.preserve_names.update(self.COMMON_KEYWORDS)
        
        self.name_map: Dict[str, str] = {}
    
    def should_preserve(self, name: str) -> bool:
        """Check if name should be preserved"""
        return (
            name in self.preserve_names or
            name.startswith('__') and name.endswith('__') or  # Dunder methods
            name.startswith('_')  # Private methods (optional)
        )
    
    def get_obfuscated_name(self, original_name: str) -> str:
        """
        Get or create obfuscated name
        
        Args:
            original_name: Original variable/function name
            
        Returns:
            Obfuscated name
        """
        if self.should_preserve(original_name):
            return original_name
        
        if original_name not in self.name_map:
            self.name_map[original_name] = RandomGenerator.variable_name()
        
        return self.name_map[original_name]
    
    def rename_in_tree(self, tree: ast.Module) -> ast.Module:
        """
        Rename all variables in AST tree
        
        Args:
            tree: AST tree to process
            
        Returns:
            Modified AST tree
        """
        # First pass: collect all defined names
        collector = DefinitionCollector()
        collector.visit(tree)
        
        # Second pass: rename only defined names
        renamer = _NameRenamer(self, collector.defined_names, collector.imported_names)
        return renamer.visit(tree)


class DefinitionCollector(ast.NodeVisitor):
    """Collects all names defined in the AST"""
    def __init__(self):
        self.defined_names = set()
        self.imported_names = set()

    def visit_FunctionDef(self, node):
        self.defined_names.add(node.name)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.defined_names.add(node.name)
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.defined_names.add(node.id)
        self.generic_visit(node)
    
    def visit_arg(self, node):
        self.defined_names.add(node.arg)
        
    def visit_Import(self, node):
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name.split('.')[0]
            self.defined_names.add(name)
            self.imported_names.add(name)
                
    def visit_ImportFrom(self, node):
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.defined_names.add(name)
            self.imported_names.add(name)


class _NameRenamer(ast.NodeTransformer):
    """AST transformer for renaming"""
    
    def __init__(self, mangler: NameMangler, defined_names: Set[str], imported_names: Set[str]):
        self.mangler = mangler
        self.defined_names = defined_names
        self.imported_names = imported_names
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        """Rename function definitions"""
        if node.name in self.defined_names and not self.mangler.should_preserve(node.name):
            node.name = self.mangler.get_obfuscated_name(node.name)
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:
        """Rename class definitions"""
        if node.name in self.defined_names and not self.mangler.should_preserve(node.name):
            node.name = self.mangler.get_obfuscated_name(node.name)
        self.generic_visit(node)
        return node
    
    def visit_Name(self, node: ast.Name) -> ast.Name:
        """Rename variable names"""
        if isinstance(node.ctx, (ast.Store, ast.Load)):
            if node.id in self.defined_names and not self.mangler.should_preserve(node.id):
                node.id = self.mangler.get_obfuscated_name(node.id)
        return node
    
    def visit_arg(self, node: ast.arg) -> ast.arg:
        """Rename function arguments"""
        if node.arg in self.defined_names and not self.mangler.should_preserve(node.arg):
            node.arg = self.mangler.get_obfuscated_name(node.arg)
        return node

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> ast.ExceptHandler:
        """Rename exception handler variable"""
        if node.name and node.name in self.defined_names and not self.mangler.should_preserve(node.name):
            node.name = self.mangler.get_obfuscated_name(node.name)
        self.generic_visit(node)
        return node

    def visit_Import(self, node: ast.Import) -> ast.Import:
        """Rename import aliases"""
        for alias in node.names:
            if alias.asname:
                if alias.asname in self.defined_names and not self.mangler.should_preserve(alias.asname):
                    alias.asname = self.mangler.get_obfuscated_name(alias.asname)
            else:
                # Handle imports without alias: import foo -> import foo as X
                name = alias.name.split('.')[0]
                if name in self.defined_names and not self.mangler.should_preserve(name):
                    alias.asname = self.mangler.get_obfuscated_name(name)
        return node

    def visit_ImportFrom(self, node: ast.ImportFrom) -> ast.ImportFrom:
        """Rename from-import aliases"""
        for alias in node.names:
            if alias.asname:
                if alias.asname in self.defined_names and not self.mangler.should_preserve(alias.asname):
                    alias.asname = self.mangler.get_obfuscated_name(alias.asname)
            else:
                # Handle from-imports without alias: from foo import bar -> from foo import bar as X
                if alias.name in self.defined_names and not self.mangler.should_preserve(alias.name):
                    alias.asname = self.mangler.get_obfuscated_name(alias.name)
        return node

    def visit_Attribute(self, node: ast.Attribute) -> ast.Attribute:
        """Rename attribute access"""
        # Check if we are accessing an attribute of an imported module
        # We check BEFORE visiting children to see the original name
        is_import_access = False
        if isinstance(node.value, ast.Name):
            if node.value.id in self.imported_names:
                is_import_access = True
        
        self.generic_visit(node)
        
        if is_import_access:
            return node
            
        if node.attr in self.defined_names and not self.mangler.should_preserve(node.attr):
            node.attr = self.mangler.get_obfuscated_name(node.attr)
        return node

    def visit_keyword(self, node: ast.keyword) -> ast.keyword:
        """Rename keyword arguments in calls"""
        self.generic_visit(node)
        if node.arg and node.arg in self.defined_names and not self.mangler.should_preserve(node.arg):
            node.arg = self.mangler.get_obfuscated_name(node.arg)
        return node
