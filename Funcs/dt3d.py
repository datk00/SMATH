import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QFrame, QGridLayout, QTextEdit
from PyQt5.QtCore import Qt
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from PyQt5.QtWebEngineWidgets import QWebEngineView

from Styles.index import styles


class dt3d(QMainWindow):
    def __init__(self, layout, currentTheme):
        super().__init__()

        self.main_layout = layout
        self.theme = currentTheme
        self.plots = []
        self.initUI()

    def initUI(self):
        # Tạo layout chính
        self.main_layout = QHBoxLayout()

        left_widget = QWidget()
        left_layout = QVBoxLayout()
        self.create_web_view(left_layout)

        input_section = QWidget()
        input_layout = QVBoxLayout()
        self.function_label = QLabel("f(x, y):")
        self.function_entry = QLineEdit(self)
        self.function_entry.setPlaceholderText('Nhập hàm số...')
        self.function_entry.setStyleSheet(styles(self.theme, 'input'))
        self.function_entry.textChanged.connect(self.update_latex_preview)

        input_layout.addWidget(self.function_label)
        input_layout.addWidget(self.function_entry)
        input_section.setLayout(input_layout)
        
        self.solve_button = QPushButton("Giải", self)
        self.solve_button.setStyleSheet(styles(self.theme, 'submit'))
        self.solve_button.clicked.connect(self.solve_and_plot_function)
        
        keyboard_widget = QWidget()
        keyboard_layout = QVBoxLayout()
        self.create_virtual_keyboard(keyboard_layout)
        keyboard_widget.setLayout(keyboard_layout)
        
        # 4. Log 
        self.log_display = QTextEdit()
        self.log_display.setStyleSheet(styles(self.theme, 'log_area'))
        self.log_display.setFixedHeight(70)
        
        left_layout.addWidget(input_section)
        left_layout.addWidget(self.solve_button)
        left_layout.addWidget(keyboard_widget)
        left_layout.addWidget(self.log_display)
        
        left_layout.addStretch()
        
        left_widget.setLayout(left_layout)

        right_widget = QWidget()
        right_layout = QVBoxLayout()

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        right_layout.addWidget(self.toolbar)
        right_layout.addWidget(self.canvas)

        right_widget.setLayout(right_layout)

        self.main_layout.addWidget(left_widget, 1)
        self.main_layout.addWidget(right_widget, 2)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)
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
                
                # Tìm mẫu số
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
            self.web_view.page().runJavaScript(f"updateMath('{expression}')")

    def create_virtual_keyboard(self, layout):
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('×', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('a²', 3, 2), ('+', 3, 3),
            ('sin(', 4, 0), ('cos(', 4, 1), ('tan(', 4, 2), ('Clear', 4, 3),
            ('(', 5, 0), (')', 5, 1), ('^(', 5, 2), ('Backspace', 5, 3), 
            ('←', 6, 0), ('→', 6, 1), ('π', 6, 2), ('e', 6, 3),
            ('√(', 7, 0), ('×10^(', 7, 1), ('x', 7, 2), ('y', 7, 3),
        ]
        
        keyboard_frame = QFrame()
        keyboard_grid = QGridLayout()
        for text, row, column in buttons:
            button = QPushButton(text, self)
            button.setStyleSheet(styles(self.theme, 'button'))
            button.clicked.connect(lambda _, key=text: self.on_keyboard_click(key))
            keyboard_grid.addWidget(button, row, column)

        keyboard_frame.setLayout(keyboard_grid)
        layout.addWidget(keyboard_frame)

    def on_keyboard_click(self, key):
        cursor_index = self.function_entry.cursorPosition()

        if key == 'Clear':
            self.function_entry.clear()
        elif key == 'Backspace':
            if cursor_index > 0:
                self.function_entry.setText(self.function_entry.text()[:-1])
        elif key == 'a²':
            self.function_entry.setText(self.function_entry.text() + '^2')
        elif key == '←':
            self.move_cursor_left()
        elif key == '→':
            self.move_cursor_right()
        elif key == '(':
            self.function_entry.setText(self.function_entry.text() + '(')
        elif key == ')':
            self.function_entry.setText(self.function_entry.text() + ')')
        elif key == 'π':
            self.function_entry.setText(self.function_entry.text() + '3.141592653589793')
        elif key == 'e':
            self.function_entry.setText(self.function_entry.text() + '2.718281828459045')
        else:
            self.function_entry.setText(self.function_entry.text() + key)

    def move_cursor_left(self):
        cursor_index = self.function_entry.cursorPosition()
        if cursor_index > 0:
            self.function_entry.setCursorPosition(cursor_index - 1)

    def move_cursor_right(self):
        cursor_index = self.function_entry.cursorPosition()
        text_length = len(self.function_entry.text())
        if cursor_index < text_length:
            self.function_entry.setCursorPosition(cursor_index + 1)

    def log(self, message, color="black"):
        colored_message = f'<font color="{color}">{message}</font>'
        self.log_display.append(colored_message)

        self.log_display.verticalScrollBar().setValue(self.log_display.verticalScrollBar().maximum())

    def solve_and_plot_function(self):
        expression_str = self.function_entry.text()
        if not expression_str:
            self.log("Lỗi: Vui lòng nhập hàm số", 'red')
            return
        self.plot_function(expression_str)

    def plot_function(self, expression_str):
        expression_str = expression_str.replace('√', 'sqrt')
        expression_str = expression_str.replace('^', '**')
        expression_str = expression_str.replace('×', '*')

        x, y = sp.symbols('x y')
        try:
            expression = sp.sympify(expression_str)
            f = sp.lambdify((x, y), expression, 'numpy')

            x_values = np.linspace(-100, 100, 400)
            y_values = np.linspace(-100, 100, 400)
            X, Y = np.meshgrid(x_values, y_values)
            Z = f(X, Y)

            self.ax.clear()
            self.ax.plot_surface(X, Y, Z, cmap='viridis')
            self.ax.set_xlabel('X')
            self.ax.set_ylabel('Y')
            self.ax.set_zlabel('Z')
            self.ax.set_box_aspect([6, 6, 6])

            self.canvas.draw()
            self.log(f"Đã vẽ đồ thị thành công: {expression_str}", 'green')
        except Exception as e:
            self.log(f"Lỗi vẽ đồ thị: {str(e)}", 'red')

    def on_window_resize(self, event):
        self.canvas.draw()


def main():
    app = QApplication(sys.argv)
    window = dt3d()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()