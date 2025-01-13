from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                           QPushButton, QLineEdit, QLabel, QFrame, QTextEdit,
                           QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QTextCursor
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from Styles.index import styles

class FunctionListWidget(QScrollArea):
    def __init__(self, plotter, currentTheme):
        super().__init__()
        self.plotter = plotter
    
        self.function_widgets = {}
        self.setStyleSheet(f"""
        FunctionListWidget QWidget {{
            background-color: {currentTheme['program']['log-area']['background']};
            }}
        FunctionListWidget QScrollArea {{
            border:none;
        }}
        
""")
        container = QWidget()
        self.layout = QVBoxLayout()
        container.setLayout(self.layout)
        
        self.setWidget(container)
        self.setWidgetResizable(True)
        
    def add_function(self, index, expression):
        function_widget = QWidget()
        layout = QHBoxLayout()
        function_widget.setLayout(layout)
        
        label = QLabel(f"Hàm số: {expression}")
        label.setStyleSheet("color: blue;")
        
        delete_button = QPushButton("Xóa")
        delete_button.setStyleSheet(f"""
            QPushButton {{
                font-size: 13px;                      
                padding: 8px;                       
                border: 2px solid transparent;      
                border-radius: 5px;               
                background-color: #D70808;       
                color: #ffffff;     
            }}

            QPushButton:hover {{
                background-color: #B60707;
            }}
                                    """)
        delete_button.index = index
        delete_button.expression = expression
        delete_button.clicked.connect(self.delete_function)
        
        layout.addWidget(label)
        layout.addWidget(delete_button)
        
        self.function_widgets[index] = function_widget
        
        self.layout.addWidget(function_widget)
        
    def delete_function(self):
        delete_button = self.sender()
        if not delete_button:
            return
            
        index = delete_button.index
        expression = delete_button.expression
        
        if index in self.function_widgets:
            # Remove widget
            widget = self.function_widgets[index]
            self.layout.removeWidget(widget)
            widget.deleteLater()
            del self.function_widgets[index]
            
            self.plotter.delete_plot(index, expression)
            
            self.update_indexes(index)
    
    def update_indexes(self, deleted_index):
        indexes_to_update = sorted([i for i in self.function_widgets.keys() if i > deleted_index])
        
        for old_index in indexes_to_update:
            widget = self.function_widgets[old_index]
            new_index = old_index - 1
            
            for child in widget.children():
                if isinstance(child, QPushButton):
                    child.index = new_index
            
            self.function_widgets[new_index] = widget
            del self.function_widgets[old_index]
class LogArea(QTextEdit):
    def __init__(self, plotter, currentTheme):
        super().__init__()
        self.plotter = plotter
        self.setReadOnly(True)
        self.setStyleSheet(styles(currentTheme, 'log_area'))

    def log_message(self, message, color = 'black', is_error=False):
        self.append(f'<span style="color: {color};">{message}</span>')

class vedothi(QWidget):
    def __init__(self, parent_layout, currentTheme):
        super().__init__()
        self.plots = []

        self.theme = currentTheme
        
        container = QWidget()
        container_layout = QHBoxLayout()
        container.setLayout(container_layout)
        
        self.setup_ui(container_layout)
        parent_layout.addWidget(container)
        
    def setup_ui(self, container_layout):
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)
        
        self.create_web_view(left_layout)
        
        input_layout = QGridLayout()
        
        self.function_label = QLabel("f(x):")
        self.function_entry = QLineEdit()
        self.function_entry.setFocus()
        self.function_entry.setPlaceholderText('Nhập hàm số...')
        self.function_entry.setStyleSheet(styles(self.theme, 'input'))
        self.function_entry.textChanged.connect(self.update_latex_preview)

        self.solve_button = QPushButton("Giải")
        self.solve_button.setStyleSheet(styles(self.theme, 'submit'))
        self.solve_button.clicked.connect(self.solve_and_plot_function)
        
        input_layout.addWidget(self.function_label, 0, 0)
        input_layout.addWidget(self.function_entry, 0, 1)
        input_layout.addWidget(self.solve_button, 1, 0, 1, 2)
        
        left_layout.addLayout(input_layout)
        
        keyboard_widget = self.create_virtual_keyboard()
        left_layout.addWidget(keyboard_widget)
        
        left_layout.addWidget(QLabel("Log:"))
        self.log_area = LogArea(self, self.theme)
        self.log_area.setMinimumHeight(70)
        left_layout.addWidget(self.log_area)
        
        left_layout.addStretch()
        
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)
        
        plot_widget = QWidget()
        plot_layout = QVBoxLayout()
        plot_widget.setLayout(plot_layout)
        self.create_plot_area(plot_layout)
        right_layout.addWidget(plot_widget, 2)
        
        function_list_widget = QWidget()
        function_list_layout = QVBoxLayout()
        function_list_widget.setLayout(function_list_layout)
        
        function_list_label = QLabel("Danh sách hàm số:")
        function_list_layout.addWidget(function_list_label)
        
        self.function_list = FunctionListWidget(self, self.theme)
        function_list_layout.addWidget(self.function_list)
        
        right_layout.addWidget(function_list_widget, 1)
        
        container_layout.addWidget(left_widget, 1)
        container_layout.addWidget(right_widget, 2)

    def create_web_view(self, layout):
        self.web_view = QWebEngineView()
        self.web_view.setFixedHeight(40)
        self.web_view.setHtml("""
        <html>
        <head>
            <style>
                #MathJax_Message {
                    display: none;
                }
                body {
                    margin: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }
                #output {
                    text-align: center;
                }
            </style>
            <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML"></script>
        </head>
        <body>
            <div id="output"></div>
            <script>
                function updateMath(latex) {
                    document.getElementById('output').innerHTML = '$$' + latex + '$$';
                    MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
                }
            </script>
        </body>
        </html>
        """)
        layout.addWidget(self.web_view)
    def update_latex_preview(self):
        expression = self.function_entry.text()
        if not expression:
            self.web_view.page().runJavaScript(f"updateMath('')")
            return

        try:
            def convert_fraction(expr):
                if '/' not in expr:
                    return expr
                    
                div_index = expr.find('/')
                
                left = div_index - 1
                brackets = 0
                power_mode = False
                while left >= 0:
                    if expr[left] == ')':
                        brackets += 1
                    elif expr[left] == '(':
                        brackets -= 1
                    elif expr[left] == '^':
                        power_mode = True
                    elif power_mode and expr[left].isdigit():
                        pass
                    elif power_mode:
                        power_mode = False
                        
                    if brackets == 0 and not power_mode and (left == 0 or expr[left-1] in '+-*/'):
                        break
                    left -= 1
                numerator = expr[left:div_index]
                
                right = div_index + 1
                brackets = 0
                while right < len(expr):
                    if expr[right] == '(':
                        brackets += 1
                    elif expr[right] == ')':
                        brackets -= 1
                    if brackets == 0 and (right == len(expr)-1 or expr[right+1] in '+-*/'):
                        right += 1
                        break
                    right += 1
                denominator = expr[div_index+1:right]

                numerator = numerator.strip('()')
                denominator = denominator.strip('()')
                
                before = expr[:left]
                after = expr[right:]
                return before + r'\\frac{' + numerator + '}{' + denominator + '}' + after

            while '/' in expression:
                expression = convert_fraction(expression)

            expression = (expression
                .replace('×', r'*')
                .replace('√', r'\\sqrt')
                .replace('*', '')
                .replace('sin(', r'\\sin(')
                .replace('cos(', r'\\cos(')
                .replace('tan(', r'\\tan(')
                .replace('pi', r'\\pi')
                .replace('×10^(', r'\\times 10^{')
                .replace('^2', r'^{2}')
                .replace('^3', r'^{3}')
                .replace('^(', '^{')
                .replace('(', '{')
                .replace(')', '}')
            )

            count_open = expression.count('{')
            count_close = expression.count('}')
            if count_open > count_close:
                expression += '}' * (count_open - count_close)
                
            self.web_view.page().runJavaScript(f"updateMath('{expression}')")
        except Exception as e:
            print("Error:", str(e))
            self.web_view.page().runJavaScript(f"updateMath('{expression}')")
    def on_keyboard_click(self, key):
        cursor_pos = self.function_entry.cursorPosition()
        current_text = self.function_entry.text()
        
        if key == 'Clear':
            self.function_entry.clear()
        elif key == 'Backspace':
            if cursor_pos > 0:
                new_text = current_text[:cursor_pos-1] + current_text[cursor_pos:]
                self.function_entry.setText(new_text)
                self.function_entry.setCursorPosition(cursor_pos-1)
        elif key == '←':
            self.function_entry.setCursorPosition(max(0, cursor_pos - 1))
        elif key == '→':
            self.function_entry.setCursorPosition(min(len(current_text), cursor_pos + 1))
        elif key == 'a²':
            self.function_entry.insert('^2')
        elif key == 'a³':
            self.function_entry.insert('^3')
        else:
            self.function_entry.insert(key)

    def create_virtual_keyboard(self):
        keyboard_widget = QWidget()
        keyboard_layout = QGridLayout()
        keyboard_widget.setLayout(keyboard_layout)
        
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('×', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('x', 3, 2), ('+', 3, 3),
            ('sin(', 4, 0), ('cos(', 4, 1), ('tan(', 4, 2), ('Clear', 4, 3),
            ('(', 5, 0), (')', 5, 1), ('^(', 5, 2), ('Backspace', 5, 3),
            ('←', 6, 0), ('→', 6, 1), ('pi', 6, 2), ('e', 6, 3),
            ('√(', 7, 0), ('×10^(', 7, 1), ('a²', 7, 2), ('a³', 7, 3),
        ]
        
        for text, row, col in buttons:
            button = QPushButton(text)
            button.setStyleSheet(styles(self.theme, 'button'))
            button.clicked.connect(lambda checked, t=text: self.on_keyboard_click(t))
            button.setMinimumSize(50, 30)
            keyboard_layout.addWidget(button, row, col)
            
        return keyboard_widget
        
    def create_plot_area(self, layout):
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        self.ax.axhline(0, color='black', linewidth=0.5)
        self.ax.axvline(0, color='black', linewidth=0.5)
        self.ax.grid(True)
        
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
            
    def solve_and_plot_function(self):
        expression_str = self.function_entry.text()
        if not expression_str:
            self.log_area.log_message("Vui lòng nhập hàm số!", 'red')
            return
            
        calc_expr = (expression_str
            .replace('√(', 'sqrt(')
            .replace('^', '**')
            .replace('×', '*')
            .replace('pi', '3.14159265358979323846264338327950288419716939937510')
            .replace('e', '2.71828182845904523536028747135266249775724709369995')
            .replace('sin(', 'sin(')
            .replace('cos(', 'cos(')
            .replace('tan(', 'tan('))
        
        x = sp.symbols('x')
        try:
            expression = sp.sympify(calc_expr)
            f = sp.lambdify(x, expression, 'numpy')
            
            x_values = np.linspace(-100, 100, 4000)
            y_values = f(x_values)
            
            plot_line, = self.ax.plot(x_values, y_values, label=expression_str)
            self.ax.legend()
            
            self.canvas.draw()
            
            self.plots.append((plot_line, expression_str))
            index = len(self.plots) - 1
            self.function_list.add_function(index, expression_str)
            
            self.reset_original_view()
        except Exception as e:
            self.log_area.log_message(f"Không thể giải hàm số, có thể do thiếu dấu nhân (*)", 'red')
        
    def delete_plot(self, index, expression):
        if 0 <= index < len(self.plots):
            plot_line, _ = self.plots.pop(index)
            plot_line.remove()
            self.canvas.draw()
            self.log_area.log_message(f"Đã xóa hàm số: {expression}", 'blue')
    def reset_original_view(self):
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.canvas.draw()
        
    def wheelEvent(self, event):
        if self.canvas.underMouse():
            factor = 1.1 if event.angleDelta().y() > 0 else 1/1.1
            self.ax.set_xlim(self.ax.get_xlim()[0] * factor, self.ax.get_xlim()[1] * factor)
            self.ax.set_ylim(self.ax.get_ylim()[0] * factor, self.ax.get_ylim()[1] * factor)
            self.canvas.draw()

    def on_keyboard_click(self, key):
        cursor_pos = self.function_entry.cursorPosition()
        current_text = self.function_entry.text()
        
        if key == 'Clear':
            self.function_entry.clear()
        elif key == 'Backspace':
            if cursor_pos > 0:
                new_text = current_text[:cursor_pos-1] + current_text[cursor_pos:]
                self.function_entry.setText(new_text)
                self.function_entry.setCursorPosition(cursor_pos-1)
        elif key == '←':
            self.function_entry.setCursorPosition(max(0, cursor_pos - 1))
        elif key == '→':
            self.function_entry.setCursorPosition(min(len(current_text), cursor_pos + 1))
        elif key == 'a²':
            self.function_entry.insert('^2')
        elif key == 'a³':
            self.function_entry.insert('^3')
        else:
            self.function_entry.insert(key)