import sys
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QFrame, QGridLayout, QTextEdit, QSizePolicy, QScrollArea
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt

from Styles.index import styles

class nguyenham(QMainWindow):
    def __init__(self, layout, currentTheme):
        super().__init__()

        self.main_layout = layout
        self.theme = currentTheme
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.main_layout = QHBoxLayout(self.main_widget)
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        self.main_layout.addLayout(self.left_layout, 1)
        self.main_layout.addLayout(self.right_layout, 3)

        self.create_widgets()

    def create_widgets(self):
        # Left side widgets (input, virtual keyboard, log)
        self.create_web_view(self.left_layout)
        self.create_input_and_keyboard()
        self.create_log_area()

        # Right side widgets (plot)
        self.create_plot()
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
                    
                # Tìm vị trí dấu '/'
                div_index = expr.find('/')
                
                # Tìm tử số
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

                # Loại bỏ ngoặc không cần thiết
                numerator = numerator.strip('()')
                denominator = denominator.strip('()')
                
                before = expr[:left]
                after = expr[right:]
                return before + r'\\frac{' + numerator + '}{' + denominator + '}' + after

            # Xử lý các phép chia
            while '/' in expression:
                expression = convert_fraction(expression)

            # Xử lý các ký tự đặc biệt khác
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

    def create_input_and_keyboard(self):
        # Input and virtual keyboard on the left side
        self.create_input_widgets()
        self.create_virtual_keyboard()

    def create_input_widgets(self):
        self.function_label = QLabel("f(x):", self)
        self.function_entry = QLineEdit(self)
        self.function_entry.setPlaceholderText('Nhập hàm số...')
        self.function_entry.setStyleSheet(styles(self.theme, 'input'))
        self.function_entry.setFocus()
        self.function_entry.textChanged.connect(self.update_latex_preview)


        self.derivative_label = QLabel("Hằng số c:", self)

        self.derivative_entry = QLineEdit(self)
        self.derivative_entry.setPlaceholderText('Nhập hằng số c...')
        self.derivative_entry.setStyleSheet(styles(self.theme, 'input'))
        self.derivative_entry.setFocus()

        self.derivative_button = QPushButton("Tính Nguyên hàm", self)
        self.derivative_button.setStyleSheet(styles(self.theme, 'submit'))
        self.derivative_button.clicked.connect(self.plot_derivative)

        input_layout = QGridLayout()
        input_layout.addWidget(self.function_label, 0, 0)
        input_layout.addWidget(self.function_entry, 0, 1)
        input_layout.addWidget(self.derivative_button, 2, 0, 1, 2)
        input_layout.addWidget(self.derivative_label, 1, 0)
        input_layout.addWidget(self.derivative_entry, 1, 1)

        self.left_layout.addLayout(input_layout)

    def create_virtual_keyboard(self):
        keyboard_frame = QFrame(self)
        keyboard_layout = QGridLayout(keyboard_frame)

        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('×', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('x', 3, 2), ('+', 3, 3),
            ('sin(', 4, 0), ('cos(', 4, 1), ('tan(', 4, 2), ('Clear', 4, 3),
            ('(', 5, 0), (')', 5, 1), ('^(', 5, 2), ('Backspace', 5, 3),
            ('←', 6, 0), ('→', 6, 1), ('π', 6, 2), ('e', 6, 3),
            ('√(', 7, 0), ('×10^(', 7, 1), ('a²', 7, 2), ('a³', 7, 3),
        ]

        for text, row, column in buttons:
            button = QPushButton(text, self)
            button.setStyleSheet(styles(self.theme, 'button'))
            button.clicked.connect(lambda checked, t=text: self.on_keyboard_click(t))
            keyboard_layout.addWidget(button, row, column)

        self.left_layout.addWidget(keyboard_frame)

    def create_log_area(self):
        self.log_area = QTextEdit(self)
        self.log_area.setStyleSheet(styles(self.theme, 'log_area'))
        self.left_layout.addWidget(self.log_area)
    def log(self, message, color="black"):
        colored_message = f'<font color="{color}">{message}</font>'
        self.log_area.append(colored_message)

        self.log_area.verticalScrollBar().setValue(self.log_area.verticalScrollBar().maximum())
    def create_plot(self):
        plot_frame = QFrame(self)
        self.right_layout.addWidget(plot_frame)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.canvas_widget = self.canvas
        self.canvas_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right_layout.addWidget(self.canvas_widget)

        toolbar = NavigationToolbar(self.canvas, self)
        self.right_layout.addWidget(toolbar)

        self.ax.axhline(0, color='black', linewidth=0.5)
        self.ax.axvline(0, color='black', linewidth=0.5)

    def on_keyboard_click(self, key):
        cursor_index = self.function_entry.cursorPosition()

        if key == 'Clear':
            self.function_entry.clear()
        elif key == 'Backspace':
            if cursor_index > 0:
                self.function_entry.backspace()
        elif key == 'a²':
            self.function_entry.insert('^2')
        elif key == 'a³':
            self.function_entry.insert('^3')
        elif key == '←':
            self.move_cursor_left()
        elif key == '→':
            self.move_cursor_right()
        else:
            self.function_entry.insert(key)

    def plot_derivative(self):
        expression_str = self.function_entry.text()

        # Thay đổi kí tự '√' thành 'sqrt'
        expression_str = expression_str.replace('√', 'sqrt')
        expression_str = expression_str.replace('^', '**')
        expression_str = expression_str.replace('×', '*')
        expression_str = expression_str.replace('π', '3.14159265358979323846264338327950288419716939937510')
        expression_str = expression_str.replace('e', '2.71828182845904523536028747135266249775724709369995')
        x = sp.symbols('x')
        tangent_point = self.derivative_entry.text()
        if len(tangent_point) == 0:
            tangent_point = 0
        else:
            tangent_point = float(tangent_point)
        try:
            expression = sp.sympify(expression_str)
            derivative_alt = derivative = sp.integrate(expression, x)
            derivative = sp.sympify(str(derivative) + '+' + str(tangent_point))
            f = sp.lambdify(x, expression, 'numpy')
            f_prime = sp.lambdify(x, derivative, 'numpy')

            # Tạo một mảng numpy với kiểu dữ liệu phù hợp
            x_values = np.linspace(-100, 100, 10000, dtype=np.float64)
            xg_values = np.linspace(-100, 100, 10000, dtype=np.float64)

            # Tính toán y_values sử dụng hàm f_prime
            y_values = f_prime(x_values)
            yg_values = f(xg_values)

            self.ax.clear()
            self.ax.plot(xg_values, yg_values, label=str(expression))
            self.ax.plot(x_values, y_values, label=str(derivative))
            self.ax.grid(True)
            self.ax.legend()

            # Đặt giới hạn cho trục
            self.ax.set_xlim(-10, 10)
            self.ax.set_ylim(-10, 10)

            self.canvas.draw()
            self.log(f"∫f(x)dx = {derivative_alt} + c", 'green')

        except Exception as e:
            self.log(f"Lỗi: Không thể tính nguyên hàm hoặc vẽ đồ thị. {str(e)}", 'red')

    def move_cursor_left(self):
        cursor_index = self.function_entry.cursorPosition()
        if cursor_index > 0:
            self.function_entry.setCursorPosition(cursor_index - 1)

    def move_cursor_right(self):
        cursor_index = self.function_entry.cursorPosition()
        text_length = len(self.function_entry.text())
        if cursor_index < text_length:
            self.function_entry.setCursorPosition(cursor_index + 1)

    def zoom_with_mouse_wheel(self, event):
        factor = 1.1 if event.delta() > 0 else 1 / 1.1
        self.ax.set_xlim(self.ax.get_xlim()[0] * factor, self.ax.get_xlim()[1] * factor)
        self.ax.set_ylim(self.ax.get_ylim()[0] * factor, self.ax.get_ylim()[1] * factor)
        self.canvas.draw()

def main():
    app = QApplication(sys.argv)
    window = nguyenham(QHBoxLayout())
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
