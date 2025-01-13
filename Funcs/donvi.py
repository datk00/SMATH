import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

from Styles.index import styles

def convert_units(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value

    conversion_factors = {
        # Length
        ("m", "dm"): 10,
        ("dm", "m"): 0.1,
        ("m", "cm"): 100,
        ("cm", "m"): 0.01,
        ("dm", "cm"): 10,
        ("cm", "dm"): 0.1,
        ("m", "mm"): 1000,
        ("mm", "m"): 0.001,
        ("dm", "mm"): 100,
        ("mm", "dm"): 0.01,
        ("cm", "mm"): 10,
        ("mm", "cm"): 0.1,
        ("mm", "dam"): 0.0001,
        ("mm", "hm"): 0.00001,
        ("mm", "Km"): 0.000001,
        ("dam", "m"): 10,
        ("dam", "hm"): 0.1,
        ("hm", "dam"): 10,
        ("hm", "m"): 100,
        ("m", "dam"): 0.1,
        ("m", "hm"): 0.01,
        ("Km", "hm"): 10,
        ("km", "dam"): 100,
        ("cm", "dam"): 0.001,
        ("dm", "dam"): 0.01,
        ("dam", "Km"): 0.01,
        ("hm", "Km"): 0.1,
        ("Km", "dm"): 10000,
        ("dm", "Km"): 0.0001,
        ("Km", "cm"): 100000,
        ("Km", "mm"): 1000000,
        ("hm", "dm"): 1000,
        ("dm", "hm"): 0.001,
        ("hm", "cm"): 100000,
        ("cm", "hm"): 0.0001,
        ("Km", "cm"): 100000,
        ("cm", "Km"): 0.00001,
        ("hm", "mm"): 1000000,
        ("dam", "dm"): 100,
        ("dm", "dam"): 0.01,
        ("dam", "cm"): 1000,
        ("cm", "dam"): 0.001,
        ("dam", "mm"): 10000,
        ("m", "Ft"): 3.28084,
        ("m", "Km"): 0.001,
        ("Km", "m"): 1000,
        ("Ft", "m"): 0.3048,
        ("dm", "Ft"): 0.328084,
        ("cm", "Ft"): 0.0328084,
        ("mm", "Ft"): 0.00328084,
        ("dam", "Ft"): 32.8084,
        ("hm", "Ft"): 328.084,
        ("Km", "Ft"): 3280.84,
        ("Km", "dam"): 100,
        ("Ft", "dm"): 3.048,
        ("Ft", "cm"): 30.48,
        ("Ft", "mm"): 304.8,
        ("Ft", "dam"): 0.03048,
        ("Ft", "hm"): 0.003048,
        ("Ft", "Km"): 0.0003048,
        # Temperature
        ("Độ C", "Độ F"): lambda x: (x * 9/5) + 32,
        ("Độ F", "Độ C"): lambda x: (x - 32) * 5/9,
        ("°C", "°F"): lambda x: x * (9/5) + 32,
        ("°F", "°C"): lambda x: (x - 32) / (9/5),
        ("°K", "°C"): lambda x: x - 273.15,
        ("°C", "°K"): lambda x: x + 273.15,
        ("°K", "°F"): lambda x: (x-273.15) * (9/5) + 32,
        ("°F", "°K"): lambda x: (x - 32) / (9/5) + 273.15,
    }
    if (from_unit, to_unit) in conversion_factors:
        factor = conversion_factors[(from_unit, to_unit)]
        return factor(value) if callable(factor) else value * factor
    else:
        return "Không đổi được"

class donvi(QtWidgets.QWidget):
    def __init__(self, layout, currentTheme):
        super().__init__()

        # Main layout
        self.main_layout = layout
        self.theme = currentTheme
        self.create_widgets()

    def create_widgets(self):
        # Category selection (Khoảng cách, Khối lượng, ...)
        self.category_selector = QtWidgets.QComboBox(self)
        self.category_selector.setStyleSheet(styles(self.theme, 'combo_box'))
        self.category_selector.addItems([
            "Chọn đại lượng...", "Khoảng cách", "Khối lượng", "Thể tích", "Diện tích", "Nhiệt độ"
        ])
        self.category_selector.currentTextChanged.connect(self.update_units)

        # Value input
        self.value_entry = QtWidgets.QLineEdit(self)
        self.value_entry.setStyleSheet(styles(self.theme, 'input'))
        self.value_entry.setPlaceholderText("Nhập giá trị...")

        # From and To unit selectors
        self.from_unit_selector = QtWidgets.QComboBox(self)
        self.to_unit_selector = QtWidgets.QComboBox(self)

        for item in [self.from_unit_selector, self.to_unit_selector]:
            item.setStyleSheet(styles(self.theme, 'combo_box'))
        # Convert button
        self.convert_button = QtWidgets.QPushButton("Chuyển đổi", self)
        self.convert_button.setStyleSheet(styles(self.theme, 'submit'))
        self.convert_button.clicked.connect(self.convert_unit)

        # Result display
        # self.result_label = QtWidgets.QLabel(self)

        # Log output
        self.log_output = QtWidgets.QTextEdit(self)
        self.log_output.setStyleSheet(styles(self.theme, 'log_area'))

        # Set the layout to the widget
        layout = QtWidgets.QVBoxLayout(self)  # Create a new layout for the widget
        layout.addWidget(self.category_selector)
        layout.addWidget(self.value_entry)
        layout.addWidget(self.from_unit_selector)
        layout.addWidget(self.to_unit_selector)
        layout.addWidget(self.convert_button)
        # layout.addWidget(self.result_label)
        layout.addWidget(self.log_output)

        # Set the layout to the widget
        self.setLayout(layout)

        # Unit categories
        self.units_dict = {
            "Chọn đại lượng...": [],
            "Khoảng cách": ["m", "dm", "cm", "mm", "dam", "hm", "Km", "Ft"],
            "Khối lượng": ["g", "Kg", "Pound", "yến", "tạ", "tấn"],
            "Thể tích": ["L", "mL", "m³", "Ft³"],
            "Diện tích": ["m²", "Km²", "Ft²"],
            "Nhiệt độ": ["°C", "°F", "°K"]
        }

        # Initialize with default units
        self.update_units()

    def update_units(self):
        category = self.category_selector.currentText()
        units = self.units_dict.get(category, [])
        self.from_unit_selector.clear()
        self.to_unit_selector.clear()
        self.from_unit_selector.addItems(units)
        self.to_unit_selector.addItems(units)

    def convert_unit(self):
        category = self.category_selector.currentText()
        value = self.value_entry.text()

        if not value:
            self.log("Vui lòng nhập giá trị cần chuyển đổi.", 'red')
            return

        try:
            value = float(value)
        except ValueError:
            self.log("Giá trị không hợp lệ.", 'red')
            return

        from_unit = self.from_unit_selector.currentText()
        to_unit = self.to_unit_selector.currentText()

        converted_value = convert_units(value, from_unit, to_unit)

        # if converted_value == "Không đổi được":
        #     self.log("Không đổi được", "blue")

        self.log(f"Chuyển đổi từ {from_unit} đến {to_unit} với giá trị: {value} -> {converted_value}", 'green')

    def log(self, message, color="black"):
        colored_message = f'<font color="{color}">{message}</font>'
        self.log_output.append(colored_message)

        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())