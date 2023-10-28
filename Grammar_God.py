import tkinter as tk
from tkinter import ttk
import language_tool_python

tool = language_tool_python.LanguageTool('en-US')

class GrammarCheckerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Grammar Checker")

        self.input_text = ttk.Label(root, text="Enter your text:")
        self.input_text.pack(pady=10)
        self.input_box = tk.Text(root, height=10, width=50)
        self.input_box.pack(pady=10)

        self.check_button = ttk.Button(root, text="Check Grammar", command=self.check_grammar)
        self.check_button.pack(pady=10)

        self.suggestion_label = ttk.Label(root, text="")
        self.suggestion_label.pack(pady=10)

        self.fix_button = ttk.Button(root, text="Fix", command=self.fix_error)
        self.fix_button.pack(pady=5)

        self.skip_button = ttk.Button(root, text="Skip", command=self.skip_error)
        self.skip_button.pack(pady=5)

        self.output_section_label = ttk.Label(root, text="Output:")
        self.output_section_label.pack(pady=10)
        self.output_box = tk.Text(root, height=10, width=50)
        self.output_box.pack(pady=10)

        self.current_errors = []
        self.current_index = 0

    def check_grammar(self):
        text = self.input_box.get("1.0", tk.END)
        self.current_errors = tool.check(text)
        self.show_next_error()
        
        # Highlighting errors
        for error in self.current_errors:
            start_line, start_char = self.get_line_and_char(error.offset)
            end_line, end_char = self.get_line_and_char(error.offset + error.errorLength)
            self.input_box.tag_add("error", f"{start_line}.{start_char}", f"{end_line}.{end_char}")
        self.input_box.tag_configure("error", underline=True)
        
    

    def show_next_error(self):
        if self.current_index < len(self.current_errors):
            error = self.current_errors[self.current_index]
            self.suggestion_label.config(text=f"Error: {error.message}. Suggestion: {error.replacements[0] if error.replacements else 'None'}")
        else:
            self.suggestion_label.config(text="All errors addressed!")
            self.output_box.delete("1.0", tk.END)
            self.output_box.insert(tk.END, self.input_box.get("1.0", tk.END))
            self.input_box.tag_remove("error", "1.0", tk.END)

    def fix_error(self):
        if self.current_index < len(self.current_errors):
            error = self.current_errors[self.current_index]
            start_line, start_char = self.get_line_and_char(error.offset)
            end_line, end_char = self.get_line_and_char(error.offset + error.errorLength)
            
            if error.replacements:
                self.input_box.delete(f"{start_line}.{start_char}", f"{end_line}.{end_char}")
                self.input_box.insert(f"{start_line}.{start_char}", error.replacements[0])
            self.current_index += 1
            self.show_next_error()

    def get_line_and_char(self, index):
        text = self.input_box.get("1.0", tk.END)
        lines = text.split("\n")
        line_count = 0
        char_count = 0
        for line in lines:
            char_count += len(line) + 1  # +1 for the newline character
            if char_count > index:
                return line_count + 1, len(line) - (char_count - index)
            line_count += 1

    def skip_error(self):
        if self.current_index < len(self.current_errors):
            self.current_index += 1
            self.show_next_error()

if __name__ == "__main__":
    root = tk.Tk()
    app = GrammarCheckerApp(root)
    root.mainloop()
