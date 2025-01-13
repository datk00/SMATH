import sys, re
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWebEngineWidgets import QWebEngineView

from Styles.index import styles


dau = ["≥", "≤"]

class bptbn(QtWidgets.QWidget):
    def __init__(self, layout, currentTheme):
        super().__init__()
        self.main_layout = layout
        self.theme = currentTheme
        self.create_widgets()

        self.value1_web_view = 'a'
        self.value2_web_view = '+b'
        self.value3_web_view = '>' 
        self.main_value_web_view = f'{self.value1_web_view}x {self.value2_web_view} {self.value3_web_view} 0'
        self.web_view.loadFinished.connect(lambda: self.update_math(self.main_value_web_view))

    def create_widgets(self):
        self.scroll_content_widget = QtWidgets.QWidget(self)
        self.main_layout.addWidget(self.scroll_content_widget)

        layout = QtWidgets.QVBoxLayout(self.scroll_content_widget)

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
        web_view_widget = QtWidgets.QWidget(self)
        web_view_layout = QtWidgets.QVBoxLayout(web_view_widget)
        web_view_layout.addWidget(self.web_view)

        self.scroll_content_widget.layout().addWidget(web_view_widget)

    def update_value_web_view(self):
        self.value1_web_view = self.a_in.text()
        try:
            self.value2_web_view = f'+ {self.b_in.text()}' if int(self.b_in.text()) > 0 else f'-{self.b_in.text()}'
        except:
            pass
        if self.choose_in.currentText() == dau[0]:
            self.value3_web_view = r'\\geq'
        elif self.choose_in.currentText() == dau[1]:
            self.value3_web_view = r'\\leq'
        elif self.choose_in.currentText() in ['>', '<']:
            self.value3_web_view = self.choose_in.currentText()
        else:
            self.value3_web_view = '?'
        self.main_value_web_view = f'{self.value1_web_view}x {self.value2_web_view} {self.value3_web_view} 0'
        self.update_math(self.main_value_web_view)
    def update_math(self, latex_code):
        # latex_code = self.convert_to_latex(text)
        self.web_view.page().runJavaScript(f"updateMath('{latex_code}');")


    def create_input_and_button(self):
        input_layout = QtWidgets.QGridLayout()

        self.a_in = QtWidgets.QLineEdit(self)
        self.b_in = QtWidgets.QLineEdit(self)
        
        self.a_in.setPlaceholderText("Nhập hệ số a...")
        self.b_in.setPlaceholderText("Nhập hệ số b...")

        for item in [self.a_in, self.b_in]:
            item.setStyleSheet(styles(self.theme, 'input'))        
        
        self.choose_in = QtWidgets.QComboBox(self)
        self.choose_in.setStyleSheet(styles(self.theme, 'combo_box'))
        self.choose_in.addItems([">", "<", "≥", "≤"])

        self.a_in.textChanged.connect(self.update_value_web_view)
        self.b_in.textChanged.connect(self.update_value_web_view)
        self.choose_in.currentTextChanged.connect(self.update_value_web_view)

        input_layout.addWidget(QtWidgets.QLabel("a:"), 0, 0)
        input_layout.addWidget(self.a_in, 0, 1)
        input_layout.addWidget(QtWidgets.QLabel("b:"), 1, 0)
        input_layout.addWidget(self.b_in, 1, 1)
        input_layout.addWidget(self.choose_in, 2, 0, 1, 2)

        self.solve_button = QtWidgets.QPushButton("Giải", self)
        self.solve_button.setStyleSheet(styles(self.theme, 'submit'))
        self.solve_button.clicked.connect(self.solve_equation)
        input_layout.addWidget(self.solve_button, 5, 0, 1, 2)

        self.scroll_content_widget.layout().addLayout(input_layout)

    def create_log_area(self):
        self.log_output = QtWidgets.QTextEdit(self)
        self.log_output.setStyleSheet(styles(self.theme, 'log_area'))
        self.scroll_content_widget.layout().addWidget(self.log_output)

    def create_plot_area(self):
        self.canvas_widget = QtWidgets.QWidget(self)
        self.canvas_layout = QtWidgets.QVBoxLayout(self.canvas_widget)
        self.scroll_content_widget.layout().addWidget(self.canvas_widget)

    def log(self, message, color="black"):
        colored_message = f'<font color="{color}">{message}</font>'
        self.log_output.append(colored_message)

        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())
    def solve_equation(self):
        try:
            a = float(self.a_in.text())
            b = float(self.b_in.text())
            choose = self.choose_in.currentText()
            print(choose)
        except ValueError:
            self.log("Hệ số không được để trống hoặc không hợp lệ.", 'red')
            return

        result = self.solve_inequality(a, b, choose)
        self.log(f"Giải bất phương trình: a={a}, b={b}, dấu={choose} -> Kết quả: {result}", 'green')
        self.plot_graph(a, b, choose)

    def solve_inequality(self, a, b, choose):
        try:
            if a > 0 and len(choose) == 1:
                x = -b / a
                if x == int(x):
                    x = int(x)
                return f"x {choose} {x}"
            elif a == 0 and len(choose) == 1:
                if choose == '>' and b > 0:
                    return "Bất phương trình đúng với mọi x"
                elif choose == '>' and b <= 0:
                    return "Vô nghiệm"
                elif choose == dau[0] and b >= 0:
                    return "Bất phương trình đúng với mọi x"
                elif choose == '<' and b >= 0:
                    return "Vô nghiệm"
                elif choose == dau[1] and b > 0:
                    return "Vô nghiệm"
                elif choose == dau[1] and b <= 0:
                    return "Bất phương trình đúng với mọi x"
                elif choose == '<' and b < 0:
                    return "Bất phương trình đúng với mọi x"
                else:
                    return "Vô nghiệm"
            else:
                x = -b / a
                choose1 = dau[0] if choose == '<' else dau[1] if choose == '>' else ('<' if choose == dau[0] else '>')
                if x == int(x):
                    x = int(x)
                return f"x {choose1} {x}"

        except Exception as e:
            return f"Error: {str(e)}"

    def plot_graph(self, a, b, choose):
        x_values = np.arange(-5, 5, 0.1)
        y_values = a * x_values + b

        fig, ax = plt.subplots()

        if choose == ">" or choose == dau[0]:
            if choose == ">":
                plt.plot(x_values, y_values, label=f"{a}x + {b} > 0", color="blue", linestyle='dashed', alpha=0.6)
            else:
                plt.plot(x_values, y_values, label=f"{a}x + {b} {dau[0]} 0", color="blue")
            plt.fill_between(x_values, -abs(max(y_values)), y_values, color="lightblue", alpha=0.8)
        elif choose == "<" or choose == dau[1]:
            if choose == "<":
                plt.plot(x_values, y_values, label=f"{a}x + {b} < 0", color="blue", linestyle='dashed', alpha=0.6)
            else:
                plt.plot(x_values, y_values, label=f"{a}x + {b} {dau[1]} 0", color="blue")
            plt.fill_between(x_values, abs(max(y_values)), y_values, color="lightblue", alpha=0.8)

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
    app = QtWidgets.QApplication(sys.argv)
    window = bptbn(QtWidgets.QVBoxLayout())
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
