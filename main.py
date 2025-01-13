from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QStackedWidget, QFrame, QComboBox, QScrollArea
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


from Layouts.layout import LAYOUTS
from Themes.theme import LIGHT_THEME, DARK_THEME





light_theme = LIGHT_THEME
dark_theme = DARK_THEME
current_theme = dark_theme
idx_theme = 1

layoutSoftware = LAYOUTS


def create_button(layout, content, path_icon='', size_icon=[24, 24], isActive = False,  connectTo=None):
    btn = QPushButton(content)
    if path_icon != '':
        btn.setIcon(QIcon(path_icon))
        btn.setIconSize(QSize(size_icon[0], size_icon[1]))
    btn.setFont(QFont("Arial", 12))
    base_style = f"""
        QPushButton {{
            background-color: {current_theme['navbar']['buttonBackground']};
            color: {current_theme['navbar']['text']};
            border-radius: 5px;
            padding: 10px;
            text-align: left;
        }}
        QPushButton:hover {{
            background-color: {current_theme['navbar']['hover']};
            color: {current_theme['navbar']['color']}
        }}
        QPushButton:checked {{
            background-color: {current_theme['navbar']['hover']};
        }}
    """

    # Nếu button được active, thay đổi style cho nó
    if isActive:
        active_style = f"""
            QPushButton {{
                background-color: {current_theme['navbar']['hover']};
                color: {current_theme['navbar']['color']};
            }}
        """
        # Kết hợp base style và active style
        btn.setStyleSheet(base_style + active_style)
    else:
        # Nếu không active, chỉ giữ base style
        btn.setStyleSheet(base_style)
    if connectTo:
        btn.clicked.connect(connectTo)

    layout.addWidget(btn)
    btn.setCursor(Qt.PointingHandCursor)
    return btn

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SMATH 1.0")
        self.setGeometry(100, 100, 1000, 600)

        self.main_layout = QHBoxLayout()

        # Program layout logic
        # self.math_program = DerivativePlotter()
        self.text_header_base = 'SMATH'
        self.text_header_current_page_layout1 = ''
        self.text_header_current_page_layout2 = ''

        self.create_navbar()
        self.create_options_frame()
        self.create_program_frame()

        self.content_stacked = QStackedWidget()
        self.content_stacked.addWidget(self.options_frame)
        self.content_stacked.addWidget(self.program_frame)
        
        self.main_layout.addWidget(self.navbar_frame)
        self.main_layout.addWidget(self.content_stacked)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

        self.apply_theme()

    def create_navbar(self, addWidget = False):
        if hasattr(self, 'navbar_frame') and self.navbar_frame:
            self.main_layout.removeWidget(self.navbar_frame)
            self.navbar_frame.deleteLater()
        
        navbar_frame = QFrame()
        navbar_frame.setFixedWidth(200)
        navbar_frame.setStyleSheet(f"""
            QFrame {{ 
                background-color: {current_theme['navbar']['background']};
                margin: 0px;
                padding: 0px;
                border-radius: 8px;
            }}
                """)
        navbar_layout = QVBoxLayout()

        header_layout = QHBoxLayout()

        logo_image = QLabel()
        if (idx_theme == 1):
            pixmap = QPixmap('./Images/logo.png')
        else:
            pixmap = QPixmap('./Images/logo_dark.png')

        scaled_pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_image.setPixmap(scaled_pixmap)
        logo_image.setAlignment(Qt.AlignLeft)

        logo_text = QLabel("SMATH")
        logo_text.setFont(QFont("Arial", 18, QFont.Bold))
        logo_text.setAlignment(Qt.AlignCenter)
        logo_text.setStyleSheet(f"color: {current_theme['navbar']['text']};")

        header_layout.addWidget(logo_image)
        header_layout.addWidget(logo_text)
        header_layout.setAlignment(Qt.AlignLeft)
        header_layout.setSpacing(10)

        navbar_layout.addLayout(header_layout)
        # navbar_layout.addWidget(logo)

        # Reset all button objects
        for item in layoutSoftware:
            if '_object' in item:
                del item['_object']

        for item in layoutSoftware:
            btn = create_button(navbar_layout, item['content'], item['icon']['path'], 
                            item['icon']['size'], isActive=item['active'])
            item['_object'] = btn
            btn.clicked.connect(lambda checked, action=item['action']: self.handle_button_action(action))

        self.theme_select = QComboBox()
        self.theme_select.addItem("Chế độ sáng")
        self.theme_select.addItem("Chế độ tối")
        self.theme_select.setCurrentIndex(idx_theme)
        self.theme_select.currentIndexChanged.connect(self.toggle_theme)
        self.theme_select.setStyleSheet(f"""
            QComboBox {{
                background-color: {current_theme['navbar']['buttonBackground']};
                color: {current_theme['navbar']['text']};
                border-radius: 5px;
                padding: 10px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {current_theme['navbar']['background']};
                color: {current_theme['navbar']['text']};
                selection-background-color: {current_theme['navbar']['hover']};
                padding: 5px;
            }}
        """)
        navbar_layout.addWidget(self.theme_select)
        navbar_layout.addStretch()

        self.scroll_area = QScrollArea()
        self.scroll_area.setStyleSheet("""
        QScrollArea {
            border: none;
            outline: none;  
            border-radius: 8px;                             
        }
""")
        self.scroll_area.setFixedWidth(210)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(navbar_frame)
        
        navbar_frame.setLayout(navbar_layout)
        self.navbar_frame = self.scroll_area

        if addWidget:
            self.main_layout.insertWidget(0, self.navbar_frame)
    def handle_button_action(self, action):
        
        """ Hàm xử lý khi button được nhấn """

        if action == 'phuong_trinh':
            self.show_options("Phương trình")
        elif action == 'bat_phuong_trinh':
            self.show_options("Bất phương trình")
        elif action == 'do_thi_tong_hop':
            self.show_options("Đồ thị tổng hợp")

        
        for item in layoutSoftware:
            item['active'] = False
        for item in layoutSoftware:
            if item['action'] == action:
                item['active'] = True
                self.create_navbar(addWidget=True)
                break
            else:
                item['active'] = False
    def create_options_frame(self):
        self.options_frame = QFrame()
        self.options_layout = QVBoxLayout()
        self.options_frame.setLayout(self.options_layout)

    def create_program_frame(self):
        self.program_frame = QFrame()
        
        self.program_layout = QVBoxLayout()

        self.program_frame.setLayout(self.program_layout)
        self.program_frame.hide()
    def apply_theme(self):
        theme = current_theme
        
        self.setStyleSheet(f"background-color: {theme['background']};")
        
        self.create_navbar(True)
        
        options_style = f"""
            QPushButton {{
                background-color: {theme['navbar']['buttonBackground']};
                color: {theme['options']['text']};
                border-radius: 5px;
                padding: 10px;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {theme['options']['hover']};
                color: {theme['navbar']['color']};
            }}
        """
        self.options_frame.setStyleSheet(options_style)

        self.program_frame.setStyleSheet(f"""
            QLineEdit {{
                background-color: {theme['program']['input']['background']};
                color: {theme['program']['input']['color']};
                padding: 5px;
                border-radius: 3px;
            }}
            QLabel {{
                color: {theme['program']['text']}
            }}                
            QPushButton {{
                background-color: {theme['program']['button']['background']};
                color: {theme['program']['button']['color']};
                border-radius: 5px;
                padding: 8px;
            }}
            QPushButton:hover {{
                background-color: {theme['program']['button']['background_hover']};
            }}
            QTextEdit {{
                background-color: {theme['program']['log-area']['background']};
                color: {theme['program']['text']};
                border-radius: 3px;
                padding: 5px;
            }}
            QComboBox {{
                background-color: {theme['program']['input']['background']};
                color: {theme['program']['input']['color']};
            }}
            QComboBox QAbstractItemView {{
            background-color: {theme['program']['input']['background']};
            color: {theme['program']['input']['color']};
            padding: 5px;
            }}
        """)

        if hasattr(self, 'text_header_current_page_layout1') and self.text_header_current_page_layout1:
            self.create_text_header(self.options_layout, 'noEdit')

        for item in layoutSoftware:
            if item['active']:
                self.show_options(item['content'])
                break

    def toggle_theme(self):
        global current_theme, idx_theme
        if self.theme_select.currentIndex() == 0:
            current_theme = light_theme
            idx_theme = 0
        else:
            current_theme = dark_theme
            idx_theme = 1
        self.apply_theme()
    def create_text_header(self, layout, title1 = '', title2 = ''):
            if title1 and title1 != 'noEdit':
                self.text_header_current_page_layout1 = title1
            self.text_header_current_page_layout2 = title2

            if (self.text_header_current_page_layout1):
                content = f"{self.text_header_base} / {self.text_header_current_page_layout1}"
            if (self.text_header_current_page_layout2):
                content = f"{self.text_header_base} / {self.text_header_current_page_layout1} / {self.text_header_current_page_layout2}"
            
            options_title = QLabel(content)
            options_title.setFont(QFont("Arial", 12))
            options_title.setStyleSheet(f"color: {current_theme['options']['textHeader']}; margin-bottom: 20px;")
            layout.addWidget(options_title)
    def show_options(self, title):
        self.options_layout.setAlignment(Qt.AlignTop)
        for i in reversed(range(self.options_layout.count())):
            self.options_layout.itemAt(i).widget().deleteLater()
        for i in reversed(range(self.program_layout.count())):
            widget = self.program_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        
        self.create_text_header(self.options_layout, title1 = title)
        def create_buttons_children(childrens = []):
            for item in layoutSoftware:
                if title == item['content']:
                    childrens = item['children']
                    break
            for childItem in childrens:
                def create_click_function(childItem=childItem): 
                    return lambda: self.show_program(childItem['handleProgram'], childItem['content'])

                clickFunction = create_click_function(childItem)

                create_button(self.options_layout, childItem['content'], connectTo=clickFunction)

        for item in layoutSoftware:
            if title == item['content']:
                create_buttons_children(item['children'])

        self.content_stacked.setCurrentWidget(self.options_frame)

    def show_program(self, programWidget, title):
        # Xóa các widget cũ trong chương trình
            
        self.create_text_header(self.program_layout, title1 = 'noEdit', title2=title)
        if programWidget:
            # Tạo đối tượng mới từ ptbn và thêm vào layout
            ptbn_widget = programWidget(self.program_layout, current_theme)  # ptbn_widget là một đối tượng của lớp ptbn
            
            self.program_layout.addWidget(ptbn_widget)  # Thêm widget vào layout
        
        self.program_frame.show()
        self.content_stacked.setCurrentWidget(self.program_frame)
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
