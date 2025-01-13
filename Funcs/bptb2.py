import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QGridLayout, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QComboBox, QPushButton, QTextEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMessageBox

from Styles.index import styles 

dau = ["≥", "≤"]

class bptb2(QWidget):
    def __init__(self, layout, currentTheme):
        super().__init__()


        self.main_layout = layout
        self.theme = currentTheme

        self.create_widgets()

        self.value1_web_view = 'a'
        self.value2_web_view = '+b'
        self.value3_web_view = '+c'
        self.value4_web_view = '>' 
        diff = r'\\neq'
        self.main_value_web_view = f'{self.value1_web_view}x^2 {self.value2_web_view}x {self.value3_web_view} {self.value4_web_view} 0   (a {diff} 0)'
        self.web_view.loadFinished.connect(lambda: self.update_math(self.main_value_web_view))

    def create_widgets(self):
        self.scroll_content_widget = QWidget(self)
        self.main_layout.addWidget(self.scroll_content_widget)

        layout = QVBoxLayout(self.scroll_content_widget)

        # Tạo web view cho biểu thức toán học
        self.create_web_view()

        # Phần nhập liệu hệ số a, b và dấu lựa chọn
        self.create_input_and_button()

        # Phần hiển thị kết quả và log
        self.create_log_area()

        # Phần vẽ đồ thị
        self.create_plot_area()

        self.scroll_content_widget.setLayout(layout)
    def create_web_view(self):
        self.web_view = QWebEngineView()
        self.web_view.setFixedHeight(40)
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

        # Bọc QWebEngineView trong một QWidget
        web_view_widget = QWidget(self)
        web_view_layout = QVBoxLayout(web_view_widget)
        web_view_layout.addWidget(self.web_view)

        self.scroll_content_widget.layout().addWidget(web_view_widget)
    def update_value_web_view(self):
        self.value1_web_view = self.a_in.text()
        try:
            self.value2_web_view = f'+ {self.b_in.text()}' if int(self.b_in.text()) > 0 else f'-{self.b_in.text()}'
        except:
            pass
        try:
            self.value3_web_view = f'+ {self.c_in.text()}' if int(self.c_in.text()) > 0 else f'-{self.c_in.text()}'
        except:
            pass
        if self.choose_in.currentText() == dau[0]:
            self.value4_web_view = r'\\geq'
        elif self.choose_in.currentText() == dau[1]:
            self.value4_web_view = r'\\leq'
        elif self.choose_in.currentText() in ['>', '<']:
            self.value4_web_view = self.choose_in.currentText()
        else:
            self.value4_web_view = '?'
        self.main_value_web_view = f'{self.value1_web_view}x^2 {self.value2_web_view}x {self.value3_web_view} {self.value4_web_view} 0'
        self.update_math(self.main_value_web_view)
    def update_math(self, latex_code):
        # latex_code = self.convert_to_latex(text)
        self.web_view.page().runJavaScript(f"updateMath('{latex_code}');")


    def create_input_and_button(self):
        input_layout = QGridLayout()

        self.a_in = QLineEdit(self)
        self.b_in = QLineEdit(self)
        self.c_in = QLineEdit(self)

        self.a_in.setPlaceholderText("Nhập hệ số a...")
        self.b_in.setPlaceholderText("Nhập hệ số b...")
        self.c_in.setPlaceholderText("Nhập hệ số c...")

        for item in [self.a_in, self.b_in, self.c_in]:
            item.setStyleSheet(styles(self.theme, 'input'))

        self.choose_in = QComboBox(self)
        self.choose_in.setStyleSheet(styles(self.theme, 'combo_box'))
        self.choose_in.addItems([">", "<", "≥", "≤"])

        self.a_in.textChanged.connect(self.update_value_web_view)
        self.b_in.textChanged.connect(self.update_value_web_view)
        self.c_in.textChanged.connect(self.update_value_web_view)
        self.choose_in.currentTextChanged.connect(self.update_value_web_view)

        input_layout.addWidget(QLabel("a:"), 0, 0)
        input_layout.addWidget(self.a_in, 0, 1)
        input_layout.addWidget(QLabel("b:"), 1, 0)
        input_layout.addWidget(self.b_in, 1, 1)
        input_layout.addWidget(QLabel("c:"), 2, 0)
        input_layout.addWidget(self.c_in, 2, 1)
        input_layout.addWidget(self.choose_in, 3, 0, 1, 3)

        self.solve_button = QPushButton("Giải", self)
        self.solve_button.setStyleSheet(styles(self.theme, 'submit'))
        self.solve_button.clicked.connect(self.solve_2)
        input_layout.addWidget(self.solve_button, 5, 0, 1, 2)

        self.scroll_content_widget.layout().addLayout(input_layout)

    def create_log_area(self):
        self.log_output = QTextEdit(self)
        self.log_output.setStyleSheet(styles(self.theme, 'log_area'))
        self.log_output.setReadOnly(True)
        self.scroll_content_widget.layout().addWidget(self.log_output)

    def create_plot_area(self):
        self.canvas_widget = QWidget(self)
        self.canvas_layout = QVBoxLayout(self.canvas_widget)
        self.scroll_content_widget.layout().addWidget(self.canvas_widget)

    def log(self, message, color="black"):
        colored_message = f'<font color="{color}">{message}</font>'
        self.log_output.append(colored_message)

        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())
    # def create_widgets(self):
    #     # Hệ thống nhập liệu và chọn dấu
    #     self.a_in = QLineEdit(self)
    #     self.b_in = QLineEdit(self)
    #     self.c_in = QLineEdit(self)
    #     self.choose_in = QComboBox(self)
    #     self.choose_in.addItems([">", "<", "≥", "≤"])

    #     self.solve_button = QPushButton("Giải", self)
    #     self.solve_button.clicked.connect(self.solve_2)

    #     # Giao diện nhập liệu
    #     input_layout = QVBoxLayout()
    #     input_layout.addWidget(QLabel("Nhập hệ số: ax² + bx + c ≤ 0"))
    #     input_layout.addWidget(QLabel("a:"))
    #     input_layout.addWidget(self.a_in)
    #     input_layout.addWidget(QLabel("b:"))
    #     input_layout.addWidget(self.b_in)
    #     input_layout.addWidget(QLabel("c:"))
    #     input_layout.addWidget(self.c_in)
    #     input_layout.addWidget(QLabel("Chọn dấu:"))
    #     input_layout.addWidget(self.choose_in)
    #     input_layout.addWidget(self.solve_button)

    #     self.main_layout.addLayout(input_layout)

    #     # Kết quả và log
    #     self.log_output = QTextEdit(self)
    #     self.log_output.setReadOnly(True)
    #     self.main_layout.addWidget(self.log_output)

    #     # Khu vực vẽ đồ thị
    #     self.canvas_widget = QWidget(self)
    #     self.canvas_layout = QVBoxLayout(self.canvas_widget)
    #     self.main_layout.addWidget(self.canvas_widget)

    # def alert_box(self, code):
    #     if code == 1:
    #         QMessageBox.critical(self, "ZeroDivisionError", "a ≠ 0")
    #     elif code == 2:
    #         QMessageBox.critical(self, "ValueError", "Hệ số không được để trống")
    #     elif code == 3:
    #         QMessageBox.critical(self, "UnboundLocalError", "Chưa chọn dấu")

    def solve_2(self):
        try:
            a = float(self.a_in.text())
            b = float(self.b_in.text())
            c = float(self.c_in.text())
        except ValueError:
            self.log("Lỗi giá trị", 'red')
            return

        choose = self.choose_in.currentText()

        if a == 0:
            self.log("Hệ số a phải khác 0", 'blue')
            return

        # Tính Delta
        denta = pow(b, 2) - (4 * a * c)
        self.log(f"Δ = {denta}", 'green')

        # Tính nghiệm và hiển thị kết quả
        try:
            if denta < 0:
                if choose == ">":
                    result = "Tất cả số thực" if a > 0 else "Vô nghiệm"
                elif choose == "<":
                    result = "Vô nghiệm" if a > 0 else "Tất cả số thực"
                elif choose == "≥":
                    result = "Tất cả số thực" if a > 0 else "Vô nghiệm"
                elif choose == "≤":
                    result = "Vô nghiệm" if a > 0 else "Tất cả số thực"
            elif denta == 0:
                x = -b / (2 * a)
                if choose == ">":
                    result = f"x ≠ {x}" if a > 0 else "Vô nghiệm"
                elif choose == "<":
                    result = "Vô nghiệm" if a > 0 else f"x ≠ {x}"
                elif choose == "≥":
                    result = "Tất cả số thực" if a > 0 else f"x = {x}"
                elif choose == "≤":
                    result = f"x = {x}" if a > 0 else "Tất cả số thực"
            else:
                sqrt_denta = math.sqrt(denta)
                x1 = round(((-b - sqrt_denta) / (2 * a)), 3)
                x2 = round(((-b + sqrt_denta) / (2 * a)), 3)
                if choose == ">":
                    result = f"x < {x1} hoặc x > {x2}" if a > 0 else f"{x1} ≤ x ≤ {x2}"
                elif choose == "<":
                    result = f"{x1} ≤ x ≤ {x2}" if a > 0 else f"x < {x1} hoặc x > {x2}"
                elif choose == "≥":
                    result = f"x ≤ {x1} hoặc x ≥ {x2}" if a > 0 else f"{x1} ≤ x ≤ {x2}"
                elif choose == "≤":
                    result = f"{x1} ≤ x ≤ {x2}" if a > 0 else f"x ≤ {x2} hoặc x ≥ {x1}"
            self.log(f"-> Kết quả: {result}", 'green')
        except Exception as e:
            self.log('Chưa chọn dấu', 'red')

        # Vẽ đồ thị
        self.plot_graph(a, b, c, choose)

    def plot_graph(self, a, b, c, choose):
        x_values = np.arange(-5, 5, 0.1)
        y_values = a * x_values**2 + b * x_values + c

        fig, ax = plt.subplots()

        if choose == ">" or choose == "≥":
            plt.fill_between(x_values, -abs(max(y_values)), y_values, color="lightblue", alpha=0.8)
            if choose == ">":
                plt.plot(x_values, y_values, label=f"{a}x² + {b}x + {c} > 0", color="blue", linestyle='dashed', alpha=0.6)
            elif choose == "≥":
                plt.plot(x_values, y_values, label=f"{a}x² + {b}x + {c} ≥ 0", color="blue")
        if choose == "<" or choose == "≤":
            plt.fill_between(x_values, abs(max(y_values)), y_values, color="lightblue", alpha=0.8)
            if choose == "<":
                plt.plot(x_values, y_values, label=f"{a}x² + {b}x + {c} < 0", color="blue", linestyle='dashed', alpha=0.6)
            elif choose == "≤":
                plt.plot(x_values, y_values, label=f"{a}x² + {b}x + {c} ≤ 0", color="blue")

        plt.axhline(0, color="gray", linestyle="--")
        plt.axvline(0, color="gray", linestyle="--")
        plt.grid(True)
        plt.legend(fontsize=6)

        canvas = FigureCanvas(fig)
        canvas.draw()

        for i in reversed(range(self.canvas_layout.count())):
            widget = self.canvas_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        self.canvas_layout.addWidget(canvas)
        plt.close(fig)

def main():
    app = QApplication(sys.argv)
    window = bptb2()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
