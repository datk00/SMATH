import sys
import re
import numpy as np
import math
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWebEngineWidgets import QWebEngineView
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


from Styles.index import styles

class ptbn(QtWidgets.QWidget):
    def __init__(self, layout, currentTheme):
        super().__init__()

        self.main_layout = layout
        self.theme = currentTheme
        self.create_widgets()

        
        
        self.first_value_web_view = '0'
        self.second_value_web_view = '0'
        self.main_value_web_view = f"{self.first_value_web_view}x + {self.second_value_web_view} = 0"
        self.web_view.loadFinished.connect(lambda: self.update_math(self.main_value_web_view))
        
    def update_value_web_view(self):
        self.first_value_web_view = self.a_in.text()
        self.second_value_web_view = self.b_in.text()
        self.main_value_web_view = f"{self.first_value_web_view}x + {self.second_value_web_view} = 0"
        self.update_math(self.main_value_web_view)

    def create_web_view(self):
        self.web_view = QWebEngineView()
        self.web_view.setFixedHeight(50)
        # self.web_view.resize(200, 40)
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
        
        self.scroll_content_widget.layout().addWidget(web_view_widget)

    def update_math(self, text):
        latex_code = self.convert_to_latex(text)
        self.web_view.page().runJavaScript(f"updateMath('{latex_code}');")

    def convert_to_latex(self, text):
        text = re.sub(r'can{(.+?)}', r'\\sqrt{\1}', text)
        text = re.sub(r'can\[(\d+)\]{(.+?)}', r'\\sqrt[\1]{\2}', text)
        text = re.sub(r'phanso{(.+?)}{(.+?)}', r'\\frac{\1}{\2}', text)
        text = re.sub(r'tichphan{(.+?)}{(.+?)}{(.+?)}', r'\\int_{\1}^{\2} \3', text)
        text = text.replace(r'\thuoc', r'\\in')
        text = text.replace(r'\khongthuoc', r'\\notin')
        text = text.replace(r'\con', r'\\subset')
        text = text.replace(r'\cha', r'\\supset')
        text = text.replace(r'\rong', r'\\emptyset')
        text = text.replace(r'\hop', r'\\cup')
        text = text.replace(r'\giao', r'\\cap')
        text = re.sub(r'(\w+)\^(\d+)', r'\1^{\2}', text)
        return text

    def create_widgets(self):
        self.scroll_content_widget = QtWidgets.QWidget(self)
        self.main_layout.addWidget(self.scroll_content_widget)

        layout = QtWidgets.QVBoxLayout(self.scroll_content_widget)

        self.create_web_view()

        self.create_input_and_button()

        self.create_log_area()
        self.create_plot_area()


        self.scroll_content_widget.setLayout(layout)

    def create_input_and_button(self):
        input_layout = QtWidgets.QGridLayout()

        self.a_in = QtWidgets.QLineEdit(self)
        self.b_in = QtWidgets.QLineEdit(self)

        self.a_in.setPlaceholderText("Nhập hệ số a...")
        self.b_in.setPlaceholderText("Nhập hệ số b...")
        for item in [self.a_in, self.b_in]:
            item.setStyleSheet(styles(self.theme, 'input'))
        self.a_in.textChanged.connect(self.update_value_web_view)
        self.b_in.textChanged.connect(self.update_value_web_view)

        input_layout.addWidget(QtWidgets.QLabel("a:"), 0, 0)
        input_layout.addWidget(self.a_in, 0, 1)
        input_layout.addWidget(QtWidgets.QLabel("b:"), 1, 0)

        input_layout.addWidget(self.b_in, 1, 1)
        self.solve_btn = QtWidgets.QPushButton("Giải", self)
        self.solve_btn.setStyleSheet(styles(self.theme, 'submit'))
        self.solve_btn.clicked.connect(self.solve_equation)
        
        input_layout.addWidget(self.solve_btn, 2, 0, 1, 2)

        self.scroll_content_widget.layout().addLayout(input_layout)

    def create_plot_area(self):
        self.canvas_widget = QtWidgets.QWidget(self)
        self.canvas_layout = QtWidgets.QVBoxLayout(self.canvas_widget)
        self.scroll_content_widget.layout().addWidget(self.canvas_widget)

    def create_log_area(self):
        self.log_output = QtWidgets.QTextEdit(self)
        self.log_output.setStyleSheet(styles(self.theme, 'log_area'))
        self.log_output.setReadOnly(True)
        self.scroll_content_widget.layout().addWidget(self.log_output)

    def log(self, message, color="black"):
        colored_message = f'<font color="{color}">{message}</font>'
        self.log_output.append(colored_message)

        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())
    def solve_equation(self):
        try:
            a = float(self.a_in.text())
            b = float(self.b_in.text())
        except ValueError:
            self.log("Lỗi giá trị", 'red')
            return

        if a == 0 and b == 0:
            self.log("Phương trình có vô số nghiệm", "green")
        elif a == 0 and b != 0:
            self.log("Vô nghiệm", "green")
        else:
            x = -b / a
            if x == int(x):
                x = int(x)
            self.log(f"x = {x}", 'green')

        self.plot_graph(a, b)

    def plot_graph(self, a, b):
        x_values = np.linspace(-10, 10, 100)
        y_values = a * x_values + b

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(x_values, y_values, label=f"{a}x + {b} = 0")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.axhline(0, color="gray", linestyle="--")
        ax.axvline(0, color="gray", linestyle="--")
        ax.grid(True)

        x = -b / a
        ax.scatter(x, 0, color='hotpink')

        ax.legend(fontsize=6)

        canvas = FigureCanvas(fig)
        canvas.draw()

        for i in reversed(range(self.canvas_layout.count())):
            widget = self.canvas_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        self.canvas_layout.addWidget(canvas)
        plt.close(fig)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    layout = QtWidgets.QVBoxLayout()
    main_window = ptbn(layout)

    container = QtWidgets.QWidget()
    container.setLayout(layout)
    container.show()

    sys.exit(app.exec_())
