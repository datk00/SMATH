from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QFrame, QGridLayout, QTextEdit, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from Styles.index import styles

class daoham(QMainWindow):
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
        self.create_function_input()
        self.create_virtual_keyboard()
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

    def create_function_input(self):
        self.create_web_view(self.left_layout)
        self.function_label = QLabel("f(x):", self)
        self.function_entry = QLineEdit(self)
        self.function_entry.setPlaceholderText('Nhập hàm số...')
        self.function_entry.setStyleSheet(styles(self.theme, 'input'))
        self.function_entry.setFocus()
        self.function_entry.textChanged.connect(self.update_latex_preview)

        self.x0_label = QLabel("Điểm x₀:", self)
        self.x0_entry = QLineEdit(self)
        self.x0_entry.setPlaceholderText('Nhập điểm x₀...')
        self.x0_entry.setStyleSheet(styles(self.theme, 'input'))


        self.derivative_button = QPushButton("Tính Đạo hàm", self)
        self.derivative_button.setStyleSheet(styles(self.theme, 'submit'))
        self.derivative_button.clicked.connect(self.plot_derivative)

        input_layout = QGridLayout()
        input_layout.addWidget(self.function_label, 0, 0)
        input_layout.addWidget(self.function_entry, 0, 1)
        input_layout.addWidget(self.x0_label, 1, 0)
        input_layout.addWidget(self.x0_entry, 1, 1)
        input_layout.addWidget(self.derivative_button, 2, 0, 1, 2)

        self.left_layout.addLayout(input_layout)

    def create_plot(self):
        self.plot_frame = QFrame(self)
        self.right_layout.addWidget(self.plot_frame)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.canvas_widget = self.canvas
        self.canvas_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right_layout.addWidget(self.canvas_widget)

        toolbar = NavigationToolbar(self.canvas, self)
        self.right_layout.addWidget(toolbar)

        self.ax.axhline(0, color='black', linewidth=0.5)
        self.ax.axvline(0, color='black', linewidth=0.5)

    def create_virtual_keyboard(self):
        self.keyboard_frame = QFrame(self)
        self.keyboard_layout = QGridLayout(self.keyboard_frame)

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
            self.keyboard_layout.addWidget(button, row, column)

        self.left_layout.addWidget(self.keyboard_frame)

    def create_log_area(self):
        self.log_area = QTextEdit(self)
        self.log_area.setStyleSheet(styles(self.theme, 'log_area'))
        self.left_layout.addWidget(self.log_area)
    def log(self, message, color="black"):
        colored_message = f'<font color="{color}">{message}</font>'
        self.log_area.append(colored_message)

        self.log_area.verticalScrollBar().setValue(self.log_area.verticalScrollBar().maximum())
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

    def plot_derivative(self, event=None):
        expression_str = self.function_entry.text()

        # Thay đổi kí tự '√' thành 'sqrt'
        expression_str = expression_str.replace('√', 'sqrt')
        expression_str = expression_str.replace('^', '**')
        expression_str = expression_str.replace('×', '*')
        expression_str = expression_str.replace('π', '3.14159265358979323846264338327950288419716939937510')
        expression_str = expression_str.replace('e', '2.71828182845904523536028747135266249775724709369995')

        x = sp.symbols('x')

        try:
            expression = sp.sympify(expression_str)
            derivative = sp.diff(expression, x)
            f = sp.lambdify(x, expression, 'numpy')
            f_prime = sp.lambdify(x, derivative, 'numpy')
            x_values = np.linspace(-100, 100, 10000, dtype=np.float64)
            y_values = f_prime(x_values)
            yg_values = f(x_values)

            self.ax.clear()
            self.ax.plot(x_values, yg_values, label=f"f(x) = {expression}")

            if isinstance(derivative, sp.Number):
                y_values = np.full_like(x_values, float(derivative))

            self.ax.plot(x_values, y_values, label=f"f'(x) = {derivative}")

            # Lấy điểm đạo hàm x₀ từ ô nhập
            tangent_point = float(self.x0_entry.text())

            # Tính toán đạo hàm tại điểm x₀
            tangent_slope = float(derivative.subs(x, tangent_point))
            tangent_intercept = float(expression.subs(x, tangent_point)) - tangent_slope * tangent_point

            # Tính và vẽ đường tiếp tuyến
            tangent_line = tangent_slope * x_values + tangent_intercept
            self.ax.plot(x_values, tangent_line, label=f"Tangent: y = {round(tangent_slope, 6)}*x + {round(tangent_intercept, 6)}")
            self.ax.scatter(tangent_point, f(tangent_point), color='red')

            self.ax.grid(True)
            self.ax.legend()
            self.reset_original_view()
            self.canvas.draw()

    
            self.log(f'f(x) = {expression}', 'green')
            self.log(f"f'(x) = {derivative}", 'green')
            self.log(f'PT tiếp tuyến y = {float(round(tangent_slope, 6))}*x + {float(round(tangent_intercept, 6))}', 'green')
            # self.create_zoom_button(tangent_point, f_prime(tangent_point))

        except Exception as e:
            self.log(f"Lỗi {e}", 'red')

    def reset_original_view(self):
        self.ax.set_xlim(-100, 100)
        self.ax.set_ylim(-10, 10)

  
    def zoom_to_derivative(self, x0, f_prime_at_x0):
        try:
            # Điều chỉnh phạm vi cho x và y
            x_range = 50
            y_range = 50

            # Giới hạn mới cho trục x và y sao cho điểm đạo hàm nằm ở giữa
            new_xlim = (x0 - x_range / 2, x0 + x_range / 2)
            new_ylim = (f_prime_at_x0 - y_range / 2, f_prime_at_x0 + y_range / 2)

            # Áp dụng các giới hạn mới cho đồ thị
            self.ax.set_xlim(new_xlim)
            self.ax.set_ylim(new_ylim)

            # Vẽ lại đồ thị
            self.canvas.draw()
        except ValueError:
            self.log_area.append("Lỗi: Vui lòng nhập một số hợp lệ cho x₀.")

    def move_cursor_left(self):
        cursor_index = self.function_entry.cursorPosition()
        if cursor_index > 0:
            self.function_entry.setCursorPosition(cursor_index - 1)

    def move_cursor_right(self):
        cursor_index = self.function_entry.cursorPosition()
        text_length = len(self.function_entry.text())
        if cursor_index < text_length:
            self.function_entry.setCursorPosition(cursor_index + 1)


def main():
    app = QApplication(sys.argv)
    window = daoham()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
