import tkinter as tk
from tkinter import ttk, messagebox
import cmath
import math

class NAFFYComplexCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Complex Number Calculator")
        self.root.geometry("800x600")
        self.root.configure(bg='#2b2b2b')
        
        self.current_expression = ""
        self.result_display = ""
        self.memory = 0+0j
        
        # Styling
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Arial', 12), borderwidth=1)
        self.style.configure('TLabel', background='#2b2b2b', foreground='white')
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Display frame
        display_frame = ttk.Frame(main_frame)
        display_frame.grid(row=0, column=0, columnspan=4, pady=(0, 10), sticky=(tk.W, tk.E))
        
        # Expression display
        self.expression_var = tk.StringVar()
        expression_label = ttk.Label(display_frame, 
                                    textvariable=self.expression_var,
                                    font=('Arial', 14),
                                    anchor='e',
                                    background='#1e1e1e',
                                    foreground='#888',
                                    padding=(10, 5))
        expression_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Result display
        self.result_var = tk.StringVar(value="0")
        result_label = ttk.Label(display_frame,
                                textvariable=self.result_var,
                                font=('Arial', 24, 'bold'),
                                anchor='e',
                                background='#1e1e1e',
                                foreground='white',
                                padding=(10, 15))
        result_label.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Button layout
        buttons = [
            # Row 1
            ['MC', 'MR', 'M+', 'M-', 'C', '⌫', '(', ')'],
            # Row 2
            ['x²', '√', '|z|', '∠', '7', '8', '9', '÷'],
            # Row 3
            ['xʸ', 'eˣ', 'ln', 'log', '4', '5', '6', '×'],
            # Row 4
            ['sin', 'cos', 'tan', 'π', '1', '2', '3', '-'],
            # Row 5
            ['sinh', 'cosh', 'tanh', 'i', '0', '.', '=', '+'],
            # Row 6
            ['1/z', 'conj', 'Re', 'Im', '±', 'j', 'ENG', 'Sci']
        ]
        
        # Special buttons with different colors
        special_buttons = ['C', '⌫', '=', 'MC', 'MR', 'M+', 'M-']
        function_buttons = ['x²', '√', '|z|', '∠', 'xʸ', 'eˣ', 'ln', 'log', 
                           'sin', 'cos', 'tan', 'sinh', 'cosh', 'tanh', 
                           '1/z', 'conj', 'Re', 'Im', '±', 'ENG', 'Sci']
        
        for row_idx, row in enumerate(buttons):
            for col_idx, text in enumerate(row):
                # Determine button style
                if text in special_buttons:
                    bg_color = '#ff9500'
                    fg_color = 'white'
                elif text in function_buttons:
                    bg_color = '#505050'
                    fg_color = 'white'
                else:
                    bg_color = '#d4d4d2'
                    fg_color = 'black'
                
                btn = tk.Button(buttons_frame,
                              text=text,
                              font=('Arial', 12, 'bold'),
                              bg=bg_color,
                              fg=fg_color,
                              activebackground='#666',
                              activeforeground=fg_color,
                              borderwidth=0,
                              height=2,
                              width=6,
                              command=lambda t=text: self.button_click(t))
                btn.grid(row=row_idx, column=col_idx, padx=2, pady=2, sticky=(tk.W, tk.E))
        
        # Configure button frame columns
        for i in range(8):
            buttons_frame.columnconfigure(i, weight=1)
    
    def parse_complex(self, text):
        """Parse complex number from text input"""
        try:
            # Remove any spaces
            text = text.replace(' ', '')
            
            # Handle j notation (engineering)
            if 'j' in text:
                text = text.replace('j', 'i')
            
            # Handle simple numbers
            if text.replace('.', '').replace('-', '').isdigit():
                return float(text) + 0j
            
            # Handle complex numbers in a+bi format
            if '+' in text or '-' in text[1:]:
                # Find the imaginary part
                if 'i' in text:
                    parts = text.replace('i', '').split('+')
                    if len(parts) == 2:
                        return complex(float(parts[0]), float(parts[1]))
                    else:
                        # Handle a-bi format
                        if '-' in text[1:]:
                            idx = text[1:].find('-') + 1
                            real = float(text[:idx])
                            imag = float(text[idx:-1].replace('i', ''))
                            return complex(real, imag)
                return complex(text)
            return complex(text)
        except:
            return None
    
    def format_complex(self, num):
        """Format complex number for display"""
        if isinstance(num, (int, float)):
            return f"{num:.10g}"
        
        real = num.real
        imag = num.imag
        
        if imag == 0:
            return f"{real:.10g}"
        elif real == 0:
            return f"{imag:.10g}i"
        else:
            sign = '+' if imag >= 0 else '-'
            return f"{real:.10g} {sign} {abs(imag):.10g}i"
    
    def button_click(self, button_text):
        """Handle button clicks"""
        operations = {
            'C': self.clear,
            '⌫': self.backspace,
            '=': self.calculate,
            '±': self.toggle_sign,
            'i': self.add_imaginary_unit,
            'j': self.add_imaginary_unit,
            'π': self.add_pi,
            '.': self.add_decimal,
            'ENG': self.toggle_engineering,
            'Sci': self.toggle_scientific
        }
        
        # Memory operations
        if button_text in ['MC', 'MR', 'M+', 'M-']:
            self.memory_operation(button_text)
            return
        
        # Special operations
        if button_text in operations:
            operations[button_text]()
            return
        
        # Mathematical functions
        if button_text in ['x²', '√', '|z|', '∠', 'xʸ', 'eˣ', 'ln', 'log',
                          'sin', 'cos', 'tan', 'sinh', 'cosh', 'tanh',
                          '1/z', 'conj', 'Re', 'Im']:
            self.apply_function(button_text)
            return
        
        # Regular numbers and operators
        if button_text in '0123456789':
            self.add_number(button_text)
        elif button_text in '+-×÷()':
            self.add_operator(button_text)
    
    def clear(self):
        """Clear the calculator"""
        self.current_expression = ""
        self.result_display = "0"
        self.update_display()
    
    def backspace(self):
        """Remove last character"""
        if self.current_expression:
            self.current_expression = self.current_expression[:-1]
            self.update_display()
    
    def add_number(self, num):
        """Add number to expression"""
        self.current_expression += num
        self.update_display()
    
    def add_operator(self, op):
        """Add operator to expression"""
        # Replace × and ÷ with * and /
        if op == '×':
            op = '*'
        elif op == '÷':
            op = '/'
        
        self.current_expression += op
        self.update_display()
    
    def add_imaginary_unit(self):
        """Add imaginary unit i or j"""
        self.current_expression += 'i'
        self.update_display()
    
    def add_pi(self):
        """Add π constant"""
        self.current_expression += str(math.pi)
        self.update_display()
    
    def add_decimal(self):
        """Add decimal point"""
        self.current_expression += '.'
        self.update_display()
    
    def toggle_sign(self):
        """Toggle sign of the current number"""
        if self.current_expression:
            # Simple implementation - add minus sign
            self.current_expression = '-' + self.current_expression
            self.update_display()
    
    def memory_operation(self, operation):
        """Handle memory operations"""
        try:
            current_value = self.parse_complex(self.result_display)
            if current_value is None:
                return
                
            if operation == 'MC':
                self.memory = 0+0j
            elif operation == 'MR':
                self.current_expression = self.format_complex(self.memory)
                self.update_display()
            elif operation == 'M+':
                self.memory += current_value
            elif operation == 'M-':
                self.memory -= current_value
        except:
            pass
    
    def apply_function(self, func):
        """Apply mathematical function to current result"""
        try:
            current_value = self.parse_complex(self.result_display)
            if current_value is None:
                return
            
            result = None
            
            if func == 'x²':
                result = current_value ** 2
            elif func == '√':
                result = cmath.sqrt(current_value)
            elif func == '|z|':
                result = abs(current_value)
            elif func == '∠':
                result = cmath.phase(current_value)
            elif func == 'eˣ':
                result = cmath.exp(current_value)
            elif func == 'ln':
                result = cmath.log(current_value)
            elif func == 'log':
                result = cmath.log10(current_value)
            elif func == 'sin':
                result = cmath.sin(current_value)
            elif func == 'cos':
                result = cmath.cos(current_value)
            elif func == 'tan':
                result = cmath.tan(current_value)
            elif func == 'sinh':
                result = cmath.sinh(current_value)
            elif func == 'cosh':
                result = cmath.cosh(current_value)
            elif func == 'tanh':
                result = cmath.tanh(current_value)
            elif func == '1/z':
                result = 1 / current_value
            elif func == 'conj':
                result = current_value.conjugate()
            elif func == 'Re':
                result = current_value.real
            elif func == 'Im':
                result = current_value.imag
            
            if result is not None:
                self.result_display = self.format_complex(result)
                self.current_expression = self.result_display
                self.update_display()
        except Exception as e:
            self.show_error(f"Error applying {func}: {str(e)}")
    
    def calculate(self):
        """Calculate the expression"""
        try:
            # Prepare expression for eval
            expr = self.current_expression
            
            # Replace display operators with Python operators
            expr = expr.replace('×', '*').replace('÷', '/')
            
            # Handle special constants
            expr = expr.replace('π', str(math.pi))
            
            # Use cmath functions for complex operations
            # Note: In production, use a safer evaluation method
            safe_dict = {
                'abs': abs,
                'sqrt': cmath.sqrt,
                'exp': cmath.exp,
                'log': cmath.log,
                'log10': cmath.log10,
                'sin': cmath.sin,
                'cos': cmath.cos,
                'tan': cmath.tan,
                'sinh': cmath.sinh,
                'cosh': cmath.cosh,
                'tanh': cmath.tanh,
                'phase': cmath.phase,
                'polar': cmath.polar,
                'rect': cmath.rect
            }
            
            # Evaluate the expression
            result = eval(expr, {"__builtins__": {}}, safe_dict)
            
            # Format and display result
            self.result_display = self.format_complex(result)
            self.current_expression = self.result_display
            self.update_display()
            
        except Exception as e:
            self.show_error(f"Calculation error: {str(e)}")
    
    def toggle_engineering(self):
        """Toggle engineering notation (not fully implemented)"""
        messagebox.showinfo("Info", "Engineering notation toggle - placeholder")
    
    def toggle_scientific(self):
        """Toggle scientific notation (not fully implemented)"""
        messagebox.showinfo("Info", "Scientific notation toggle - placeholder")
    
    def update_display(self):
        """Update the display"""
        self.expression_var.set(self.current_expression)
        self.result_var.set(self.result_display)
    
    def show_error(self, message):
        """Show error message"""
        messagebox.showerror("Error", message)
        self.clear()

def main():
    root = tk.Tk()
    app = ComplexCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()