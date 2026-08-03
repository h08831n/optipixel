from PySide6.QtWidgets import QWidget, QHBoxLayout, QSlider, QLabel, QSpinBox
from PySide6.QtCore import Qt

class QualityControlWidget(QWidget):
    def __init__(self, default_value: int = 82, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel("Quality:"))

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(1, 100)
        self.slider.setValue(default_value)

        self.spin = QSpinBox()
        self.spin.setRange(1, 100)
        self.spin.setValue(default_value)

        self.slider.valueChanged.connect(self.spin.setValue)
        self.spin.valueChanged.connect(self.slider.setValue)

        layout.addWidget(self.slider)
        layout.addWidget(self.spin)

    def value(self) -> int:
        return self.spin.value()
