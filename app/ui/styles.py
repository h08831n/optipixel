# PySide6 Modern QSS Stylesheets matching Web Theme (Slate & Indigo)

DARK_STYLESHEET = """
QMainWindow, QDialog {
    background-color: #0B0F19;
    color: #F8FAFC;
}

QWidget {
    font-family: "IRANYekanX", "IRANYekan", "IRANYekanXVF", "Vazirmatn", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 13px;
    color: #F8FAFC;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: transparent;
    width: 8px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #334155;
    min-height: 24px;
    border-radius: 4px;
}
QScrollBar::handle:vertical:hover {
    background: #475569;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background: transparent;
    height: 8px;
    margin: 0px;
}
QScrollBar::handle:horizontal {
    background: #334155;
    min-width: 24px;
    border-radius: 4px;
}
QScrollBar::handle:horizontal:hover {
    background: #475569;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* Sidebar List Widget */
QListWidget#SidebarList {
    background-color: #0F172A;
    border-right: 1px solid #1E293B;
    outline: none;
    padding-top: 12px;
}

QListWidget#SidebarList::item {
    height: 48px;
    padding-left: 16px;
    padding-right: 16px;
    color: #94A3B8;
    border-radius: 10px;
    margin: 4px 10px;
    font-size: 13px;
    font-weight: 600;
}

QListWidget#SidebarList::item:hover {
    background-color: #1E293B;
    color: #F8FAFC;
}

QListWidget#SidebarList::item:selected {
    background-color: #4F46E5;
    color: #FFFFFF;
    font-weight: 700;
}

/* Cards & GroupBoxes */
QGroupBox {
    background-color: #161F32;
    border: 1px solid #23314D;
    border-radius: 14px;
    margin-top: 24px;
    padding-top: 18px;
    padding-left: 14px;
    padding-right: 14px;
    padding-bottom: 14px;
    font-weight: 700;
    font-size: 13px;
    color: #CBD5E1;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 3px 12px;
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 8px;
    color: #818CF8;
    font-weight: 700;
}

QFrame#StatsCard {
    background-color: #161F32;
    border: 1px solid #23314D;
    border-radius: 14px;
    padding: 16px;
}

QFrame#StatsCard QLabel#Title {
    font-size: 12px;
    color: #94A3B8;
    font-weight: 600;
}

QFrame#StatsCard QLabel#Value {
    font-size: 24px;
    color: #F8FAFC;
    font-weight: 800;
}

QFrame#StatsCard QLabel#Subtitle {
    font-size: 11px;
    color: #64748B;
}

/* DropZone Widget */
QFrame#DropZone {
    background-color: #111827;
    border: 2px dashed #4F46E5;
    border-radius: 16px;
    padding: 28px;
}

QFrame#DropZone:hover {
    background-color: #1E1B4B;
    border-color: #818CF8;
}

/* Buttons */
QPushButton {
    background-color: #1E293B;
    color: #F8FAFC;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 8px 18px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #334155;
    border-color: #475569;
}

QPushButton:pressed {
    background-color: #0F172A;
}

QPushButton#PrimaryButton {
    background-color: #4F46E5;
    color: #FFFFFF;
    border: none;
    font-weight: 700;
    padding: 10px 24px;
    border-radius: 10px;
}

QPushButton#PrimaryButton:hover {
    background-color: #4338CA;
}

QPushButton#PrimaryButton:disabled {
    background-color: #312E81;
    color: #6366F1;
}

QPushButton#DangerButton {
    background-color: #991B1B;
    color: #FEE2E2;
    border: none;
    border-radius: 10px;
}

QPushButton#DangerButton:hover {
    background-color: #B91C1C;
}

/* Inputs & Selects */
QComboBox, QSpinBox, QLineEdit {
    background-color: #111827;
    border: 1px solid #23314D;
    border-radius: 10px;
    padding: 7px 12px;
    color: #F8FAFC;
    font-size: 13px;
}

QComboBox:hover, QSpinBox:hover, QLineEdit:hover {
    border-color: #6366F1;
}

QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}

QComboBox QAbstractItemView {
    background-color: #1E293B;
    border: 1px solid #334155;
    color: #F8FAFC;
    selection-background-color: #4F46E5;
    border-radius: 8px;
}

/* CheckBox */
QCheckBox {
    spacing: 8px;
    font-size: 13px;
    color: #E2E8F0;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 5px;
    border: 1px solid #475569;
    background-color: #0F172A;
}

QCheckBox::indicator:checked {
    background-color: #4F46E5;
    border-color: #4F46E5;
}

/* Tables */
QTableWidget {
    background-color: #111827;
    border: 1px solid #1E293B;
    border-radius: 12px;
    gridline-color: #1F2937;
    color: #E2E8F0;
    selection-background-color: #1E1B4B;
}

QHeaderView::section {
    background-color: #1F2937;
    color: #9CA3AF;
    padding: 10px 14px;
    border: none;
    border-bottom: 1px solid #374151;
    font-weight: 700;
    font-size: 12px;
}

QTableWidget::item {
    padding: 10px;
    border-bottom: 1px solid #1F2937;
}

QTableWidget::item:selected {
    background-color: #312E81;
    color: #FFFFFF;
}

/* Progress Bar */
QProgressBar {
    background-color: #1F2937;
    border: 1px solid #374151;
    border-radius: 10px;
    height: 20px;
    text-align: center;
    color: #F8FAFC;
    font-size: 11px;
    font-weight: 700;
}

QProgressBar::chunk {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4F46E5, stop:1 #818CF8);
    border-radius: 9px;
}

/* Status Bar */
QStatusBar {
    background-color: #0F172A;
    border-top: 1px solid #1E293B;
    color: #64748B;
    font-size: 12px;
    padding: 4px;
}
"""

LIGHT_STYLESHEET = """
QMainWindow, QDialog {
    background-color: #F8FAFC;
    color: #0F172A;
}

QWidget {
    font-family: "IRANYekanX", "IRANYekan", "IRANYekanXVF", "Vazirmatn", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 13px;
    color: #0F172A;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: transparent;
    width: 8px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #CBD5E1;
    min-height: 24px;
    border-radius: 4px;
}
QScrollBar::handle:vertical:hover {
    background: #94A3B8;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background: transparent;
    height: 8px;
    margin: 0px;
}
QScrollBar::handle:horizontal {
    background: #CBD5E1;
    min-width: 24px;
    border-radius: 4px;
}
QScrollBar::handle:horizontal:hover {
    background: #94A3B8;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* Sidebar List Widget */
QListWidget#SidebarList {
    background-color: #FFFFFF;
    border-right: 1px solid #E2E8F0;
    outline: none;
    padding-top: 12px;
}

QListWidget#SidebarList::item {
    height: 48px;
    padding-left: 16px;
    padding-right: 16px;
    color: #64748B;
    border-radius: 10px;
    margin: 4px 10px;
    font-size: 13px;
    font-weight: 600;
}

QListWidget#SidebarList::item:hover {
    background-color: #F1F5F9;
    color: #0F172A;
}

QListWidget#SidebarList::item:selected {
    background-color: #4F46E5;
    color: #FFFFFF;
    font-weight: 700;
}

/* Cards & GroupBoxes */
QGroupBox {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    margin-top: 24px;
    padding-top: 18px;
    padding-left: 14px;
    padding-right: 14px;
    padding-bottom: 14px;
    font-weight: 700;
    font-size: 13px;
    color: #334155;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 3px 12px;
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    color: #4F46E5;
    font-weight: 700;
}

QFrame#StatsCard {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 16px;
}

QFrame#StatsCard QLabel#Title {
    font-size: 12px;
    color: #64748B;
    font-weight: 600;
}

QFrame#StatsCard QLabel#Value {
    font-size: 24px;
    color: #0F172A;
    font-weight: 800;
}

QFrame#StatsCard QLabel#Subtitle {
    font-size: 11px;
    color: #94A3B8;
}

/* DropZone Widget */
QFrame#DropZone {
    background-color: #FFFFFF;
    border: 2px dashed #818CF8;
    border-radius: 16px;
    padding: 28px;
}

QFrame#DropZone:hover {
    background-color: #EEF2FF;
    border-color: #4F46E5;
}

/* Buttons */
QPushButton {
    background-color: #F1F5F9;
    color: #0F172A;
    border: 1px solid #CBD5E1;
    border-radius: 10px;
    padding: 8px 18px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #E2E8F0;
    border-color: #94A3B8;
}

QPushButton:pressed {
    background-color: #CBD5E1;
}

QPushButton#PrimaryButton {
    background-color: #4F46E5;
    color: #FFFFFF;
    border: none;
    font-weight: 700;
    padding: 10px 24px;
    border-radius: 10px;
}

QPushButton#PrimaryButton:hover {
    background-color: #4338CA;
}

QPushButton#PrimaryButton:disabled {
    background-color: #C7D2FE;
    color: #6366F1;
}

QPushButton#DangerButton {
    background-color: #FEE2E2;
    color: #991B1B;
    border: 1px solid #FCA5A5;
    border-radius: 10px;
}

QPushButton#DangerButton:hover {
    background-color: #FCA5A5;
}

/* Inputs & Selects */
QComboBox, QSpinBox, QLineEdit {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 10px;
    padding: 7px 12px;
    color: #0F172A;
    font-size: 13px;
}

QComboBox:hover, QSpinBox:hover, QLineEdit:hover {
    border-color: #4F46E5;
}

QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}

QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    color: #0F172A;
    selection-background-color: #4F46E5;
    selection-color: #FFFFFF;
    border-radius: 8px;
}

/* CheckBox */
QCheckBox {
    spacing: 8px;
    font-size: 13px;
    color: #1E293B;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 5px;
    border: 1px solid #94A3B8;
    background-color: #FFFFFF;
}

QCheckBox::indicator:checked {
    background-color: #4F46E5;
    border-color: #4F46E5;
}

/* Tables */
QTableWidget {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    gridline-color: #F1F5F9;
    color: #0F172A;
}

QHeaderView::section {
    background-color: #F8FAFC;
    color: #64748B;
    padding: 10px 14px;
    border: none;
    border-bottom: 1px solid #E2E8F0;
    font-weight: 700;
    font-size: 12px;
}

QTableWidget::item {
    padding: 10px;
    border-bottom: 1px solid #F1F5F9;
}

QTableWidget::item:selected {
    background-color: #EEF2FF;
    color: #4F46E5;
}

/* Progress Bar */
QProgressBar {
    background-color: #E2E8F0;
    border: 1px solid #CBD5E1;
    border-radius: 10px;
    height: 20px;
    text-align: center;
    color: #0F172A;
    font-size: 11px;
    font-weight: 700;
}

QProgressBar::chunk {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4F46E5, stop:1 #818CF8);
    border-radius: 9px;
}

/* Status Bar */
QStatusBar {
    background-color: #FFFFFF;
    border-top: 1px solid #E2E8F0;
    color: #64748B;
    font-size: 12px;
    padding: 4px;
}
"""

