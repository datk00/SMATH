from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from vedothi import FunctionPlotter
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vẽ đồ thị hàm số")
        self.setMinimumSize(800, 600)
        
        # Widget và layout chính
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Khởi tạo FunctionPlotter với layout chính
        self.plotter = FunctionPlotter(main_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())