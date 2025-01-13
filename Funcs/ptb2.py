import sys, re
import math
import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWebEngineWidgets import QWebEngineView
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from Styles.index import styles 


class ptb2(QtWidgets.QWidget):
    def __init__(self, layout, currentTheme):
        super().__init__()

        self.main_layout = layout
        self.theme = currentTheme

        # Không sử dụng QScrollArea nữa
        self.create_widgets()

        self.first_value_web_view = '0'
        self.second_value_web_view = '0'
        self.third_value_web_view = '0'
        self.main_value_web_view = f"{self.first_value_web_view}x^2 + {self.second_value_web_view}x + {self.third_value_web_view} = 0"
        self.web_view.loadFinished.connect(lambda: self.update_math(self.main_value_web_view))

    def create_widgets(self):
        layout = QtWidgets.QVBoxLayout(self)

        # Phần hiển thị công thức toán học
        self.create_web_view()
        # Phần nhập liệu
        self.create_input_and_button()

        # Phần hiển thị log kết quả
        self.create_log_area()
        # Phần khung vẽ đồ thị
        self.create_plot_area()

        self.setLayout(layout)

    def create_input_and_button(self):
        input_layout = QtWidgets.QGridLayout()

        self.a_in = QtWidgets.QLineEdit(self)
        self.b_in = QtWidgets.QLineEdit(self)
        self.c_in = QtWidgets.QLineEdit(self)

        self.a_in.setPlaceholderText("Nhập hệ số a...")
        self.b_in.setPlaceholderText("Nhập hệ số b...")
        self.c_in.setPlaceholderText("Nhập hệ số c...")
        for item in [self.a_in, self.b_in, self.c_in]:
            item.setStyleSheet(styles(self.theme, 'input'))
            item.textChanged.connect(self.update_value_web_view)

        input_layout.addWidget(QtWidgets.QLabel("a:"), 0, 0)
        input_layout.addWidget(self.a_in, 0, 1)
        input_layout.addWidget(QtWidgets.QLabel("b:"), 1, 0)
        input_layout.addWidget(self.b_in, 1, 1)
        input_layout.addWidget(QtWidgets.QLabel("c:"), 2, 0)
        input_layout.addWidget(self.c_in, 2, 1)

        self.solve_btn = QtWidgets.QPushButton("Giải", self)
        self.solve_btn.setStyleSheet(styles(self.theme, 'submit'))
        self.solve_btn.clicked.connect(self.solve_equation)

        input_layout.addWidget(self.solve_btn, 3, 0, 1, 2)

        self.layout().addLayout(input_layout)

    def create_plot_area(self):
        # Khung vẽ đồ thị
        self.canvas_widget = QtWidgets.QWidget(self)
        self.canvas_layout = QtWidgets.QVBoxLayout(self.canvas_widget)
        self.layout().addWidget(self.canvas_widget)

    def create_log_area(self):
        # Khung log
        self.log_output = QtWidgets.QTextEdit(self)
        self.log_output.setStyleSheet(styles(self.theme, 'log_area'))
        self.log_output.setReadOnly(True)
        self.layout().addWidget(self.log_output)

    def create_web_view(self):
        self.web_view = QWebEngineView(self)
        self.web_view.setFixedHeight(50)
        self.web_view.setHtml("""
        <html>
        <head>
            <style>
                 #MathJax_Message {
                display: none;
            }
            </style>
            <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML"></script>
        </head>
        <body>
            <div id="output">Hello, MathJax!</div>
            <script>
                function updateMath(latex) {
                    document.getElementById('output').innerHTML = '$$' + latex + '$$';
                    MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
                }
            </script>
        </body>
        </html>
        """)
        
        web_view_widget = QtWidgets.QWidget(self)
        web_view_layout = QtWidgets.QVBoxLayout(web_view_widget)
        web_view_layout.addWidget(self.web_view)

        self.layout().addWidget(web_view_widget)

    def update_value_web_view(self):
        self.first_value_web_view = self.a_in.text()
        self.second_value_web_view = self.b_in.text()
        self.third_value_web_view = self.c_in.text()
        self.main_value_web_view = f"{self.first_value_web_view}x^2 + {self.second_value_web_view}x + {self.third_value_web_view} = 0"
        self.update_math(self.main_value_web_view)

    def update_math(self, text):
        latex_code = self.convert_to_latex(text)
        self.web_view.page().runJavaScript(f"updateMath('{latex_code}');")

    def convert_to_latex(self, text):
        # Tìm kiếm và thay thế các biểu thức toán học thành LaTeX
        text = re.sub(r'(\w+)\^(\d+)', r'\1^{\2}', text)  # Công thức có dạng x^2
        return text

    def log(self, message, color="black"):
        colored_message = f'<font color="{color}">{message}</font>'
        self.log_output.append(colored_message)

        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())
    def solve_equation(self):
        try:
            a = float(self.a_in.text())
            b = float(self.b_in.text())
            c = float(self.c_in.text())
        except ValueError:
            self.log("Hệ số không được để trống", 'red')
            return

        if a == 0:
            self.log("a ≠ 0", 'blue')
            return

        denta = b**2 - 4 * a * c
        self.log(f"Δ = {denta}", 'green')

        if denta > 0:
            can_denta = math.sqrt(denta)
            x1 = (-b + can_denta) / (2 * a)
            x2 = (-b - can_denta) / (2 * a)
            self.log(f"x1 = {x1}", 'green')
            self.log(f"x2 = {x2}", 'green')
        elif denta == 0:
            x = -b / (2 * a)
            self.log(f"x = {x}", 'green')
        else:
            self.log("Vô nghiệm", 'green')

        tdx = round(-b / (2 * a), 6)
        ttp = round(-denta / (4 * a), 6)
        self.log(f"TĐX = {tdx}", 'blue')
        self.log(f"I = ({tdx}, {ttp})", 'blue')

        # Vẽ đồ thị
        self.plot_graph(a, b, c, denta)

    def plot_graph(self, a, b, c, denta):
        x_values = np.linspace(-10, 10, 100)
        y_values = a * x_values**2 + b * x_values + c

        fig, ax = plt.subplots(figsize=(5, 3))  # Điều chỉnh kích thước đồ thị
        ax.plot(x_values, y_values, label=f"{a}x^2 + {b}x + {c} = 0")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.axhline(0, color="gray", linestyle="--")
        ax.axvline(0, color="gray", linestyle="--")
        
        if denta > 0:
            x1 = (-b + math.sqrt(denta)) / (2 * a)
            x2 = (-b - math.sqrt(denta)) / (2 * a)
            ax.scatter(x1, 0, color='hotpink')
            ax.scatter(x2, 0, color='#88c999')
        elif denta == 0:
            x1 = -b / (2 * a)
            ax.scatter(x1, 0, color='red')

        ax.grid(True)
        ax.legend(fontsize=6)

        # Tạo canvas để hiển thị đồ thị
        canvas = FigureCanvas(fig)
        canvas.draw()

        # Đảm bảo widget chứa canvas luôn được cập nhật
        for i in reversed(range(self.canvas_layout.count())):
            widget = self.canvas_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        self.canvas_layout.addWidget(canvas)
        plt.close(fig)


