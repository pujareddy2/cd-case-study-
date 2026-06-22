import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os

class CompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Compiler Design - Case Study 2")
        self.root.geometry("1000x700")

        top_frame = tk.Frame(root)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        self.btn_load = tk.Button(top_frame, text="Load Source File", command=self.load_file)
        self.btn_load.pack(side=tk.LEFT, padx=5)

        self.btn_compile = tk.Button(top_frame, text="Run Compiler", command=self.run_compiler)
        self.btn_compile.pack(side=tk.LEFT, padx=5)
        
        self.lbl_file = tk.Label(top_frame, text="No file selected")
        self.lbl_file.pack(side=tk.LEFT, padx=10)

        paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left_frame = tk.Frame(paned_window)
        paned_window.add(left_frame, minsize=300)
        
        tk.Label(left_frame, text="Source Code").pack(anchor=tk.W)
        self.txt_source = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, width=40, height=30)
        self.txt_source.pack(fill=tk.BOTH, expand=True)

        from tkinter import ttk
        self.notebook = ttk.Notebook(paned_window)
        paned_window.add(self.notebook, minsize=500)

        self.txt_tac = scrolledtext.ScrolledText(self.notebook, wrap=tk.WORD)
        self.notebook.add(self.txt_tac, text="Original TAC")

        self.txt_bb = scrolledtext.ScrolledText(self.notebook, wrap=tk.WORD)
        self.notebook.add(self.txt_bb, text="Basic Blocks")

        self.txt_cfg = scrolledtext.ScrolledText(self.notebook, wrap=tk.WORD)
        self.notebook.add(self.txt_cfg, text="CFG (Text & DOT)")

        self.txt_opt = scrolledtext.ScrolledText(self.notebook, wrap=tk.WORD)
        self.notebook.add(self.txt_opt, text="Optimized TAC")
        
        self.txt_raw = scrolledtext.ScrolledText(self.notebook, wrap=tk.WORD)
        self.notebook.add(self.txt_raw, text="Raw Console Output")

        self.file_path = None

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if path:
            self.file_path = path
            self.lbl_file.config(text=os.path.basename(path))
            with open(path, 'r') as f:
                self.txt_source.delete(1.0, tk.END)
                self.txt_source.insert(tk.END, f.read())

    def run_compiler(self):
        if not self.file_path:
            messagebox.showwarning("Warning", "Please load a source file first.")
            return

        compiler_exe = "compiler.exe"
        if not os.path.exists(compiler_exe):
            messagebox.showerror("Error", f"{compiler_exe} not found. Please build the compiler first using build.bat")
            return

        try:
            result = subprocess.run([compiler_exe, self.file_path], capture_output=True, text=True, check=True)
            output = result.stdout
            
            self.txt_raw.delete(1.0, tk.END)
            self.txt_raw.insert(tk.END, output)
            
            tac_start = output.find("--- Original Three Address Code ---")
            tac_end = output.find("-----------------------------------")
            
            bb_start = output.find("--- Leaders ---")
            cfg_start = output.find("--- Control Flow Graph ---")
            opt_start = output.find("--- Optimized TAC ---")
            
            if tac_start != -1 and tac_end != -1:
                self.txt_tac.delete(1.0, tk.END)
                self.txt_tac.insert(tk.END, output[tac_start:tac_end + 35])
                
            if bb_start != -1 and cfg_start != -1:
                self.txt_bb.delete(1.0, tk.END)
                self.txt_bb.insert(tk.END, output[bb_start:cfg_start])
                
            if cfg_start != -1 and opt_start != -1:
                self.txt_cfg.delete(1.0, tk.END)
                self.txt_cfg.insert(tk.END, output[cfg_start:opt_start])
                
            if opt_start != -1:
                self.txt_opt.delete(1.0, tk.END)
                self.txt_opt.insert(tk.END, output[opt_start:])

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Execution Error", f"Compiler failed with error code {e.returncode}\n{e.stderr}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = CompilerGUI(root)
    root.mainloop()
