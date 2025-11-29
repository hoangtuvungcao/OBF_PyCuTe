import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import sys
import os
import time
import ast
import threading
import difflib
import re

# ==============================================================================
# MODERN UI CONSTANTS
# ==============================================================================
COLORS = {
    "bg": "#121212",        # Main Background (Very Dark Grey)
    "panel": "#1E1E1E",     # Panel Background (Dark Grey)
    "fg": "#E0E0E0",        # Primary Text (Light Grey)
    "fg_dim": "#A0A0A0",    # Secondary Text (Dim Grey)
    "accent": "#00E676",    # Accent Color (Bright Green)
    "accent_hover": "#00C853",
    "info": "#2979FF",      # Info Blue
    "info_hover": "#2962FF",
    "warning": "#FFB74D",   # Warning Orange
    "warning_hover": "#FF9800",
    "error": "#FF5252",     # Error Red
    "button": "#2D2D2D",    # Button BG
    "button_hover": "#3D3D3D",
    "entry_bg": "#252525",
    "border": "#333333"
}

FONTS = {
    "header": ("Segoe UI", 18, "bold"),
    "subheader": ("Segoe UI", 12),
    "label": ("Segoe UI", 10),
    "button": ("Segoe UI", 10, "bold"),
    "console": ("Consolas", 10),
    "status": ("Segoe UI", 9)
}

class ModernButton(tk.Button):
    """Custom Button with Hover Effect"""
    def __init__(self, master, **kwargs):
        self.bg_color = kwargs.get("bg", COLORS["button"])
        self.hover_color = kwargs.get("activebackground", COLORS["button_hover"])
        
        # Remove custom args before passing to super
        if "hover_bg" in kwargs:
            self.hover_color = kwargs.pop("hover_bg")
            
        super().__init__(master, **kwargs)
        self.configure(
            relief="flat",
            bd=0,
            cursor="hand2",
            font=FONTS["button"],
            fg=COLORS["bg"] if self.bg_color in [COLORS["accent"], COLORS["info"], COLORS["warning"]] else COLORS["fg"]
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.configure(bg=self.hover_color)

    def on_leave(self, e):
        self.configure(bg=self.bg_color)

class ObfuscationQAStudio:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_ui()
        self.auto_load_files()

    def setup_window(self):
        self.root.title("Obfuscation QA Studio v6.0")
        self.root.configure(bg=COLORS["bg"])
        
        # Center the window
        width = 1100
        height = 750
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.minsize(900, 600)

    def setup_ui(self):
        # --- HEADER ---
        header = tk.Frame(self.root, bg=COLORS["panel"], height=80)
        header.pack(fill="x", pady=(0, 2))
        header.pack_propagate(False)

        # Logo/Title Area (Centered)
        title_frame = tk.Frame(header, bg=COLORS["panel"])
        title_frame.pack(expand=True)

        tk.Label(title_frame, text="🛡", font=("Segoe UI Emoji", 24), bg=COLORS["panel"], fg=COLORS["accent"]).pack(side="left", padx=10)
        
        text_frame = tk.Frame(title_frame, bg=COLORS["panel"])
        text_frame.pack(side="left")
        
        tk.Label(text_frame, text="OBFUSCATION QA STUDIO", font=FONTS["header"], bg=COLORS["panel"], fg=COLORS["fg"]).pack(anchor="w")
        tk.Label(text_frame, text="Advanced Quality Assurance & Benchmarking Tool", font=FONTS["status"], bg=COLORS["panel"], fg=COLORS["fg_dim"]).pack(anchor="w")

        # --- MAIN CONTAINER ---
        main_container = tk.Frame(self.root, bg=COLORS["bg"])
        main_container.pack(fill="both", expand=True, padx=40, pady=30)

        # --- FILE SELECTION PANEL ---
        file_panel = tk.LabelFrame(main_container, text="  TARGET FILES  ", font=FONTS["button"], 
                                  bg=COLORS["bg"], fg=COLORS["info"], bd=1, relief="solid")
        file_panel.pack(fill="x", pady=(0, 20), ipady=10)

        self.src_entry = self.create_file_row(file_panel, "Source File:", "src")
        self.obf_entry = self.create_file_row(file_panel, "Obfuscated File:", "obf")

        # --- ACTION TOOLBAR ---
        toolbar = tk.Frame(main_container, bg=COLORS["bg"])
        toolbar.pack(fill="x", pady=(0, 20))

        # Center the buttons
        btn_container = tk.Frame(toolbar, bg=COLORS["bg"])
        btn_container.pack(anchor="center")

        ModernButton(btn_container, text="🔍 CHECK SYNTAX", bg=COLORS["info"], hover_bg=COLORS["info_hover"], 
                    command=self.run_syntax_check, width=20).pack(side="left", padx=10)
        
        ModernButton(btn_container, text="🚀 RUN BENCHMARK", bg=COLORS["accent"], hover_bg=COLORS["accent_hover"], 
                    command=self.run_benchmark, width=20).pack(side="left", padx=10)
        
        ModernButton(btn_container, text="🔧 FIX ENCODING", bg=COLORS["warning"], hover_bg=COLORS["warning_hover"], 
                    command=self.fix_encoding, width=20).pack(side="left", padx=10)
        
        ModernButton(btn_container, text="🧹 CLEAR LOG", bg=COLORS["button"], hover_bg=COLORS["button_hover"], 
                    command=self.clear_log, width=15).pack(side="left", padx=10)

        # --- CONSOLE OUTPUT ---
        console_frame = tk.LabelFrame(main_container, text="  EXECUTION LOG  ", font=FONTS["button"], 
                                     bg=COLORS["bg"], fg=COLORS["fg_dim"], bd=1, relief="solid")
        console_frame.pack(fill="both", expand=True)

        self.console = scrolledtext.ScrolledText(console_frame, bg="#0F0F0F", fg="#D0D0D0",
                                                font=FONTS["console"], bd=0, padx=15, pady=15,
                                                selectbackground=COLORS["info"], selectforeground="white")
        self.console.pack(fill="both", expand=True)

        # Console Tags
        self.console.tag_config("INFO", foreground=COLORS["info"])
        self.console.tag_config("SUCCESS", foreground=COLORS["accent"])
        self.console.tag_config("ERROR", foreground=COLORS["error"])
        self.console.tag_config("WARNING", foreground=COLORS["warning"])
        self.console.tag_config("HEADER", foreground="#FFFFFF", background="#333333", justify="center")
        self.console.tag_config("TIMESTAMP", foreground=COLORS["fg_dim"])

        # --- FOOTER ---
        footer = tk.Label(self.root, text="PyCuTe Obfuscator v3.0 • Premium Edition", 
                         font=FONTS["status"], bg=COLORS["bg"], fg=COLORS["fg_dim"])
        footer.pack(side="bottom", pady=10)

    def create_file_row(self, parent, label_text, var_name):
        row = tk.Frame(parent, bg=COLORS["bg"])
        row.pack(fill="x", padx=20, pady=8)
        
        tk.Label(row, text=label_text, bg=COLORS["bg"], fg=COLORS["fg"], 
                font=FONTS["label"], width=15, anchor="w").pack(side="left")
        
        entry = tk.Entry(row, bg=COLORS["entry_bg"], fg="white", 
                        insertbackground="white", bd=0, relief="flat", font=("Consolas", 10))
        entry.pack(side="left", fill="x", expand=True, padx=10, ipady=6)
        
        ModernButton(row, text="Browse...", width=10, 
                    command=lambda: self.browse_file(entry, var_name)).pack(side="left")
        
        return entry

    def auto_load_files(self):
        if os.path.exists("src.py"):
            self.src_entry.insert(0, os.path.abspath("src.py"))
        if os.path.exists("obf_src.py"):
            self.obf_entry.insert(0, os.path.abspath("obf_src.py"))
        
        self.log("Ready. Select files or click an action to begin.", "INFO")

    def browse_file(self, entry, var_name):
        path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if path:
            entry.delete(0, tk.END)
            entry.insert(0, path)
            self.log(f"Selected {var_name.upper()}: {os.path.basename(path)}", "INFO")

    def log(self, message, tag=None):
        self.console.configure(state="normal")
        timestamp = f"[{time.strftime('%H:%M:%S')}] "
        self.console.insert(tk.END, timestamp, "TIMESTAMP")
        self.console.insert(tk.END, message + "\n", tag)
        self.console.see(tk.END)
        self.console.configure(state="disabled")

    def clear_log(self):
        self.console.configure(state="normal")
        self.console.delete(1.0, tk.END)
        self.console.configure(state="disabled")

    def run_syntax_check(self):
        threading.Thread(target=self._syntax_check_thread, daemon=True).start()

    def _syntax_check_thread(self):
        src = self.src_entry.get()
        obf = self.obf_entry.get()
        
        if not src or not obf:
            self.log("Please select both files first!", "ERROR")
            return

       # self.log("\n════════════════════════════════════════════════════════════", "HEADER")
        self.log("STARTING SYNTAX CHECK", "HEADER")
       # self.log("════════════════════════════════════════════════════════════\n", "HEADER")
        
        for label, path in [("SOURCE", src), ("OBFUSCATED", obf)]:
            self.log(f"► Checking {label}: {os.path.basename(path)}", "INFO")
            if not os.path.exists(path):
                self.log(f"  [X] File not found!", "ERROR")
                continue
                
            try:
                size = os.path.getsize(path)
                self.log(f"  • Size: {size:,} bytes", "TIMESTAMP")
                
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                ast.parse(content)
                self.log(f"  ✔ Syntax Valid", "SUCCESS")
            except SyntaxError as e:
                self.log(f"  ✘ Syntax Error: Line {e.lineno}: {e.msg}", "ERROR")
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        if 0 <= e.lineno - 1 < len(lines):
                            self.log(f"    Code: {lines[e.lineno-1].strip()}", "WARNING")
                except: pass
            except UnicodeDecodeError:
                 self.log(f"  ✘ Encoding Error: File is not valid UTF-8", "ERROR")
            except Exception as e:
                self.log(f"  ✘ Error: {str(e)}", "ERROR")
        
        self.log("\n------------------------------------------------------------", "TIMESTAMP")

    def run_benchmark(self):
        threading.Thread(target=self._benchmark_thread, daemon=True).start()

    def _benchmark_thread(self):
        src = self.src_entry.get()
        obf = self.obf_entry.get()
        
        if not src or not obf:
            self.log("Please select both files first!", "ERROR")
            return

       # self.log("\n════════════════════════════════════════════════════════════", "HEADER")
        self.log("STARTING BENCHMARK", "HEADER")
       # self.log("════════════════════════════════════════════════════════════\n", "HEADER")
        
        # Run Source
        self.log("► Running Source...", "INFO")
        src_res = self._run_script(src)
        
        if src_res['code'] != 0:
            self.log("  ✘ Source execution failed!", "ERROR")
            self.log(f"  Error: {src_res['stderr'].strip()}", "ERROR")
            return
            
        self.log(f"  ✔ Finished in {src_res['time']:.4f}s", "SUCCESS")
        
        # Run Obfuscated
        self.log("► Running Obfuscated...", "INFO")
        obf_res = self._run_script(obf)
        
        if obf_res['code'] != 0:
            self.log("  ✘ Obfuscated execution failed!", "ERROR")
            self.log(f"  Error: {obf_res['stderr'].strip()}", "ERROR")
        else:
            self.log(f"  ✔ Finished in {obf_res['time']:.4f}s", "SUCCESS")
            
        # Compare
        self.log("► Comparing Outputs...", "INFO")
        if src_res['stdout'] == obf_res['stdout']:
            self.log("  ✔ STDOUT matches perfectly!", "SUCCESS")
        else:
            self.log("  ✘ STDOUT mismatch!", "ERROR")
            s_lines = src_res['stdout'].splitlines()
            o_lines = obf_res['stdout'].splitlines()
            diff = list(difflib.unified_diff(s_lines, o_lines, fromfile='Source', tofile='Obfuscated', lineterm=''))
            if diff:
                self.log("  Differences:", "WARNING")
                for line in diff[:5]:
                    self.log(f"    {line}", "WARNING")
                if len(diff) > 5:
                    self.log("    ... (more differences)", "WARNING")
            
    def _run_script(self, path):
        start = time.time()
        try:
            # Force Python to use UTF-8 for IO to avoid encoding issues on Windows consoles
            env = os.environ.copy()
            env["PYTHONUTF8"] = "1"
            
            proc = subprocess.run(
                [sys.executable, path], 
                capture_output=True, 
                text=True, 
                timeout=5, 
                encoding='utf-8', 
                errors='replace',  # Use replace to avoid crashing on bad output
                env=env
            )
            return {
                "code": proc.returncode,
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "time": time.time() - start
            }
        except subprocess.TimeoutExpired:
            return {"code": -1, "stdout": "", "stderr": "Timeout", "time": 5.0}
        except Exception as e:
            return {"code": -1, "stdout": "", "stderr": str(e), "time": 0}

    def fix_encoding(self):
        obf = self.obf_entry.get()
        ModernButton(btn_container, text="🧹 CLEAR LOG", bg=COLORS["button"], hover_bg=COLORS["button_hover"], 
                    command=self.clear_log, width=15).pack(side="left", padx=10)

        # --- CONSOLE OUTPUT ---
        console_frame = tk.LabelFrame(main_container, text="  EXECUTION LOG  ", font=FONTS["button"], 
                                     bg=COLORS["bg"], fg=COLORS["fg_dim"], bd=1, relief="solid")
        console_frame.pack(fill="both", expand=True)

        self.console = scrolledtext.ScrolledText(console_frame, bg="#0F0F0F", fg="#D0D0D0",
                                                font=FONTS["console"], bd=0, padx=15, pady=15,
                                                selectbackground=COLORS["info"], selectforeground="white")
        self.console.pack(fill="both", expand=True)

        # Console Tags
        self.console.tag_config("INFO", foreground=COLORS["info"])
        self.console.tag_config("SUCCESS", foreground=COLORS["accent"])
        self.console.tag_config("ERROR", foreground=COLORS["error"])
        self.console.tag_config("WARNING", foreground=COLORS["warning"])
        self.console.tag_config("HEADER", foreground="#FFFFFF", background="#333333", justify="center")
        self.console.tag_config("TIMESTAMP", foreground=COLORS["fg_dim"])

        # --- FOOTER ---
        footer = tk.Label(self.root, text="PyCuTe Obfuscator v3.0 • Premium Edition", 
                         font=FONTS["status"], bg=COLORS["bg"], fg=COLORS["fg_dim"])
        footer.pack(side="bottom", pady=10)

    def create_file_row(self, parent, label_text, var_name):
        row = tk.Frame(parent, bg=COLORS["bg"])
        row.pack(fill="x", padx=20, pady=8)
        
        tk.Label(row, text=label_text, bg=COLORS["bg"], fg=COLORS["fg"], 
                font=FONTS["label"], width=15, anchor="w").pack(side="left")
        
        entry = tk.Entry(row, bg=COLORS["entry_bg"], fg="white", 
                        insertbackground="white", bd=0, relief="flat", font=("Consolas", 10))
        entry.pack(side="left", fill="x", expand=True, padx=10, ipady=6)
        
        ModernButton(row, text="Browse...", width=10, 
                    command=lambda: self.browse_file(entry, var_name)).pack(side="left")
        
        return entry

    def auto_load_files(self):
        if os.path.exists("src.py"):
            self.src_entry.insert(0, os.path.abspath("src.py"))
        if os.path.exists("obf_src.py"):
            self.obf_entry.insert(0, os.path.abspath("obf_src.py"))
        
        self.log("Ready. Select files or click an action to begin.", "INFO")

    def browse_file(self, entry, var_name):
        path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if path:
            entry.delete(0, tk.END)
            entry.insert(0, path)
            self.log(f"Selected {var_name.upper()}: {os.path.basename(path)}", "INFO")

    def log(self, message, tag=None):
        self.console.configure(state="normal")
        timestamp = f"[{time.strftime('%H:%M:%S')}] "
        self.console.insert(tk.END, timestamp, "TIMESTAMP")
        self.console.insert(tk.END, message + "\n", tag)
        self.console.see(tk.END)
        self.console.configure(state="disabled")

    def clear_log(self):
        self.console.configure(state="normal")
        self.console.delete(1.0, tk.END)
        self.console.configure(state="disabled")

    def run_syntax_check(self):
        threading.Thread(target=self._syntax_check_thread, daemon=True).start()

    def _syntax_check_thread(self):
        src = self.src_entry.get()
        obf = self.obf_entry.get()
        
        if not src or not obf:
            self.log("Please select both files first!", "ERROR")
            return

       # self.log("\n════════════════════════════════════════════════════════════", "HEADER")
        self.log("STARTING SYNTAX CHECK", "HEADER")
       # self.log("════════════════════════════════════════════════════════════\n", "HEADER")
        
        for label, path in [("SOURCE", src), ("OBFUSCATED", obf)]:
            self.log(f"► Checking {label}: {os.path.basename(path)}", "INFO")
            if not os.path.exists(path):
                self.log(f"  [X] File not found!", "ERROR")
                continue
                
            try:
                size = os.path.getsize(path)
                self.log(f"  • Size: {size:,} bytes", "TIMESTAMP")
                
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                ast.parse(content)
                self.log(f"  ✔ Syntax Valid", "SUCCESS")
            except SyntaxError as e:
                self.log(f"  ✘ Syntax Error: Line {e.lineno}: {e.msg}", "ERROR")
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        if 0 <= e.lineno - 1 < len(lines):
                            self.log(f"    Code: {lines[e.lineno-1].strip()}", "WARNING")
                except: pass
            except UnicodeDecodeError:
                 self.log(f"  ✘ Encoding Error: File is not valid UTF-8", "ERROR")
            except Exception as e:
                self.log(f"  ✘ Error: {str(e)}", "ERROR")
        
        self.log("\n------------------------------------------------------------", "TIMESTAMP")

    def run_benchmark(self):
        threading.Thread(target=self._benchmark_thread, daemon=True).start()

    def _benchmark_thread(self):
        src = self.src_entry.get()
        obf = self.obf_entry.get()
        
        if not src or not obf:
            self.log("Please select both files first!", "ERROR")
            return

       # self.log("\n════════════════════════════════════════════════════════════", "HEADER")
        self.log("STARTING BENCHMARK", "HEADER")
       # self.log("════════════════════════════════════════════════════════════\n", "HEADER")
        
        # Run Source
        self.log("► Running Source...", "INFO")
        src_res = self._run_script(src)
        
        if src_res['code'] != 0:
            self.log("  ✘ Source execution failed!", "ERROR")
            self.log(f"  Error: {src_res['stderr'].strip()}", "ERROR")
            return
            
        self.log(f"  ✔ Finished in {src_res['time']:.4f}s", "SUCCESS")
        
        # Run Obfuscated
        self.log("► Running Obfuscated...", "INFO")
        obf_res = self._run_script(obf)
        
        if obf_res['code'] != 0:
            self.log("  ✘ Obfuscated execution failed!", "ERROR")
            self.log(f"  Error: {obf_res['stderr'].strip()}", "ERROR")
        else:
            self.log(f"  ✔ Finished in {obf_res['time']:.4f}s", "SUCCESS")
            
        # Compare
        self.log("► Comparing Outputs...", "INFO")
        if src_res['stdout'] == obf_res['stdout']:
            self.log("  ✔ STDOUT matches perfectly!", "SUCCESS")
        else:
            self.log("  ✘ STDOUT mismatch!", "ERROR")
            s_lines = src_res['stdout'].splitlines()
            o_lines = obf_res['stdout'].splitlines()
            diff = list(difflib.unified_diff(s_lines, o_lines, fromfile='Source', tofile='Obfuscated', lineterm=''))
            if diff:
                self.log("  Differences:", "WARNING")
                for line in diff[:5]:
                    self.log(f"    {line}", "WARNING")
                if len(diff) > 5:
                    self.log("    ... (more differences)", "WARNING")
            
    def _run_script(self, path):
        start = time.time()
        try:
            # Force Python to use UTF-8 for IO to avoid encoding issues on Windows consoles
            env = os.environ.copy()
            env["PYTHONUTF8"] = "1"
            
            proc = subprocess.run(
                [sys.executable, path], 
                capture_output=True, 
                text=True, 
                timeout=5, 
                encoding='utf-8', 
                errors='replace',  # Use replace to avoid crashing on bad output
                env=env
            )
            return {
                "code": proc.returncode,
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "time": time.time() - start
            }
        except subprocess.TimeoutExpired:
            return {"code": -1, "stdout": "", "stderr": "Timeout", "time": 5.0}
        except Exception as e:
            return {"code": -1, "stdout": "", "stderr": str(e), "time": 0}

    def fix_encoding(self):
        obf = self.obf_entry.get()
        if not obf or not os.path.exists(obf):
            self.log("Select a valid obfuscated file first.", "ERROR")
            return
            
        self.log(f"Attempting to fix encoding for {os.path.basename(obf)}...", "WARNING")
        try:
            # Read as binary to handle BOM and raw bytes
            with open(obf, "rb") as f:
                raw = f.read()
            
            # Strip UTF-8 BOM if present
            if raw.startswith(b'\xef\xbb\xbf'):
                raw = raw[3:]
            
            # Decode with replacement to fix "Non-UTF-8 code" errors
            content = raw.decode("utf-8", errors="replace")
            lines = content.splitlines()
            
            # Prepare the standard header
            std_header = "# -*- coding: utf-8 -*-"
            
            # Check for existing coding header in first 2 lines
            header_idx = -1
            for i in range(min(2, len(lines))):
                if re.search(r"coding[:=]\s*([-\w.]+)", lines[i]):
                    header_idx = i
                    break
            
            if header_idx != -1:
                # Replace existing header to ensure it's correct
                lines[header_idx] = std_header
            else:
                # Insert new header
                if len(lines) > 0 and lines[0].startswith("#!"):
                    # Insert after shebang
                    lines.insert(1, std_header)
                else:
                    # Insert at top
                    lines.insert(0, std_header)
            
            # Reconstruct content
            new_content = "\n".join(lines)
            
            # Write back as clean UTF-8
            with open(obf, "w", encoding="utf-8") as f:
                f.write(new_content)
                
            self.log("✔ File re-saved as UTF-8 with coding header", "SUCCESS")
            self.log("Try running Syntax Check again.", "INFO")
        except Exception as e:
            self.log(f"Failed to fix: {e}", "ERROR")

if __name__ == "__main__":
    root = tk.Tk()
    app = ObfuscationQAStudio(root)
    root.mainloop()