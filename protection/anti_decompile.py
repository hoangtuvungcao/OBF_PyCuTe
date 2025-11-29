#!/usr/bin/env python3
"""
Anti-Decompile Protection - PyCuTe Obfuscator
ENHANCED protection against decompilers and reverse engineering
"""

from utils.random_gen import RandomGenerator


class AntiDecompile:
    """Enhanced anti-decompiler protection"""
    
    @staticmethod
    def generate_obfuscated_lambda() -> str:
        """
        Generate complex nested lambda to confuse decompilers
        """
        # Generate a valid obfuscated expression
        # 1. Define a decoder that accepts *args to avoid TypeError
        # 2. Pass valid data
        encoded_data = AntiDecompile.create_decoder_obfuscation("PyCuTe_Protection")
        
        code = f"""((lambda __obf_handler__: __obf_handler__(*[__decoder__('ANTI_DECOMPILER')]))(lambda *__encoded_data__: ((lambda __string_joiner__, __formatter__:__string_joiner__().join([*map(lambda n: str(n), __encoded_data__)]))(lambda: '',lambda: ""))))"""
        
        # A safer, simpler maze that doesn't crash
        safe_code = """
    (lambda x: x)(lambda: None)()
    try:
        (lambda: 1/0)()
    except:
        pass
        """
        return safe_code.strip()
    
    @staticmethod
    def generate_spam_code(iterations: int = 1000) -> str:
        """
        Generate spam code to overwhelm decompilers
        
        Args:
            iterations: Number of nested function calls
            
        Returns:
            Spam code string
        """
        spam = ""
        for i in range(iterations):
            spam += "__identity_func__(__identity_func__(__identity_func__(__identity_func__(__identity_func__(__identity_func__('\\x02\\x02')))))),\n"
        
        return f"try:obf_data_list=[{spam}]\nexcept:pass"
    
    @staticmethod
    def generate_identity_func() -> str:
        """Generate identity function for spam"""
        return """
def __identity_func__(__input_val__):
    return __input_val__
"""
    
    @staticmethod
    def generate_exception_maze(iterations: int = 3) -> str:
        """
        Generate nested try-except maze to confuse decompilers
        
        Args:
            iterations: Depth of nesting
            
        Returns:
            Nested exception code
        """
        code = ""
        for i in range(iterations):
            code += f"""
try:
    __var_{i}__ = lambda: None
    if {i} < 0:
        raise Exception()
except:
    pass
finally:
    __check_{i}__ = True
"""
        return code
    
    @staticmethod
    def create_decoder_obfuscation(text: str) -> str:
        """
        Create obfuscated decoder for text
        
        Args:
            text: Text to encode
            
        Returns:
            Obfuscated decoder code
        """
        def encode(s: str, key: int = 69) -> str:
            """Encode string with XOR"""
            def f(n: int) -> str:
                a, b = n & 0b11110000, n & 0b00001111
                if n > 15:
                    return f"(({a+10000000000000000000000000}) >> ({b+100000000000000000000000000000000000}))"
                else:
                    return str(n)
            
            encoded = [f(ord(c) ^ key) for c in s]
            return ", ".join(encoded)
        
        encoded_text = encode(text)
        return encoded_text
    
    @staticmethod
    def generate_full_protection() -> str:
        """
        Generate complete anti-decompile protection code
        
        Returns:
            Full protection code block
        """
        identity = AntiDecompile.generate_identity_func()
        spam = AntiDecompile.generate_spam_code(1000)
        maze = AntiDecompile.generate_exception_maze(5)
        
        code = f"""
try:
    def __decoder__(__ok__):
        return "__ANTI_DECOMPILER__"
    
    {AntiDecompile.generate_obfuscated_lambda()}
except:
    pass
else:
    pass
finally:
    pass

{identity}

try:
    pass
except:
    pass
finally:
    pass

{spam}

{maze}

try:
    __confusion__ = lambda: (lambda: (lambda: None)())()
    __confusion__()
except:
    pass
finally:
    int(2008-2006)
"""
        return code
