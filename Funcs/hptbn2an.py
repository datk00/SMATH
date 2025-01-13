import sys, re
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from Styles.index import styles

class hptbn2an(QtWidgets.QWidget):
    def __init__(self, layout, currentTheme):
        super().__init__()
        self.main_layout = layout
        self.theme = currentTheme

        # Scrollable content widget
        self.scroll_content_widget = QtWidgets.QWidget(self)
        self.main_layout.addWidget(self.scroll_content_widget)
        content_layout = QtWidgets.QVBoxLayout(self.scroll_content_widget)

        # Web View (for displaying math in LaTeX format)
        self.create_web_view(content_layout)

        # Input & Button Area
        self.create_input_and_button(content_layout)

        # Log Area (output area)
        self.create_log_area(content_layout)

        # Graph Area (for plotting the system of equations)
        self.create_plot_area(content_layout)

        self.scroll_content_widget.setLayout(content_layout)

        self.a1_value = 'a₁'
        self.a2_value = 'a₂'
        self.b1_value = 'b₁'
        self.b2_value = 'b₂'
        self.c1_value = 'c₁'
        self.c2_value = 'c₂'
        self.main_value1 = f'{self.a1_value}x + {self.b1_value}y = {self.c1_value}'
        self.main_value2 = f'{self.a2_value}x + {self.b2_value}y = {self.c2_value}'
        self.web_view.loadFinished.connect(lambda: self.update_math1(self.main_value1))
        self.web_view.loadFinished.connect(lambda: self.update_math2(self.main_value1))
    def update_value_web_view(self):
        self.a1_value = self.a1_in.text()
        self.a2_value = self.a2_in.text()
        self.b1_value = self.b1_in.text()
        self.b2_value = self.b2_in.text()
        self.c1_value = self.c1_in.text()
        self.c2_value = self.c2_in.text()
        self.main_value1 = f'{self.a1_value}x + {self.b1_value}y = {self.c1_value}'
        self.main_value2 = f'{self.a2_value}x + {self.b2_value}y = {self.c2_value}'
        self.update_math1(self.main_value1)
        self.update_math2(self.main_value2)
    def update_math1(self, text):
        latex_code = self.convert_to_latex(text)
        self.web_view.page().runJavaScript(f"updateMath1('{latex_code}');")
    def update_math2(self, text):
        latex_code = self.convert_to_latex(text)
        self.web_view.page().runJavaScript(f"updateMath2('{latex_code}');")

    def convert_to_latex(self, text):
        # Tìm kiếm và thay thế các biểu thức toán học thành LaTeX
        text = re.sub(r'(\w+)\^(\d+)', r'\1^{\2}', text)  # Công thức có dạng x^2
        return text
    def create_web_view(self, layout):
        self.web_view = QWebEngineView(self)
        self.web_view.setFixedHeight(80)
        self.web_view.setHtml("""
            <html>
            <head>
                <style>
                    #MathJax_Message { display: none; }
                </style>
                <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML"></script>
            </head>
            <body>
                <div id="output1"></div>
                <div id="output2"></div>
                <script>
                    function updateMath1(latex) {
                        document.getElementById('output1').innerHTML = '$$' + latex + '$$';
                        MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
                    }
                    function updateMath2(latex) {
                        document.getElementById('output2').innerHTML = '$$' + latex + '$$';
                        MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
                    }
                </script>
            </body>
            </html>
        """)
        layout.addWidget(self.web_view)

    def create_input_and_button(self, layout):
        input_layout = QtWidgets.QGridLayout()

        # Create input fields
        self.a1_in = QtWidgets.QLineEdit(self)
        self.b1_in = QtWidgets.QLineEdit(self)
        self.c1_in = QtWidgets.QLineEdit(self)
        self.a2_in = QtWidgets.QLineEdit(self)
        self.b2_in = QtWidgets.QLineEdit(self)
        self.c2_in = QtWidgets.QLineEdit(self)

        self.a1_in.setPlaceholderText("Nhập hệ số a₁...")
        self.a2_in.setPlaceholderText("Nhập hệ số a₂...")
        self.b1_in.setPlaceholderText("Nhập hệ số b₁...")
        self.b2_in.setPlaceholderText("Nhập hệ số b₂...")
        self.c1_in.setPlaceholderText("Nhập hệ số c₁...")
        self.c2_in.setPlaceholderText("Nhập hệ số c₂...")
        for item in [self.a1_in, self.a2_in, self.b1_in, self.b2_in, self.c1_in, self.c2_in]:
            item.setStyleSheet(styles(self.theme, 'input'))

        input_layout.addWidget(QtWidgets.QLabel("a₁:"), 0, 0)
        input_layout.addWidget(self.a1_in, 0, 1)
        input_layout.addWidget(QtWidgets.QLabel("b₁:"), 0, 2)
        input_layout.addWidget(self.b1_in, 0, 3)
        input_layout.addWidget(QtWidgets.QLabel("c₁:"), 0, 4)
        input_layout.addWidget(self.c1_in, 0, 5)
        input_layout.addWidget(QtWidgets.QLabel("a₂:"), 1, 0)
        input_layout.addWidget(self.a2_in, 1, 1)
        input_layout.addWidget(QtWidgets.QLabel("b₂:"), 1, 2)
        input_layout.addWidget(self.b2_in, 1, 3)
        input_layout.addWidget(QtWidgets.QLabel("c₂:"), 1, 4)
        input_layout.addWidget(self.c2_in, 1, 5)

        for item in [self.a1_in, self.a2_in, self.b1_in, self.b2_in, self.c1_in, self.c2_in]:
            item.textChanged.connect(self.update_value_web_view)

        # Solve button
        self.solve_btn = QtWidgets.QPushButton("Giải", self)
        self.solve_btn.setStyleSheet(styles(self.theme, 'submit'))
        self.solve_btn.clicked.connect(self.solve_system)
        input_layout.addWidget(self.solve_btn, 2, 0, 1, 6) 

        layout.addLayout(input_layout)

    def create_log_area(self, layout):
        self.log_output = QtWidgets.QTextEdit(self)
        self.log_output.setStyleSheet(styles(self.theme, 'log_area'))
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

    def create_plot_area(self, layout):
        self.canvas_widget = QtWidgets.QWidget(self)
        self.canvas_layout = QtWidgets.QVBoxLayout(self.canvas_widget)
        layout.addWidget(self.canvas_widget)

    def log(self, message, color="black"):
        colored_message = f'<font color="{color}">{message}</font>'
        self.log_output.append(colored_message)

        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())
    def solve_system(self):
        try:
            a1, a2, b1, b2, c1, c2 = map(float, [
                self.a1_in.text(), self.a2_in.text(),
                self.b1_in.text(), self.b2_in.text(),
                self.c1_in.text(), self.c2_in.text()
            ])
        except ValueError:
            self.log("Hệ số không hợp lệ. Vui lòng nhập số!", "red")
            return

        # Tính định thức (determinant)
        det = a1 * b2 - a2 * b1

        # Xử lý các trường hợp đặc biệt
        if det == 0:
            # Trường hợp det = 0, kiểm tra xem có vô số nghiệm hay vô nghiệm
            if a1 * c2 == a2 * c1 and b1 * c2 == b2 * c1:
                self.log("=> Hệ phương trình có vô số nghiệm", 'green')
            else:
                self.log("=> Hệ phương trình vô nghiệm", 'green')
        else:
            # Trường hợp hệ có nghiệm duy nhất
            x = ((b2 * c1) - (b1 * c2)) / det
            y = ((a1 * c2) - (a2 * c1)) / det
            self.log(f"x = {x}", 'green')
            self.log(f"y = {y}", 'green')

        # Vẽ đồ thị
        self.plot_graph(a1, b1, c1, a2, b2, c2)

    def plot_graph(self, a1, b1, c1, a2, b2, c2):
        x_values = np.linspace(-10, 10, 100)
        y_values1 = (c1 - a1 * x_values) / b1
        y_values2 = (c2 - a2 * x_values) / b2

        # Vẽ đồ thị
        fig, ax = plt.subplots(figsize=(5, 3))  # Điều chỉnh kích thước đồ thị
        ax.plot(x_values, y_values1, label=f"{a1}x + {b1}y = {c1}", alpha=0.5)
        ax.plot(x_values, y_values2, label=f"{a2}x + {b2}y = {c2}", color='lime', alpha=0.5)

        if a1 / a2 == b1 / b2 == c1 / c2:
            ax.plot(x_values, y_values2, color='red', alpha=0.8)

        ax.axhline(0, color="gray", linestyle="--")  # Đường ngang y=0
        ax.axvline(0, color="gray", linestyle="--")  # Đường dọc x=0

        # Điểm giao nếu có
        if a1 / a2 != b1 / b2:
            x = ((b2 * c1) - (b1 * c2)) / ((a1 * b2) - (a2 * b1))
            y = ((a1 * c2) - (a2 * c1)) / ((a1 * b2) - (a2 * b1))
            ax.scatter(x, y, color='hotpink')

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

# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     main_window = hptbn2an()
#     main_window.show()
#     sys.exit(app.exec_())
